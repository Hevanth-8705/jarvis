from datetime import datetime, timedelta
from core.skill import Skill
from typing import Dict, Callable, List, Any
import pytz


class DateTimeSkill(Skill):

    DEFAULT_TIMEZONE = "Asia/Kolkata"

    @property
    def name(self):
        return "datetime_skill"

    # ======================================
    # TOOL DEFINITIONS
    # ======================================

    def get_tools(self) -> List[Dict[str, Any]]:
        return [{
            "type": "function",
            "function": {
                "name": "get_datetime",
                "description": "Get current date, time, full datetime, weekday, or relative date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["date", "time", "datetime", "weekday", "tomorrow", "yesterday"]
                        },
                        "format_24h": {
                            "type": "boolean",
                            "description": "Return time in 24-hour format"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Timezone (example: Asia/Kolkata, UTC)"
                        }
                    },
                    "required": ["type"]
                }
            }
        }]

    def get_functions(self) -> Dict[str, Callable]:
        return {"get_datetime": self.get_datetime}

    # ======================================
    # MAIN FUNCTION
    # ======================================

    def get_datetime(self, type: str, format_24h: bool = False, timezone: str = None):

        try:
            tz_name = timezone if timezone else self.DEFAULT_TIMEZONE
            tz = pytz.timezone(tz_name)
        except:
            tz = pytz.timezone(self.DEFAULT_TIMEZONE)

        now = datetime.now(tz)

        # ==============================
        # TIME
        # ==============================
        if type == "time":

            if format_24h:
                return now.strftime("Current time is %H:%M")
            else:
                return now.strftime("Current time is %I:%M %p")

        # ==============================
        # DATE
        # ==============================
        if type == "date":
            return now.strftime("Today's date is %d %B %Y")

        # ==============================
        # FULL DATETIME
        # ==============================
        if type == "datetime":
            return now.strftime("It is %I:%M %p on %d %B %Y")

        # ==============================
        # WEEKDAY
        # ==============================
        if type == "weekday":
            return now.strftime("Today is %A")

        # ==============================
        # TOMORROW
        # ==============================
        if type == "tomorrow":
            tomorrow = now + timedelta(days=1)
            return tomorrow.strftime("Tomorrow is %A, %d %B %Y")

        # ==============================
        # YESTERDAY
        # ==============================
        if type == "yesterday":
            yesterday = now - timedelta(days=1)
            return yesterday.strftime("Yesterday was %A, %d %B %Y")

        return "I could not determine the requested date or time."