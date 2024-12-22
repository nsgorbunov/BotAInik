import os
from pypdf import PdfReader
import docx

def load_text_from_file(file_path: str) -> str:
    """Определяет тип файла и загружает текст."""
    if file_path.lower().endswith(".pdf"):
        return load_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return load_text_from_docx(file_path)
    elif file_path.lower().endswith(".txt"):
        return load_text_from_txt(file_path)
    else:
        return ""


def load_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        pdf = PdfReader(pdf_path)
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    except:
        pass
    return text


def load_text_from_docx(docx_path: str) -> str:
    doc = docx.Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


def load_text_from_txt(txt_path: str) -> str:
    with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
