import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import uuid

class VectorStoreRepository:
    """
    Abstracts interactions with the Vector Database (ChromaDB).
    """
    
    def __init__(self, persist_directory="data/chroma_db", collection_name="legal_docs"):
        """
        Initialize ChromaDB client and collection.
        
        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection
        """
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, texts: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]] = None):
        """
        Add documents and their embeddings to the vector store.
        
        Args:
            texts: List of text chunks
            embeddings: List of embedding vectors
            metadatas: Optional list of metadata dicts
        """
        ids = [str(uuid.uuid4()) for _ in texts]
        
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas if metadatas else [{}] * len(texts)
        )

    def search(self, query_embedding: List[float], k: int = 5) -> Dict[str, Any]:
        """
        Perform vector similarity search.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            
        Returns:
            Dict with 'documents', 'metadatas', and 'distances'
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        return {
            'documents': results['documents'][0],
            'metadatas': results['metadatas'][0],
            'distances': results['distances'][0]
        }
