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
    # Разбиваем построчно
    lines = meta.split("\n")
    pattern = r"^(\d+)\.\s*(.*)$"
    results = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = re.match(pattern, line)
        if match:
            importance = match.group(1)
            bullet_text = match.group(2)
            results.append((importance, bullet_text))

    return results


def ingest_data(excel_path: str = EXCEL_INPUT_PATH, collection_name: str = "bota_inik"):
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    collection = client.get_or_create_collection(collection_name)

    df = pd.read_excel(excel_path)

    counter = 0
    skipped = 0

    for idx, row in df.iterrows():
        text_chunk = str(row["text"])
        meta_str = str(row["meta"]) if not pd.isna(row["meta"]) else ""

        # Парсим опорники
        bullets = parse_bullets(meta_str)

        # Если нет опорников, создаём всё равно запись
        if not bullets:
            try:
                bullet_embedding = encode_text(text_chunk).tolist()  # Преобразование в список
                doc_id = f"doc_{idx}_bullet_0"
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
            except Exception as e:
                print(f"[ERROR] Ошибка при добавлении текста: {e}")
                skipped += 1
        else:
            # У каждого опорника своя запись
            for b_idx, (imp, b_text) in enumerate(bullets):
                try:
                    bullet_embedding = encode_text(b_text).tolist()  # Преобразование в список
                    doc_id = f"doc_{idx}_bullet_{b_idx}"
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
                except Exception as e:
                    print(f"[ERROR] Ошибка при добавлении опорника: {e}")
                    skipped += 1

    print(f"Всего добавлено {counter} строк из Excel в Chroma ({collection_name}).")
    print(f"Пропущено строк из-за ошибок: {skipped}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest data from Excel to Chroma.")
    parser.add_argument("--excel", type=str, default=EXCEL_INPUT_PATH, help="Path to Excel file.")
    parser.add_argument("--collection", type=str, default="bota_inik", help="Collection name.")
    args = parser.parse_args()

    ingest_data(args.excel, args.collection)
