from langchain_text_splitters import RecursiveCharacterTextSplitter


# spilt text by simple amount of characters or by paragraphs
class Doc_Splitter:
    def __init__(self, docs):
        self.CHUNK_SIZE = 600
        self.CHUNK_OVERLAP = 200
        self.docs = docs

    def simple_splitter(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE,
            chunk_overlap=self.CHUNK_OVERLAP,
        )
        splits = text_splitter.split_documents(self.docs)
        return splits

    def paragraph_splitter(self):
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " "],  # separates either on words or paragraphs
            chunk_size=self.CHUNK_SIZE,
            chunk_overlap=self.CHUNK_OVERLAP,
        )
        splits = splitter.split_documents(self.docs)
        return splits
