import os
from typing import Literal

import yaml


def load_config(path: str = "config.yaml"):
    """Загружает конфигурацию из YAML-файла."""
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "configs", "config.yaml")
config = load_config(CONFIG_PATH)

LLM_TYPE: Literal["chatgpt", "mistral"] = config.get("llm_type", "mistral")
OPENAI_API_KEY = config.get("openai_api_key", "")
MISTRAL_API_KEY = config.get("mistral_api_key", "")
LANGSMITH_API_KEY = config.get("langsmith_api_key", "")
CHUNK_SIZE = config.get("chunk_size", 300)
CHUNK_OVERLAP = config.get("chunk_overlap", 50)
EXCEL_INPUT_PATH = config.get("excel_input_path", "data/input.xlsx")
CHROMA_DB_DIR = config.get("chroma_db_dir", "chroma_db")
EMBEDDING_MODEL = config.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")
