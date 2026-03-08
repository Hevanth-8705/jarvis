import json
from core.engine import JarvisEngine


class CommandEngine:

    def __init__(self):
        self.ai = JarvisEngine()

    def interpret(self, user_input: str):

        prompt = f"""
You are a desktop AI command parser.

Classify the user input into one of these actions:
- open_app
- close_app
- search_web
- system_control
- chat

If action is open_app or close_app, extract the app name.
If search_web, extract search query.
If system_control, specify action (shutdown, restart, lock, volume_up, volume_down, mute).
If chat, return chat.

Return JSON only:
{{
  "action": "...",
  "target": "...",
  "confidence": 0.0
}}

User input:
"{user_input}"
"""

        response = self.ai.run_conversation(prompt)

        try:
            return json.loads(response)
        except:
            return {
                "action": "chat",
                "target": user_input,
                "confidence": 0.3
            }