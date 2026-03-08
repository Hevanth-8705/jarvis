import requests
from core.skill import Skill
from typing import List, Dict, Any, Callable

API_KEY = "YOUR_OPENWEATHER_API_KEY"

class WeatherSkill(Skill):

    @property
    def name(self) -> str:
        return "weather_skill"

    def get_tools(self):
        return [{
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather of a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"}
                    },
                    "required": ["city"]
                }
            }
        }]

    def get_functions(self):
        return {"get_weather": self.get_weather}

    def get_weather(self, city: str):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            data = requests.get(url).json()

            if "main" in data:
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                return f"{city}: {temp}°C, {desc}"
            return "Weather not available."
        except Exception as e:
            return f"Weather error: {str(e)}"
