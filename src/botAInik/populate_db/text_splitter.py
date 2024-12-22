def split_text(text: str, chunk_size: int = 50, chunk_overlap: int = 10):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start = end - chunk_overlap if (end - chunk_overlap) > start else end
    return chunks
