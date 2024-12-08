from database import get_vectorstore
from config import USE_RERANKER

def get_relevant_documents(query: str, k: int = 5):
    vs = get_vectorstore()
    retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": k})
    docs = retriever.get_relevant_documents(query)

    if USE_RERANKER:
        #TODO
        print('No reranker yet')

    return docs
