import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY", "")
GIGACHAT_API_URL = os.getenv("GIGACHAT_API_URL", "")

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL", "")

CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")

USE_RERANKER = os.getenv("USE_RERANKER", "False").lower() in ["true", "1", "yes"]
