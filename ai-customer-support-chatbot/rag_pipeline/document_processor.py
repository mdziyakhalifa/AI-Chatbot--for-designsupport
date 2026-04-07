import logging
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
        )

    def load_pdf(self, file_path: str) -> List[Document]:
        """Loads a PDF file and returns a list of documents."""
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            logger.info(f"Loaded {len(pages)} pages from {file_path}")
            return pages
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {e}")
            return []

    def load_txt(self, file_path: str) -> List[Document]:
        """Loads a text file and returns a list of documents."""
        try:
            loader = TextLoader(file_path)
            docs = loader.load()
            logger.info(f"Loaded content from {file_path}")
            return docs
        except Exception as e:
            logger.error(f"Error loading text file {file_path}: {e}")
            return []

    def load_website(self, url: str) -> List[Document]:
        """Loads content from a website and returns a list of documents."""
        try:
            loader = WebBaseLoader(url)
            docs = loader.load()
            logger.info(f"Loaded content from website: {url}")
            return docs
        except Exception as e:
            logger.error(f"Error loading website {url}: {e}")
            return []

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Splits documents into smaller chunks."""
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")
        return chunks

    def process_file(self, file_path: str) -> List[Document]:
        """Processes a single file based on its extension."""
        if file_path.endswith('.pdf'):
            docs = self.load_pdf(file_path)
        elif file_path.endswith('.txt'):
            docs = self.load_txt(file_path)
        else:
            logger.warning(f"Unsupported file format: {file_path}")
            return []
        
        return self.split_documents(docs)

    def process_url(self, url: str) -> List[Document]:
        """Processes a website URL."""
        docs = self.load_website(url)
        return self.split_documents(docs)
