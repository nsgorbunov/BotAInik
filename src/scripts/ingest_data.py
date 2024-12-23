import re
import pandas as pd
import chromadb
from src.rag_pipeline.encoder import encode_text
from src.config import EXCEL_INPUT_PATH, CHROMA_DB_DIR


def parse_bullets(meta: str):
    """
    Ищем строки вида:
        1. какая-то фраза
        2. другая фраза
    Возвращаем список кортежей (importance, text).
    """
    lines = meta.split("\n")
    pattern = r"^(\d+)[\.\-)]\s*(.*)$"
    results = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = re.match(pattern, line)
        if match:
            try:
                importance = int(match.group(1))
                bullet_text = match.group(2)
                results.append((importance, bullet_text))
            except ValueError:
                print(f"[ERROR] Некорректное значение importance: '{match.group(1)}' в строке '{line}'")
        else:
            print(f"[DEBUG] Строка не соответствует шаблону: '{line}'")

    return results


def ingest_data(
        csv_path: str = EXCEL_INPUT_PATH,
        collection_name: str = "bota_inik",
        supporting_phrases_column: str = "supporting_phrases"
):
    """
    Ингестит данные из CSV-файла в ChromaDB.

    :param csv_path: Путь к входному CSV-файлу.
    :param collection_name: Название коллекции в ChromaDB.
    :param supporting_phrases_column: Название столбца с опорниками.
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    collection = client.get_or_create_collection(collection_name)

    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        print(f"[INFO] Успешно прочитан CSV-файл: {csv_path}")
    except Exception as e:
        print(f"[ERROR] Не удалось прочитать CSV-файл {csv_path}: {e}")
        return

    print(f"[DEBUG] Столбцы CSV: {df.columns.tolist()}")
    print(f"[DEBUG] Первые 5 строк CSV:\n{df.head()}")

    if "text" not in df.columns:
        raise ValueError("Входной CSV-файл должен содержать столбец 'text'.")

    if supporting_phrases_column not in df.columns:
        print(
            f"[WARNING] Входной CSV-файл не содержит столбца '{supporting_phrases_column}'. Все документы будут добавлены без опорников.")

    counter = 0
    skipped = 0

    for idx, row in df.iterrows():
        text_chunk = str(row["text"])
        meta_str = str(row[supporting_phrases_column]) if supporting_phrases_column in row and not pd.isna(
            row[supporting_phrases_column]) else ""

        # Логирование содержимого meta_str для отладки
        print(f"[DEBUG] Обработка документа {idx}: meta_str='{meta_str}'")

        # парсим опорники
        bullets = parse_bullets(meta_str)

        # логирование результата парсинга
        print(f"[DEBUG] Найдено опорников: {len(bullets)} для документа {idx}")

        if not bullets:
            try:
                bullet_embedding = encode_text(text_chunk).tolist()  # Преобразование в список
                doc_id = f"doc_{idx}_bullet_0"

                # проверка на существование doc_id
                existing_ids = set(collection.get(ids=[doc_id])['ids'])
                if doc_id in existing_ids:
                    print(f"[WARNING] Документ с ID {doc_id} уже существует. Пропуск.")
                    skipped += 1
                    continue

                collection.add(
                    embeddings=[bullet_embedding],
                    documents=[text_chunk],
                    metadatas=[{
                        "chunk_text": text_chunk,
                        "bullet_importance": 1,
                        "bullet_text": text_chunk
                    }],
                    ids=[doc_id]
                )
                counter += 1
                print(f"[INFO] Добавлен документ без опорников: {doc_id}")
            except Exception as e:
                print(f"[ERROR] Ошибка при добавлении текста: {e}")
                skipped += 1
        else:
            # у каждого опорника своя запись
            for b_idx, (imp, b_text) in enumerate(bullets):
                try:
                    bullet_embedding = encode_text(b_text).tolist()  # Преобразование в список
                    doc_id = f"doc_{idx}_bullet_{b_idx}"

                    # проверка на существование doc_id
                    existing_ids = set(collection.get(ids=[doc_id])['ids'])
                    if doc_id in existing_ids:
                        print(f"[WARNING] Документ с ID {doc_id} уже существует. Пропуск.")
                        skipped += 1
                        continue

                    collection.add(
                        embeddings=[bullet_embedding],
                        documents=[b_text],
                        metadatas=[{
                            "chunk_text": text_chunk,
                            "bullet_importance": int(imp),
                            "bullet_text": b_text
                        }],
                        ids=[doc_id]
                    )
                    counter += 1
                    print(f"[INFO] Добавлен опорник: {doc_id} с важностью {imp}")
                except Exception as e:
                    print(f"[ERROR] Ошибка при добавлении опорника: {e}")
                    skipped += 1

    print(f"Всего добавлено {counter} строк из CSV в ChromaDB ({collection_name}).")
    print(f"Пропущено строк из-за ошибок или дубликатов: {skipped}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest data from CSV to ChromaDB.")
    parser.add_argument("--csv", type=str, default=EXCEL_INPUT_PATH, help="Path to CSV file.")
    parser.add_argument("--collection", type=str, default="bota_inik", help="Collection name.")
    parser.add_argument("--supporting_phrases_column", type=str, default="supporting_phrases",
                        help="Name of the column containing supporting phrases.")
    args = parser.parse_args()

    ingest_data(args.csv, args.collection, args.supporting_phrases_column)
