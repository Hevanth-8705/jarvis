import threading
import time
from datetime import datetime
from core.skill import Skill
from typing import List, Dict, Any, Callable

class ReminderSkill(Skill):

    @property
    def name(self):
        return "reminder_skill"

    def get_tools(self):
        return [{
            "type": "function",
            "function": {
                "name": "set_reminder",
                "description": "Set reminder at HH:MM (24-hour)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "time": {"type": "string"},
                        "message": {"type": "string"}
                    },
                    "required": ["time", "message"]
                }
            }
        }]

    def get_functions(self):
        return {"set_reminder": self.set_reminder}

    def set_reminder(self, time_str: str, message: str):
        thread = threading.Thread(
            target=self._wait_and_notify,
            args=(time_str, message),
            daemon=True
        )
        thread.start()
        return f"Reminder set for {time_str}"

    def _wait_and_notify(self, time_str, message):
        try:
            target = datetime.strptime(time_str, "%H:%M")
            while True:
                now = datetime.now()
                if now.hour == target.hour and now.minute == target.minute:
                    print(f"Reminder: {message}")
                    break
                time.sleep(30)
        except:
            pass
