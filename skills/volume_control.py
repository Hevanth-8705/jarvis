from core.skill import Skill
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeControl(Skill):

    def can_handle(self, command: str) -> bool:
        return "volume" in command

    def handle(self, command: str) -> str:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        if "up" in command:
            volume.SetMasterVolumeLevelScalar(1.0, None)
            return "Volume increased"

        if "down" in command:
            volume.SetMasterVolumeLevelScalar(0.2, None)
            return "Volume decreased"

        return "Specify volume up or down."
