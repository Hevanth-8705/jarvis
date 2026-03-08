import pywhatkit
from core.skill import Skill

class YouTubeSkill(Skill):

    def can_handle(self, command: str) -> bool:
        return command.startswith("play ")

    def handle(self, command: str) -> str:
        song = command.replace("play ", "").strip()
        pywhatkit.playonyt(song)
        return f"Playing {song} on YouTube"
