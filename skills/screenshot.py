import pyautogui
from core.skill import Skill

class ScreenshotSkill(Skill):

    def can_handle(self, command: str) -> bool:
        return "screenshot" in command

    def handle(self, command: str) -> str:
        file = "screenshot.png"
        pyautogui.screenshot(file)
        return "Screenshot saved."
