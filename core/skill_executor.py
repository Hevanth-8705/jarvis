import os
import subprocess
import webbrowser
import datetime
import psutil
import re
import difflib
import urllib.parse
from pathlib import Path

from core.memory_store import MemoryStore


class SkillExecutor:

    def __init__(self):

        self.start_menu_paths = [
            Path(os.getenv("APPDATA")) / r"Microsoft\Windows\Start Menu\Programs",
            Path(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs")
        ]

        self.program_paths = [
            Path("C:/Program Files"),
            Path("C:/Program Files (x86)")
        ]

        self.app_index = self.build_app_index()

        # 🔥 Persistent Memory
        self.memory = MemoryStore()

    # ==================================
    # BUILD APP INDEX
    # ==================================

    def build_app_index(self):
        index = {}
        for path in self.start_menu_paths:
            if path.exists():
                for file in path.rglob("*.lnk"):
                    index[file.stem.lower()] = str(file)
        return index

    # ==================================
    # MAIN EXECUTION
    # ==================================

    def execute(self, intent_data):

        intent = intent_data.get("intent")
        entity = intent_data.get("entity")

        # Track usage
        if entity:
            self.memory.track_command(str(entity))

        # ===========================
        # CONTACT MANAGEMENT
        # ===========================

        if intent == "add_contact":
            name = entity.get("name")
            number = entity.get("number")
            self.memory.add_contact(name, number)
            return f"Contact {name} saved successfully."

        # ===========================
        # WHATSAPP FEATURES
        # ===========================

        if intent == "open_whatsapp":
            webbrowser.open("https://web.whatsapp.com")
            return "Opening WhatsApp."

        if intent == "whatsapp_call":
            return self.call_whatsapp(entity)

        if intent == "whatsapp_send":
            prepared, error = self.prepare_whatsapp_message(entity)
            if error:
                return error
            return prepared  # confirmation handled in main.py

        # ===========================
        # SYSTEM FEATURES
        # ===========================

        if intent == "open" and entity:
            return self.open_application(entity)

        if intent == "close" and entity:
            return self.close_application(entity)

        if intent == "time":
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"The time is {now}."

        if intent == "cpu":
            return f"CPU usage is {psutil.cpu_percent()} percent."

        if intent == "ram":
            return f"RAM usage is {psutil.virtual_memory().percent} percent."

        if intent == "battery":
            battery = psutil.sensors_battery()
            if battery:
                return f"Battery at {battery.percent} percent."
            return "Battery information not available."

        if intent == "shutdown":
            os.system("shutdown /s /t 10")
            return "System will shut down in 10 seconds."

        if intent == "restart":
            os.system("shutdown /r /t 10")
            return "System will restart in 10 seconds."

        if intent == "lock":
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "Locking system."

        if intent == "volume_up":
            os.system("nircmd.exe changesysvolume 5000")
            return "Increasing volume."

        if intent == "volume_down":
            os.system("nircmd.exe changesysvolume -5000")
            return "Decreasing volume."

        if intent == "mute":
            os.system("nircmd.exe mutesysvolume 1")
            return "System muted."

        return None

    # ==================================
    # WHATSAPP PREPARATION
    # ==================================

    def prepare_whatsapp_message(self, data):

        if not data:
            return None, "Invalid message format."

        names = data.get("names", [])
        message = data.get("message")
        schedule = data.get("schedule")

        if not message:
            return None, "Message cannot be empty."

        valid_contacts = []

        all_contacts = self.memory.get_all_contacts()

        for name in names:
            clean_name = name.lower().strip()
            if clean_name in all_contacts:
                valid_contacts.append((clean_name, all_contacts[clean_name]))

        if not valid_contacts:
            return None, "No valid contacts found."

        return {
            "type": "whatsapp_prepared",
            "contacts": valid_contacts,
            "message": message,
            "schedule": schedule
        }, None

    # ==================================
    # FINAL SEND
    # ==================================

    def send_whatsapp_message(self, prepared_data):

        if not prepared_data:
            return "Nothing to send."

        encoded_message = urllib.parse.quote(prepared_data["message"])

        for name, number in prepared_data["contacts"]:
            url = f"https://wa.me/{number}?text={encoded_message}"
            webbrowser.open(url)

        return "Message ready to send. Please press send in WhatsApp."

    # ==================================
    # WHATSAPP CALL
    # ==================================

    def call_whatsapp(self, name):

        if not name:
            return "Invalid contact."

        clean_name = name.lower().strip()

        number = self.memory.get_contact(clean_name)

        if not number:
            return "Contact not found."

        webbrowser.open(f"https://wa.me/{number}")

        return f"Opening chat with {clean_name}. Press call button."

    # ==================================
    # OPEN APPLICATION
    # ==================================

    def open_application(self, app_name):

        app_name = re.sub(r"[^\w\s\.\\:/-]", "", app_name.lower()).strip()

        if Path(app_name).exists():
            os.startfile(app_name)
            return f"Opening file {app_name}."

        if app_name.startswith("http") or "." in app_name:
            webbrowser.open(app_name if app_name.startswith("http") else f"https://{app_name}")
            return f"Opening {app_name}."

        if app_name in self.app_index:
            subprocess.Popen(self.app_index[app_name], shell=True)
            return f"Opening {app_name}."

        matches = difflib.get_close_matches(app_name, self.app_index.keys(), n=1, cutoff=0.6)
        if matches:
            best = matches[0]
            subprocess.Popen(self.app_index[best], shell=True)
            return f"Opening {best}."

        return f"I could not find {app_name}."

    # ==================================
    # CLOSE APPLICATION
    # ==================================

    def close_application(self, app_name):

        app_name = re.sub(r"[^\w\s]", "", app_name.lower()).strip()
        closed = False

        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and app_name in proc.info['name'].lower():
                    proc.kill()
                    closed = True
            except:
                continue

        return f"Closing {app_name}." if closed else f"{app_name} is not running."