# core/wake_word.py

import pvporcupine
import sounddevice as sd
import struct


class WakeWordDetector:

    def __init__(self, access_key, keyword="jarvis"):

        self.porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=[keyword],
            sensitivities=[0.8]
        )

        self.sample_rate = self.porcupine.sample_rate
        self.frame_length = self.porcupine.frame_length

        self.stream = None

    def start_stream(self):

        if self.stream:
            return

        # DO NOT force device index
        # DO NOT force custom sample rate
        # Let PortAudio select compatible settings

        self.stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.frame_length,
            dtype="int16",
            channels=1
        )

        self.stream.start()

    def listen(self, shutdown_event=None):

        if not self.stream:
            self.start_stream()

        while True:

            if shutdown_event and shutdown_event.is_set():
                return False

            pcm, _ = self.stream.read(self.frame_length)

            pcm = struct.unpack_from(
                "h" * self.frame_length,
                pcm
            )

            result = self.porcupine.process(pcm)

            if result >= 0:
                print("WAKE DETECTED")
                return True

    def pause(self):
        if self.stream:
            self.stream.stop()

    def resume(self):
        if self.stream:
            self.stream.start()

    def shutdown(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
        self.porcupine.delete()