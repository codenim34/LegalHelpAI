from functools import lru_cache
from src.services.document_service import DocumentService
from src.services.query_service import QueryService
from src.services.embedding_service import EmbeddingService
from src.repositories.document_repo import DocumentRepository
from src.repositories.vector_store_repo import VectorStoreRepository
from src.utils.parsers import FileParser
from src.core.chunking import Chunker
from src.utils.reranker import Reranker

# Singleton instances (cached) for heavy/stateful components
@lru_cache()
def get_embedding_service() -> EmbeddingService:
    """
    Singleton embedding service.
    The embedding model is loaded once and reused across requests.
    """
    return EmbeddingService()

@lru_cache()
def get_vector_store_repo() -> VectorStoreRepository:
    """
    Singleton vector store repository.
    ChromaDB connection is created once and reused.
    """
    return VectorStoreRepository()

@lru_cache()
def get_document_repo() -> DocumentRepository:
    """
    Singleton document repository.
    """
    return DocumentRepository()

@lru_cache()
def get_parser() -> FileParser:
    """
    Singleton file parser.
    Vision model is loaded once if needed.
    """
    return FileParser()

@lru_cache()
def get_chunker() -> Chunker:
    """
    Singleton text chunker.
    """
    return Chunker()

@lru_cache()
def get_reranker() -> Reranker:
    """
    Singleton Reranker.
    Cross-Encoder model is loaded once and reused.
    """
    return Reranker()

# Service instances (lightweight, can be created per request)
def get_document_service() -> DocumentService:
    """
    Dependency provider for DocumentService.
    Uses cached singletons for heavy components.
    """
    return DocumentService(
        document_repo=get_document_repo(),
        vector_store_repo=get_vector_store_repo(),
        parser=get_parser(),
        chunker=get_chunker(),
        embedder=get_embedding_service()
    )

def get_query_service() -> QueryService:
    """
    Dependency provider for QueryService.
    Uses cached singletons for heavy components.
    """
    return QueryService(
        vector_store_repo=get_vector_store_repo(),
        embedder=get_embedding_service(),
        reranker=get_reranker()
    )
