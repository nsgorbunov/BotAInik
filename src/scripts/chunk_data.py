import os
import glob
import math
import pandas as pd
from src.utils.doc_loaders import load_text_from_file
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str, chunk_size: int, chunk_overlap: int):
    """Разбивает текст на чанки по chunk_size слов с перекрытием chunk_overlap"""
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunk_str = " ".join(chunk)
        chunks.append(chunk_str)
        start = end - chunk_overlap

        if start < 0:
            break
    return chunks

def process_folder(folder_path: str, output_excel: str = "data/output.xlsx"):
    all_chunks = []
    processed_files = []
    skipped_chunks = 0
    skipped_files = 0

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith((".pdf", ".txt", ".docx")):
                full_path = os.path.join(root, file_name)
                try:
                    text = load_text_from_file(full_path)
                except Exception as e:
                    print(f"[ERROR] Не удалось загрузить файл {file_name}: {e}")
                    skipped_files += 1
                    continue

                try:
                    chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
                    for idx, chunk in enumerate(chunks):
                        meta = f"{file_name} | chunk_{idx}"
                        all_chunks.append({"text": chunk, "meta": meta})
                    processed_files.append(file_name)
                except Exception as e:
                    print(f"[WARNING] Пропущен чанк из файла {file_name} из-за ошибки: {e}")
                    skipped_chunks += 1

    try:
        df = pd.DataFrame(all_chunks)
        df.to_excel(output_excel, index=False, engine="openpyxl")
        print(f"Сохранено в {output_excel}")
    except Exception as e:
        print(f"[ERROR] Не удалось сохранить файл: {e}")

    print(f"Обработанные файлы: {', '.join(processed_files)}")
    print(f"Пропущено чанков из-за ошибок: {skipped_chunks}")
    print(f"Пропущено файлов из-за ошибок загрузки: {skipped_files}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Chunk files from a folder.")
    parser.add_argument("--folder", type=str, required=True, help="Path to the folder with docs.")
    parser.add_argument("--output", type=str, default="data/output.xlsx", help="Excel output file.")
    args = parser.parse_args()

    process_folder(args.folder, args.output)
