from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class LangChainPlanner:

    def __init__(self):

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3
        )

    def plan(self, prompt: str):

        response = self.llm.invoke(prompt)

        return response.content