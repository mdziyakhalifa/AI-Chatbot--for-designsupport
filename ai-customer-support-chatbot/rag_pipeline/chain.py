import logging
from langchain_community.llms import Ollama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from .vector_store import VectorStoreManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGChain:
    def __init__(self, model_name: str = "llama3"):
        self.llm = Ollama(model=model_name)
        self.vector_store_manager = VectorStoreManager()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True,
            output_key='answer'
        )
        self.chain = self._initialize_chain()

    def _initialize_chain(self):
        """Initializes the conversational retrieval chain."""
        retriever = self.vector_store_manager.get_retriever()
        if retriever is None:
            logger.warning("No retriever available. Run document upload first.")
            return None
        
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True
        )

    def ask(self, question: str):
        """Ask a question to the RAG chatbot."""
        if self.chain is None:
            # Re-initialize in case data was added later
            self.chain = self._initialize_chain()
            if self.chain is None:
                return "The knowledge base is empty. Please upload some company documents first."

        try:
            response = self.chain.invoke({"question": question})
            answer = response.get("answer", "I couldn't process that.")
            source_docs = response.get("source_documents", [])
            
            sources = []
            for doc in source_docs:
                source = doc.metadata.get("source", "Unknown")
                if source not in sources:
                    sources.append(source)
            
            return {
                "answer": answer,
                "sources": sources
            }
        except Exception as e:
            logger.error(f"Error during RAG ask: {e}")
            return {"answer": f"Error interacting with LLM: {str(e)}", "sources": []}

    def reset_memory(self):
        """Clear chat history."""
        self.memory.clear()
        logger.info("Chat history cleared.")
