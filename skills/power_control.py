import os
from core.skill import Skill
from typing import List, Dict, Any, Callable

class PowerControl(Skill):

    @property
    def name(self):
        return "power_control"

    def get_tools(self):
        return [{
            "type": "function",
            "function": {
                "name": "power_action",
                "description": "Shutdown or restart system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["shutdown", "restart"]
                        }
                    },
                    "required": ["action"]
                }
            }
        }]

    def get_functions(self):
        return {"power_action": self.power_action}

    def power_action(self, action: str):
        if action == "shutdown":
            os.system("shutdown /s /t 5")
            return "Shutting down"
        elif action == "restart":
            os.system("shutdown /r /t 5")
            return "Restarting"
        return "Invalid action"
