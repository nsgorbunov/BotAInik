import requests
from config import (
    LLM_PROVIDER,
    GIGACHAT_API_KEY,
    GIGACHAT_API_URL,
    MISTRAL_API_KEY,
)


class GigaChatLLM:
    # заглушка пока что, если вдруг пригодится
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url

    def call(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"prompt": prompt, "max_tokens": 1024}
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get("completion", "").strip()


class MistralLLM:
    def __init__(self, api_key: str, model: str = "mistral-large-latest"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.mistral.ai/v1/chat/completions"

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


def get_llm():
    if LLM_PROVIDER == "gigachat":
        return GigaChatLLM(api_key=GIGACHAT_API_KEY, api_url=GIGACHAT_API_URL)
    elif LLM_PROVIDER == "mistral":
        if not MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY is not set.")
        return MistralLLM(api_key=MISTRAL_API_KEY)
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")
