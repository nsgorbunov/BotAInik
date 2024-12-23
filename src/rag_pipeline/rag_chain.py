from langsmith import traceable
from src.rag_pipeline.llms import MistralLLM
from src.rag_pipeline.retriever import ChromaRetriever
from src.config import MISTRAL_API_KEY


class RAGChain:
    def __init__(self):
        self.llm = MistralLLM(api_key=MISTRAL_API_KEY)
        self.retriever = ChromaRetriever()

    @traceable
    def run(self, query: str) -> str:
        # ищем релевантные чанки
        results = self.retriever.similarity_search(query, top_k=3)

        # составляем контекст из базы знаний
        context_chunks = [
            metadata.get("chunk_text", "") for _, metadata, _ in results
        ]
        context = "\n\n".join(context_chunks)

        # генерируем запрос к LLM
        prompt = (f""
                  f"Ты - помощник в подготовке к собеседованиям. "
                  f"Ты должен отвечать на вопрос пользователя. "
                  f"Вот информация из базы знаний, который поможет тебе ответить:\n{context}\n"
                  f"\nQuestion: {query}. Ответь кратко, без разбиения текста на пунты, выделений жирным шрифтом. "
                  f"Если нужно, пиши формулы. "
                  f"В формулах используй форматирование.")
        print(prompt)
        answer = self.llm.call(prompt)

        return answer

    def validate(self, query: str) -> str:
        # ищем релевантные чанки
        results = self.retriever.similarity_search(query, top_k=3)

        # составляем контекст из базы знаний
        context_chunks = [
            metadata.get("chunk_text", "") for _, metadata, _ in results
        ]
        context = "\n\n".join(context_chunks)
        context_to_validate = [str(chunk) for chunk in context_chunks]

        # генерируем запрос к LLM
        prompt = (f""
                  f"Ты - помощник в подготовке к собеседованиям. "
                  f"Ты должен отвечать на вопрос пользователя. "
                  f"Вот информация из базы знаний, который поможет тебе ответить:\n{context}\n"
                  f"\nQuestion: {query}. Ответь кратко, без разбиения текста на пунты, выделений жирным шрифтом. "
                  f"Если нужно, пиши формулы. "
                  f"В формулах используй форматирование.")
        answer = self.llm.call(prompt)

        return {
            "answer": answer,
            "contexts": context_to_validate,
        }