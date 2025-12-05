from sentence_transformers import SentenceTransformer
from typing import List
from src.core.config import settings
from src.core.logging_config import get_logger
from src.core.exceptions import EmbeddingError

logger = get_logger(__name__)

class EmbeddingService:
    """
    Handles generation of embeddings for text.
    """
    
    def __init__(self, model_name=None):
        """
        Initialize the embedding model.
        
        Args:
            model_name: Name of the HuggingFace model to use (defaults to settings)
        """
        model_name = model_name or settings.EMBEDDING_MODEL_NAME
        logger.info(f"Loading embedding model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise EmbeddingError(f"Failed to load embedding model: {e}")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        try:
            logger.debug(f"Generating embeddings for {len(texts)} text(s)")
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise EmbeddingError(f"Failed to generate embeddings: {e}")

    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query string.
        
        Args:
            text: Query text
            
        Returns:
            Embedding vector
        """
        try:
            logger.debug("Generating query embedding")
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            raise EmbeddingError(f"Failed to generate query embedding: {e}")
