# core/engine.py

import os
from groq import Groq


class JarvisEngine:

    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"

    def handle(self, text):

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are Jarvis AI."},
                    {"role": "user", "content": text}
                ],
                max_tokens=200,
                temperature=0.4
            )

            return response.choices[0].message.content.strip()

        except:
            return "I am having trouble processing that."