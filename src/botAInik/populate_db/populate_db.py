import os
import sys
from botAInik.database import get_vectorstore
from botAInik.populate_db.pdf_loader import load_pdf_text
from botAInik.populate_db.text_splitter import split_text
from docx import Document


def load_txt_text(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_docx_text(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def populate_data(directory: str):
    print("[DEBUG] Connecting to Chroma database...")
    vectorstore = get_vectorstore()
    print("[DEBUG] Successfully connected to Chroma.")

    if not os.path.exists(directory):
        print(f"[ERROR] Directory does not exist: {directory}")
        return

    if not os.path.isdir(directory):
        print(f"[ERROR] Path is not a directory: {directory}")
        return

    file_parsers = {
        ".pdf": load_pdf_text,
        ".txt": load_txt_text,
        ".docx": load_docx_text,
    }

    for root, dirs, files in os.walk(directory):
        print(f"[DEBUG] Scanning directory: {root}")
        for f in files:
            ext = os.path.splitext(f)[-1].lower()
            if ext not in file_parsers:
                print(f"[DEBUG] Skipping unsupported file: {f}")
                continue

            file_path = os.path.join(root, f)
            print(f"[DEBUG] Found supported file: {file_path}")

            try:
                text = file_parsers[ext](file_path)
                print(f"[DEBUG] Successfully extracted text from: {file_path}")
            except Exception as e:
                print(f"[ERROR] Failed to extract text from {file_path}: {e}")
                continue

            try:
                chunks = split_text(text)
                print(f"[DEBUG] Split text into {len(chunks)} chunks for: {file_path}")
            except Exception as e:
                print(f"[ERROR] Failed to split text into chunks for {file_path}: {e}")
                continue

            try:
                metadatas = [{"source": file_path} for _ in chunks]
                vectorstore.add_texts(chunks, metadatas=metadatas)
                print(f"[DEBUG] Indexed {len(chunks)} chunks from {file_path}")
            except Exception as e:
                print(f"[ERROR] Failed to add chunks to Chroma for {file_path}: {e}")
                continue

    try:
        vectorstore.persist()
        print("[DEBUG] Database successfully updated!")
    except Exception as e:
        print(f"[ERROR] Failed to persist data to Chroma: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python populate_db.py <directory>")
        sys.exit(1)
    data_dir = sys.argv[1]
    print(f"[DEBUG] Starting population process for directory: {data_dir}")
    populate_data(data_dir)
