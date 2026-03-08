# core/voice.py

import os

# 🔥 Force FFmpeg path into environment BEFORE importing whisper
FFMPEG_PATH = r"C:\Users\Hehanth\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

import sounddevice as sd
import numpy as np
import pyttsx3
import whisper
import tempfile
from scipy.signal import resample
from scipy.io.wavfile import write


DEVICE_SAMPLERATE = 44100
MODEL_SAMPLERATE = 16000
RECORD_DURATION = 4


# ===============================
# TTS ENGINE
# ===============================

engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)


# ===============================
# LOAD WHISPER MODEL
# ===============================

try:
    _whisper_model = whisper.load_model("base")
except Exception as e:
    print("Whisper model load error:", e)
    _whisper_model = None


# ===============================
# SPEAK
# ===============================

def speak(text):
    if not text:
        return

    print("JARVIS:", text)

    try:
        engine.stop()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("TTS error:", e)


# ===============================
# RECORD AUDIO
# ===============================

def record_audio():
    print("Listening...")

    try:
        recording = sd.rec(
            int(RECORD_DURATION * DEVICE_SAMPLERATE),
            samplerate=DEVICE_SAMPLERATE,
            channels=1,
            dtype="int16"
        )
        sd.wait()
    except Exception as e:
        print("Recording error:", e)
        return None

    audio = recording.flatten()

    # Resample to Whisper's 16k
    try:
        num_samples = int(len(audio) * MODEL_SAMPLERATE / DEVICE_SAMPLERATE)
        audio = resample(audio, num_samples).astype(np.int16)
    except Exception as e:
        print("Resample error:", e)
        return None

    return audio


# ===============================
# LISTEN (STT)
# ===============================

def listen():

    if _whisper_model is None:
        print("Whisper model not loaded.")
        return "none"

    audio_data = record_audio()

    if audio_data is None:
        return "none"

    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp_path = tmp.name
            write(tmp_path, MODEL_SAMPLERATE, audio_data)

        result = _whisper_model.transcribe(
            tmp_path,
            language=None,
            fp16=False
        )

        text = result["text"].lower().strip()
        print("USER:", text)

        return text if text else "none"

    except Exception as e:
        print("Whisper error:", e)
        return "none"

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except:
                pass