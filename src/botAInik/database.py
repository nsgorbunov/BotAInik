from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from config import CHROMA_DB_DIR

def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
    print(f"[DEBUG] Number of documents in Chroma: {vectorstore._collection.count()}")
    return vectorstore
