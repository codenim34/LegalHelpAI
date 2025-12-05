import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import uuid
from src.core.config import settings as app_settings
from src.core.logging_config import get_logger
from src.core.exceptions import VectorStoreError

logger = get_logger(__name__)

class VectorStoreRepository:
    """
    Abstracts interactions with the Vector Database (ChromaDB).
    """
    
    def __init__(self, persist_directory=None, collection_name="legal_docs"):
        """
        Initialize ChromaDB client and collection.
        
        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection
        """
        try:
            persist_directory = persist_directory or app_settings.CHROMA_DB_DIR
            logger.info(f"Initializing ChromaDB client at: {persist_directory}")
            
            self.client = chromadb.PersistentClient(path=persist_directory)
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"ChromaDB initialized. Collection: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise VectorStoreError(f"Failed to initialize vector store: {e}")

    def add_documents(self, texts: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]] = None):
        """
        Add documents and their embeddings to the vector store.
        
        Args:
            texts: List of text chunks
            embeddings: List of embedding vectors
            metadatas: Optional list of metadata dicts
        """
        try:
            ids = [str(uuid.uuid4()) for _ in texts]
            logger.debug(f"Adding {len(texts)} document(s) to vector store")
            
            self.collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas if metadatas else [{}] * len(texts)
            )
            
            logger.info(f"Successfully added {len(texts)} document(s) to vector store")
        except Exception as e:
            logger.error(f"Failed to add documents to vector store: {e}")
            raise VectorStoreError(f"Failed to add documents: {e}")

    def search(self, query_embedding: List[float], k: int = 5) -> Dict[str, Any]:
        """
        Perform vector similarity search.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            
        Returns:
            Dict with 'documents', 'metadatas', and 'distances'
        """
        try:
            logger.debug(f"Searching vector store (k={k})")
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k
            )
            
            num_results = len(results['documents'][0]) if results['documents'] else 0
            logger.debug(f"Found {num_results} result(s)")
            
            return {
                'documents': results['documents'][0],
                'metadatas': results['metadatas'][0],
                'distances': results['distances'][0]
            }
        except Exception as e:
            logger.error(f"Failed to search vector store: {e}")
            raise VectorStoreError(f"Failed to search vector store: {e}")
