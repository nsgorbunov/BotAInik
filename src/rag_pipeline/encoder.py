from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL

_encoder = SentenceTransformer(EMBEDDING_MODEL)

def encode_text(text: str):
    """Возвращает эмдеддинг"""
    return _encoder.encode(text, show_progress_bar=False)
