import chromadb
from src.rag_pipeline.encoder import encode_text
from src.config import CHROMA_DB_DIR


class ChromaRetriever:
    def __init__(self, collection_name: str = "bota_inik"):
        self.client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection = self.client.get_or_create_collection(collection_name)

    def similarity_search(self, query: str, top_k: int = 3):
        """
        Ищем наиболее релевантные документы по косинусной близости с учётом важности.
        Более низкое значение 'importance' увеличивает итоговый скор.

        Args:
            query (str): Запрос для поиска.
            top_k (int): Количество топовых результатов для возврата.

        Returns:
            List[Tuple[str, dict, float]]: Список кортежей (doc_id, metadata, custom_score).
        """
        query_embedding = encode_text(query).tolist()  # Преобразуем в список

        # ищем в Chroma
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=10,  # Берём чуть побольше, потом досортируем вручную
        )

        # results – это словарь, содержащий 'ids', 'distances' и 'metadatas'
        scored_results = []
        for doc_id, dist, metadata in zip(results["ids"][0], results["distances"][0], results["metadatas"][0]):
            # Chroma хранит distance = cosine distance
            similarity = 1.0 - dist
            importance = float(metadata.get("bullet_importance", 1.0))

            # обеспечиваем, что importance не меньше 1, чтобы избежать деления на ноль или отрицательных значений
            importance = max(1.0, importance)

            # Учитываем важность: чем ниже, тем лучше
            custom_score = similarity + (0.1 / importance)
            scored_results.append((doc_id, metadata, custom_score))

        # сортируем по custom_score убыванию
        scored_results.sort(key=lambda x: x[2], reverse=True)
        # беремм top_k
        top_scored = scored_results[:top_k]

        return top_scored
