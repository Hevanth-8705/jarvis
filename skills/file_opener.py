# skills/file_opener.py

import os
import subprocess
import webbrowser
import shutil


class FileOpenerSkill:

    def __init__(self):
        # Common app aliases
        self.app_map = {
            "chrome": "chrome",
            "google chrome": "chrome",
            "edge": "msedge",
            "notepad": "notepad",
            "calculator": "calc",
            "paint": "mspaint",
            "cmd": "cmd",
            "powershell": "powershell",
            "whatsapp": "whatsapp"
        }

    def open(self, target):

        target = target.lower().strip()

        # -------------------------
        # 1️⃣ Web URLs
        # -------------------------
        if target.startswith("http") or "www." in target:
            webbrowser.open(target)
            return f"Opening {target}"

        if "youtube" in target:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube"

        if "google" in target:
            webbrowser.open("https://google.com")
            return "Opening Google"

        # -------------------------
        # 2️⃣ Known App Map
        # -------------------------
        if target in self.app_map:
            app_name = self.app_map[target]

            try:
                subprocess.Popen(app_name)
                return f"Opening {target}"
            except Exception:
                pass

        # -------------------------
        # 3️⃣ Try Windows Search
        # -------------------------
        try:
            subprocess.Popen(target)
            return f"Opening {target}"
        except Exception:
            pass

        # -------------------------
        # 4️⃣ Try Full Path
        # -------------------------
        if os.path.exists(target):
            os.startfile(target)
            return f"Opening {target}"

        return "Application or file not found."
