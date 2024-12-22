import requests
import openai
from src.config import OPENAI_API_KEY, MISTRAL_API_KEY, LLM_TYPE
from langsmith import traceable

class MistralLLM:
    def __init__(self, api_key: str, model: str = "mistral-large-latest"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.mistral.ai/v1/chat/completions"

    @traceable
    def call(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()


class ChatGPTLLM:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model

    def call(self, prompt: str) -> str:
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return resp.choices[0].message.content.strip()


def get_llm():
    """Возвращает выбранную LLM в соответствии с configом"""
    if LLM_TYPE == "mistral":
        return MistralLLM(MISTRAL_API_KEY)
    else:
        return ChatGPTLLM(OPENAI_API_KEY)
