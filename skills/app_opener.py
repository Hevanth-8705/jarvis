import subprocess
import os
import webbrowser
import shutil
from core.skill import Skill
from typing import List, Dict, Any, Callable


class AppOpener(Skill):

    # ===============================
    # APP ALIAS MAP (Windows Focused)
    # ===============================

    APP_ALIASES = {
        "chrome": "chrome.exe",
        "google chrome": "chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
        "spotify": "spotify.exe",
        "vlc": "vlc.exe",
        "edge": "msedge.exe",
        "microsoft edge": "msedge.exe"
    }

    SAFE_BLOCKED = [
        "format",
        "regedit",
        "taskkill /f"
    ]

    @property
    def name(self) -> str:
        return "app_opener"

    # ===============================
    # TOOL DEFINITION (LLM FUNCTION)
    # ===============================

    def get_tools(self) -> List[Dict[str, Any]]:
        return [{
            "type": "function",
            "function": {
                "name": "open_application",
                "description": "Open any installed Windows application or website",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {
                            "type": "string",
                            "description": "Application name or website URL"
                        }
                    },
                    "required": ["app_name"]
                }
            }
        }]

    def get_functions(self) -> Dict[str, Callable]:
        return {"open_application": self.open_application}

    # ===============================
    # MAIN EXECUTION
    # ===============================

    def open_application(self, app_name: str):

        app_name = app_name.lower().strip()

        # 🔒 Safety Filter
        for blocked in self.SAFE_BLOCKED:
            if blocked in app_name:
                return "This command is restricted for safety."

        # 🌐 Website Detection
        if "." in app_name and " " not in app_name:
            try:
                webbrowser.open(app_name)
                return f"Opening website {app_name}"
            except Exception as e:
                return f"Failed to open website: {str(e)}"

        # 🔄 Normalize alias
        executable = self.APP_ALIASES.get(app_name, app_name)

        # ✅ Check if executable exists in PATH
        path = shutil.which(executable)

        if path:
            try:
                subprocess.Popen(path)
                return f"Opening {app_name}"
            except Exception as e:
                return f"Failed to open {app_name}: {str(e)}"

        # 🚀 Try direct open (fallback)
        try:
            subprocess.Popen(executable)
            return f"Opening {app_name}"
        except Exception:
            return f"I could not find {app_name} on this system."