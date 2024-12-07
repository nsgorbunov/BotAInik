import os

from dotenv import load_dotenv
from html_parser import Html_parser, ml_handbook
from icecream import ic
from langchain.chains.question_answering import load_qa_chain
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.retrievers import TFIDFRetriever
from langchain_mistralai.chat_models import ChatMistralAI
from splitter import Doc_Splitter

# Load environment variables
load_dotenv(".env")

api_key = os.environ["API_KEY"]

# certain_pages = random.choices(ml_handbook, k=3)
certain_pages = ml_handbook[:3]

# print(certain_pages)

# Html Parser
docs = Html_parser().web_page(certain_pages)


# Recursive Chunking
rec_splitter = Doc_Splitter(docs)
splits = rec_splitter.paragraph_splitter()


# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="cointegrated/rubert-tiny2")

# SIMPLE RAG
# I - CHROMA
# Chroma справляется плохо
# load it into Chroma
# db = Chroma.from_documents(splits, embedding_function)

query = "Что такое логистическая регрессия"
# docs = db.similarity_search(query, k=2)

# II - TFIDF
# TFIDF норм

retriever = TFIDFRetriever.from_documents(splits)
# result = retriever.invoke(query)


# III - BM25
# from langchain_community.retrievers import BM25Retriever
# bm25_retriever = BM25Retriever.from_documents(splits)
# result = bm25_retriever.invoke(query)

# ADVANCED RAG - LLM MistralAI

llm = ChatMistralAI(
    mistral_api_key=api_key, model="mistral-large-latest", temperature=0, max_retries=2
)

qa_chain = load_qa_chain(llm=llm, chain_type="stuff")
relevant_texts = retriever.get_relevant_documents(query)
initial_answer = qa_chain.run(input_documents=relevant_texts, question=query)


ic(query)
ic(initial_answer)
# ic(result)
# ic(docs)
# print(docs[0].page_content)
# print(docs[1].page_content)
# ic(docs[0].page_content)
# ic(docs[1].page_content)
# print(docs[:3])
