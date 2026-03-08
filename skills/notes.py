import json
from core.skill import Skill

class NotesSkill(Skill):

    def can_handle(self, command: str) -> bool:
        return command.startswith("note ")

    def handle(self, command: str) -> str:
        note = command.replace("note ", "").strip()

        with open("memory.json", "r") as f:
            data = json.load(f)

        data.setdefault("notes", []).append(note)

        with open("memory.json", "w") as f:
            json.dump(data, f, indent=4)

        return "Note saved."
