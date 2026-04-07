import os
import logging
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from embeddings.manager import get_embeddings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(self, index_path: str = "data/faiss_index"):
        self.index_path = index_path
        self.embeddings = get_embeddings()
        self.vector_store = self._load_or_create_index()

    def _load_or_create_index(self):
        """Loads an existing FAISS index or creates a new empty one."""
        if os.path.exists(self.index_path):
            logger.info(f"Loading existing FAISS index from {self.index_path}")
            try:
                return FAISS.load_local(
                    self.index_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True # Required for local loading
                )
            except Exception as e:
                logger.error(f"Error loading FAISS index: {e}")
                return None
        else:
            logger.info("Initializing new FAISS index")
            return None

    def add_documents(self, documents: List[Document]):
        """Adds documents to the FAISS index and saves it."""
        if not documents:
            logger.warning("No documents provided to add to vector store.")
            return

        if self.vector_store is None:
            logger.info("Creating first entries in vector store.")
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            logger.info(f"Adding {len(documents)} documents to existing vector store.")
            self.vector_store.add_documents(documents)
        
        self.save_index()

    def save_index(self):
        """Saves the current vector store to disk."""
        if self.vector_store:
            logger.info(f"Saving FAISS index to {self.index_path}")
            self.vector_store.save_local(self.index_path)

    def get_retriever(self):
        """Returns a retriever object from the vector store."""
        if self.vector_store:
            return self.vector_store.as_retriever(search_kwargs={"k": 5})
        return None
