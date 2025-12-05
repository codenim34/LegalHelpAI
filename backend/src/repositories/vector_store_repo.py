import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import uuid
import numpy as np
from rank_bm25 import BM25Okapi
from src.core.config import settings as app_settings
from src.core.logging_config import get_logger
from src.core.exceptions import VectorStoreError

logger = get_logger(__name__)

class VectorStoreRepository:
    """
    Abstracts interactions with the Vector Database (ChromaDB).
    """
    
    def __init__(self, persist_directory: str = None, collection_name: str = None):
        """
        Initialize ChromaDB client and collection.
        
        Args:
            persist_directory: Directory to persist the database (defaults to settings.CHROMA_DB_DIR)
            collection_name: Name of the collection (defaults to settings.VECTOR_STORE_COLLECTION_NAME)
        """
        try:
            persist_directory = persist_directory or app_settings.CHROMA_DB_DIR
            collection_name = collection_name or app_settings.VECTOR_STORE_COLLECTION_NAME
            logger.info(f"Initializing ChromaDB client at: {persist_directory}")
            
            self.client = chromadb.PersistentClient(path=persist_directory)
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            # Initialize BM25 for hybrid search
            self.bm25_index = None
            self.bm25_docs = []
            self.bm25_metadatas = []
            
            logger.info(f"ChromaDB initialized. Collection: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise VectorStoreError(f"Failed to initialize vector store: {e}")

    def add_documents(self, texts: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]] = None):
        """
        Add documents and their embeddings to the vector store.
        Also builds BM25 index for hybrid search.
        
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
            
            # Add to BM25 index
            self.bm25_docs.extend(texts)
            self.bm25_metadatas.extend(metadatas if metadatas else [{}] * len(texts))
            
            # Rebuild BM25 index
            tokenized_corpus = [doc.lower().split() for doc in self.bm25_docs]
            self.bm25_index = BM25Okapi(tokenized_corpus)
            
            logger.info(f"Successfully added {len(texts)} document(s) to vector store and BM25 index")
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

    def hybrid_search(self, query_embedding: List[float], query_text: str, k: int = 5, alpha: float = None) -> Dict[str, Any]:
        """
        Perform hybrid search combining BM25 and vector search using RRF.
        
        Args:
            query_embedding: Query embedding vector
            query_text: Original query text for BM25
            k: Number of results to return
            alpha: Weight for combining scores (0=BM25 only, 1=vector only, defaults to settings.HYBRID_SEARCH_ALPHA)
            
        Returns:
            Dict with 'documents', 'metadatas', and 'scores'
        """
        alpha = alpha if alpha is not None else app_settings.HYBRID_SEARCH_ALPHA
        try:
            logger.debug(f"Performing hybrid search (k={k}, alpha={alpha})")
            
            # 1. Vector search (get top 2k for better coverage)
            vector_results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(k * 2, max(len(self.bm25_docs), 1))
            )
            
            # 2. BM25 search
            if self.bm25_index and self.bm25_docs:
                tokenized_query = query_text.lower().split()
                bm25_scores = self.bm25_index.get_scores(tokenized_query)
            else:
                logger.warning("BM25 index not initialized, falling back to vector search only")
                return self.search(query_embedding, k)
            
            # 3. Reciprocal Rank Fusion (RRF)
            doc_scores = {}
            rrf_k = app_settings.HYBRID_SEARCH_RRF_K
            
            # Add vector search scores (using RRF: 1/(rank + k))
            for rank, (doc, metadata) in enumerate(zip(vector_results['documents'][0], vector_results['metadatas'][0])):
                rrf_score = 1.0 / (rank + rrf_k)
                doc_scores[doc] = {
                    'score': alpha * rrf_score,
                    'metadata': metadata
                }
            
            # Add BM25 scores (using RRF)
            bm25_ranked = sorted(enumerate(bm25_scores), key=lambda x: -x[1])
            for rank, (idx, score) in enumerate(bm25_ranked[:k * 2]):
                doc = self.bm25_docs[idx]
                rrf_score = 1.0 / (rank + rrf_k)
                
                if doc in doc_scores:
                    doc_scores[doc]['score'] += (1 - alpha) * rrf_score
                else:
                    doc_scores[doc] = {
                        'score': (1 - alpha) * rrf_score,
                        'metadata': self.bm25_metadatas[idx]
                    }
            
            # 4. Sort by combined score and return top k
            sorted_docs = sorted(doc_scores.items(), key=lambda x: -x[1]['score'])[:k]
            
            logger.debug(f"Hybrid search found {len(sorted_docs)} result(s)")
            
            return {
                'documents': [doc for doc, _ in sorted_docs],
                'metadatas': [data['metadata'] for _, data in sorted_docs],
                'scores': [data['score'] for _, data in sorted_docs]
            }
        except Exception as e:
            logger.error(f"Hybrid search failed: {e}")
            raise VectorStoreError(f"Hybrid search failed: {e}")
