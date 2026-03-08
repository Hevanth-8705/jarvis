import webbrowser
from core.skill import Skill
from typing import List, Dict, Any, Callable

class GoogleSearch(Skill):

    @property
    def name(self) -> str:
        return "google_search"

    def get_tools(self) -> List[Dict[str, Any]]:
        return [{
            "type": "function",
            "function": {
                "name": "google_search",
                "description": "Search anything on Google",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"}
                    },
                    "required": ["query"]
                }
            }
        }]

    def get_functions(self) -> Dict[str, Callable]:
        return {"google_search": self.google_search}

    def google_search(self, query: str):
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching Google for {query}"
