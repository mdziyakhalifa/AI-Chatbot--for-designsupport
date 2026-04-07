from langchain_huggingface import HuggingFaceEmbeddings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_embeddings():
    """
    Initializes and returns a local HuggingFace embedding model.
    Using 'all-MiniLM-L6-v2' for a good balance between speed and quality.
    This runs entirely on your local machine for free.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'} # Change to 'cuda' if you have a GPU
    encode_kwargs = {'normalize_embeddings': False}
    
    logger.info(f"Initializing HuggingFace embeddings with model: {model_name}")
    
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        return embeddings
    except Exception as e:
        logger.error(f"Error initializing embeddings: {e}")
        raise
