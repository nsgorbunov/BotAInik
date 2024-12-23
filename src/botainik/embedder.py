from html_parser import ml_handbook, Html_parser
from splitter import Doc_Splitter
import random
import numpy as np
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings
)



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

# load it into Chroma
db = Chroma.from_documents(docs, embedding_function)

query = "Что такое линейная регрессия"
docs = db.similarity_search(query, k=3)

print(docs[:3])