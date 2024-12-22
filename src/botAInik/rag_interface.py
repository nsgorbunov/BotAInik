from retriever import get_relevant_documents
from model_api import get_llm


def answer_question(question: str) -> str:
    llm = get_llm()

    docs = get_relevant_documents(question)
    context_text = "\n\n".join([doc.page_content for doc in docs])

    print("\n[DEBUG] Контекст, который достали:\n")
    print(context_text)
    print("\n[END OF CONTEXT]\n")

    prompt = (f"Сейчас я покажу тебе информацию из базы знаний. Используй информацию оттуда для ответа на вопрос. "
              f"Информация из базы знаний:\n\n{context_text}\n\nВопрос: {question}")

    answer = llm.call(prompt)
    return answer.strip()
