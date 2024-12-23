from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader


class PDFParser:
    def PdfParser(self, path: str) -> Document:
        loader = PyPDFLoader(path)
        pages = loader.load_and_split()

        return pages
