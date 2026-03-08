# core/automation.py

import os
import subprocess
import pyautogui
import webbrowser
import psutil
import platform


class Automation:

    def __init__(self):

        # Smart app mapping
        self.app_map = {
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "cmd": "cmd.exe",
            "explorer": "explorer.exe",
            "spotify": "spotify.exe"
        }

    # ============================
    # APPLICATION CONTROL
    # ============================

    def open_app(self, name):
        name = name.lower().strip()

        try:
            if name in self.app_map:
                subprocess.Popen(self.app_map[name])
            else:
                subprocess.Popen(name)

            return f"Opening {name}"

        except Exception as e:
            return f"Failed to open {name}"

    def close_app(self, name):
        try:
            subprocess.call(f"taskkill /f /im {name}.exe", shell=True)
            return f"Closed {name}"
        except:
            return f"Could not close {name}"

    # ============================
    # BROWSER
    # ============================

    def open_website(self, url):
        if not url.startswith("http"):
            url = "https://" + url

        webbrowser.open(url)
        return f"Opening {url}"

    def google_search(self, query):
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Searching for {query}"

    # ============================
    # KEYBOARD / MOUSE
    # ============================

    def type_text(self, text):
        pyautogui.write(text)
        return "Typing text"

    def press_key(self, key):
        pyautogui.press(key)
        return f"Pressed {key}"

    def hotkey(self, *keys):
        pyautogui.hotkey(*keys)
        return "Hotkey executed"

    def scroll(self, amount):
        pyautogui.scroll(amount)
        return "Scrolling"

    # ============================
    # WINDOW CONTROL
    # ============================

    def minimize(self):
        pyautogui.hotkey("win", "down")
        return "Minimizing window"

    def maximize(self):
        pyautogui.hotkey("win", "up")
        return "Maximizing window"

    def close_current(self):
        pyautogui.hotkey("alt", "f4")
        return "Closing current window"

    # ============================
    # SYSTEM CONTROL
    # ============================

    def shutdown(self):
        os.system("shutdown /s /t 5")
        return "Shutting down system"

    def restart(self):
        os.system("shutdown /r /t 5")
        return "Restarting system"

    def lock(self):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Locking system"

    # ============================
    # SYSTEM STATUS
    # ============================

    def cpu_usage(self):
        return f"CPU usage is {psutil.cpu_percent()} percent"

    def ram_usage(self):
        return f"RAM usage is {psutil.virtual_memory().percent} percent"

    def system_info(self):
        return f"You are running {platform.system()}"