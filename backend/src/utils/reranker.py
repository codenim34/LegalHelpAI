from sentence_transformers import CrossEncoder
from typing import List, Tuple
from src.core.config import settings
from src.core.logging_config import get_logger
from src.core.exceptions import ConfigurationError

logger = get_logger(__name__)

class Reranker:
    """
    Handles re-ranking of retrieved documents using a Cross-Encoder.
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the CrossEncoder model.
        
        Args:
            model_name: Name of the CrossEncoder model (defaults to settings.RERANKER_MODEL_NAME)
        """
        try:
            model_name = model_name or settings.RERANKER_MODEL_NAME
            logger.info(f"Loading CrossEncoder model: {model_name}")
            self.model = CrossEncoder(model_name)
            logger.info("CrossEncoder model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load CrossEncoder model: {e}")
            raise ConfigurationError(f"Failed to load CrossEncoder model: {e}")

    def rerank(self, query: str, documents: List[str], top_k: int = 3) -> List[Tuple[str, float, int]]:
        """
        Re-rank the documents based on relevance to the query.
        
        Args:
            query: The user query
            documents: List of document texts
            top_k: Number of top results to return
            
        Returns:
            List of tuples (document_text, score, original_index) sorted by score
        """
        if not documents:
            return []
            
        try:
            # Create pairs of (query, document)
            pairs = [[query, doc] for doc in documents]
            
            # Predict scores
            scores = self.model.predict(pairs)
            
            # Combine docs with scores and original indices
            # Result: (doc_text, score, original_index)
            results = []
            for idx, (doc, score) in enumerate(zip(documents, scores)):
                results.append((doc, float(score), idx))
            
            # Sort by score descending
            ranked_results = sorted(results, key=lambda x: x[1], reverse=True)
            
            logger.debug(f"Re-ranked {len(documents)} documents. Top score: {ranked_results[0][1] if ranked_results else 0}")
            
            return ranked_results[:top_k]
        except Exception as e:
            logger.error(f"Re-ranking failed: {e}")
            # Fallback: return original documents with 0 score, preserving order
            return [(doc, 0.0, idx) for idx, doc in enumerate(documents[:top_k])]
