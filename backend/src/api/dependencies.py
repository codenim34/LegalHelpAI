from src.services.document_service import DocumentService
from src.services.query_service import QueryService
from src.services.embedding_service import EmbeddingService
from src.repositories.document_repo import DocumentRepository
from src.repositories.vector_store_repo import VectorStoreRepository
from src.utils.parsers import FileParser
from src.core.chunking import Chunker

def get_document_service() -> DocumentService:
    """
    Dependency provider for DocumentService.
    """
    document_repo = DocumentRepository()
    vector_store_repo = VectorStoreRepository()
    parser = FileParser()
    chunker = Chunker()
    embedder = EmbeddingService()
    
    return DocumentService(
        document_repo=document_repo,
        vector_store_repo=vector_store_repo,
        parser=parser,
        chunker=chunker,
        embedder=embedder
    )

def get_query_service() -> QueryService:
    """
    Dependency provider for QueryService.
    """
    vector_store_repo = VectorStoreRepository()
    embedder = EmbeddingService()
    
    return QueryService(
        vector_store_repo=vector_store_repo,
        embedder=embedder
    )
