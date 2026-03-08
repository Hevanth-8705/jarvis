class ContextManager:

    def __init__(self):
        self.last_intent = None
        self.last_contacts = None
        self.last_message = None

    def update(self, intent, entity):

        self.last_intent = intent

        if intent == "whatsapp_send" and entity:
            if entity.get("names"):
                self.last_contacts = entity["names"]

            if entity.get("message"):
                self.last_message = entity["message"]

    def resolve_pronoun(self, text):

        pronouns = ["him", "her", "them", "that person"]

        if any(p in text.lower() for p in pronouns):
            return self.last_contacts

        return None

    def extend_message(self, extra_text):

        if self.last_message:
            self.last_message += " " + extra_text
            return self.last_message

        return None

    def clear(self):
        self.last_intent = None
        self.last_contacts = None
        self.last_message = None