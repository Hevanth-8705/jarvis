# core/intent_router.py

import re


class IntentRouter:

    def route(self, text: str):

        text = text.lower().strip()

        # =========================
        # CONFIRMATION (FIRST)
        # =========================

        if text in ["yes", "confirm", "send it", "haan", "avunu"]:
            return {"intent": "confirm_send", "entity": None}

        if text in ["no", "cancel", "stop", "vaddu"]:
            return {"intent": "cancel_send", "entity": None}

        # =========================
        # SCREENSHOT
        # =========================

        if "screenshot" in text or "capture screen" in text or "take screenshot" in text:
            return {"intent": "screenshot", "entity": None}

        # =========================
        # ADD CONTACT (ENGLISH)
        # =========================

        add_contact_match = re.search(
            r"add contact (.+?) number (\d+)",
            text
        )

        if add_contact_match:
            return {
                "intent": "add_contact",
                "entity": {
                    "name": add_contact_match.group(1).strip(),
                    "number": add_contact_match.group(2).strip()
                }
            }

        # =========================
        # ADD CONTACT (TELUGU MIXED)
        # =========================

        telugu_add_match = re.search(
            r"(.+?) number (\d+) add chey",
            text
        )

        if telugu_add_match:
            return {
                "intent": "add_contact",
                "entity": {
                    "name": telugu_add_match.group(1).strip(),
                    "number": telugu_add_match.group(2).strip()
                }
            }

        # =========================
        # SYSTEM AUDIO
        # =========================

        if "volume up" in text or "increase volume" in text:
            return {"intent": "volume_up", "entity": None}

        if "volume down" in text or "decrease volume" in text:
            return {"intent": "volume_down", "entity": None}

        if "mute" in text:
            return {"intent": "mute", "entity": None}

        # =========================
        # BASIC SYSTEM COMMANDS
        # =========================

        if "shutdown" in text:
            return {"intent": "shutdown", "entity": None}

        if "restart" in text:
            return {"intent": "restart", "entity": None}

        if "time" in text:
            return {"intent": "time", "entity": None}

        if "cpu" in text:
            return {"intent": "cpu", "entity": None}

        if "ram" in text:
            return {"intent": "ram", "entity": None}

        # =========================
        # OPEN / CLOSE APPS
        # =========================

        open_match = re.search(r"\bopen\s+(.+)", text)
        if open_match:
            app = open_match.group(1).strip()

            if "whatsapp" in app:
                return {"intent": "open_whatsapp", "entity": None}

            return {"intent": "open", "entity": app}

        close_match = re.search(r"\bclose\s+(.+)", text)
        if close_match:
            return {"intent": "close", "entity": close_match.group(1).strip()}

        # =========================
        # WHATSAPP CALL (LOOSE)
        # =========================

        if "call" in text and "whatsapp" in text:
            name = text.replace("call", "").replace("on whatsapp", "").replace("whatsapp", "").strip()
            return {
                "intent": "whatsapp_call",
                "entity": name
            }

        # =========================
        # WHATSAPP SCHEDULED MESSAGE
        # =========================

        schedule_match = re.search(
            r"send message to (.+?) at (.+?) saying (.+)",
            text
        )

        if schedule_match:
            names_part = schedule_match.group(1)
            time_part = schedule_match.group(2)
            message_part = schedule_match.group(3)

            names = re.split(r",| and ", names_part)

            return {
                "intent": "whatsapp_send",
                "entity": {
                    "names": [n.strip() for n in names],
                    "message": message_part.strip(),
                    "schedule": time_part.strip()
                }
            }

        # =========================
        # WHATSAPP SEND WITH MESSAGE
        # =========================

        send_match = re.search(
            r"send message to (.+?) saying (.+)",
            text
        )

        if send_match:
            names_part = send_match.group(1)
            message_part = send_match.group(2)

            names = re.split(r",| and ", names_part)

            return {
                "intent": "whatsapp_send",
                "entity": {
                    "names": [n.strip() for n in names],
                    "message": message_part.strip(),
                    "schedule": None
                }
            }

        # =========================
        # WHATSAPP SEND WITHOUT MESSAGE
        # Example: send message to daddy in whatsapp
        # =========================

        loose_whatsapp = re.search(
            r"send message to (.+?)( in whatsapp| on whatsapp| whatsapp|$)",
            text
        )

        if loose_whatsapp:
            names_part = loose_whatsapp.group(1)
            names = re.split(r",| and ", names_part)

            return {
                "intent": "whatsapp_send",
                "entity": {
                    "names": [n.strip() for n in names],
                    "message": None,
                    "schedule": None
                }
            }

        # =========================
        # TELUGU MIXED SEND
        # =========================

        telugu_match = re.search(
            r"(.+?) ki msg chey (.+)",
            text
        )

        if telugu_match:
            name = telugu_match.group(1).strip()
            message = telugu_match.group(2).strip()

            return {
                "intent": "whatsapp_send",
                "entity": {
                    "names": [name],
                    "message": message,
                    "schedule": None
                }
            }

        # =========================
        # DEFAULT CHAT
        # =========================

        return {"intent": "chat", "entity": text}