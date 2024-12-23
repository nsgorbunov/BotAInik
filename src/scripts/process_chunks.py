import pandas as pd
from src.rag_pipeline.llms import MistralLLM
from src.config import MISTRAL_API_KEY
import argparse

def get_llm():
    """
    Инициализирует LLM (только Mistral).
    """
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY не установлен в конфигурации.")
    return MistralLLM(api_key=MISTRAL_API_KEY)

def generate_supporting_phrases(llm, chunk: str) -> str:
    """
    Генерирует опорные фразы для переданного чанка с помощью LLM.
    """
    prompt = (
        f"Прочитай следующий текст и сгенерируй 3-5 коротких опорных фраз или вопросов, связанных с этим текстом. "
        f"Фразы должны быть релевантны теме текста, упорядочены по убыванию важности, пронумерованы и заканчиваться точкой или вопросительным знаком.\n"
        f"Это должен быть список в виде:\n"
        f"1. Самая важная опорная фраза (т.е. текст по большей части об этом)\n"
        f"2. Менее важная фраза... и так далее\n"
        f"Текст: \"{chunk}\""
    )
    try:
        response = llm.call(prompt)
        return response
    except Exception as e:
        print(f"[ERROR] Не удалось сгенерировать опорные фразы для чанка: {e}")
        return ""

def process_chunks(input_file: str, output_file: str):
    """
    Читает файл с текстами, генерирует опорные фразы с помощью LLM и сохраняет результат в новый CSV-файл.
    """
    print("[INFO] Инициализация LLM...")
    llm = get_llm()
    print("[INFO] Успешно инициализирован LLM!")

    # читаем файл с текстами
    print(f"[INFO] Чтение входного файла: {input_file}")
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
    except Exception as e:
        print(f"[ERROR] Не удалось прочитать входной файл {input_file}: {e}")
        return

    if "text" not in df.columns:
        raise ValueError("Входной файл должен содержать столбец 'text'.")

    # генерируем опорные фразы для каждого текста
    supporting_phrases = []
    total_chunks = len(df)
    for idx, chunk in enumerate(df["text"], start=1):
        print(f"[INFO] Обработка текста {idx}/{total_chunks}...")
        phrases = generate_supporting_phrases(llm, chunk)
        print(f"[DEBUG] Сгенерированные опорные фразы: {phrases}")
        supporting_phrases.append(phrases)

    # добавляем результаты в DataFrame
    df["supporting_phrases"] = supporting_phrases

    # сохраняем результат в новый CSV-файл
    try:
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"[INFO] Результаты успешно сохранены в файл: {output_file}")
    except Exception as e:
        print(f"[ERROR] Не удалось сохранить файл: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Генерация опорных фраз для текстов из CSV-файла.")
    parser.add_argument("--input", type=str, required=True, help="Путь к входному CSV-файлу с текстами.")
    parser.add_argument("--output", type=str, required=True, help="Путь для сохранения результата с опорными фразами в CSV-файл.")
    args = parser.parse_args()

    process_chunks(args.input, args.output)
