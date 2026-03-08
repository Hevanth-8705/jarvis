import json
import os
from datetime import datetime


class Memory:

    def __init__(self, file="memory.json"):
        self.file = file
        self._initialize_file()

    # ==========================================
    # INITIALIZE STRUCTURED MEMORY
    # ==========================================

    def _initialize_file(self):
        if not os.path.exists(self.file):
            base_structure = {
                "profile": {},
                "data": {},
                "history": []
            }
            self._write(base_structure)

    # ==========================================
    # GENERIC SAVE / GET (Backward Compatible)
    # ==========================================

    def save(self, key, value):
        data = self._load()
        data["data"][key] = value
        self._write(data)

    def get(self, key):
        return self._load()["data"].get(key, None)

    # ==========================================
    # PROFILE STORAGE
    # ==========================================

    def save_profile(self, key, value):
        data = self._load()
        data["profile"][key] = value
        self._write(data)

    def get_profile(self, key):
        return self._load()["profile"].get(key, None)

    # ==========================================
    # CONVERSATION HISTORY
    # ==========================================

    def add_history(self, user_text, assistant_text):
        data = self._load()

        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_text,
            "assistant": assistant_text
        }

        data["history"].append(entry)

        # Keep only last 20 interactions
        if len(data["history"]) > 20:
            data["history"] = data["history"][-20:]

        self._write(data)

    def get_history(self):
        return self._load()["history"]

    def clear_history(self):
        data = self._load()
        data["history"] = []
        self._write(data)

    # ==========================================
    # SAFE LOAD / WRITE
    # ==========================================

    def _load(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            # If corrupted, reset safely
            base_structure = {
                "profile": {},
                "data": {},
                "history": []
            }
            self._write(base_structure)
            return base_structure

    def _write(self, data):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)