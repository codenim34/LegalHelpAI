import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Application configuration settings.
    Centralized configuration management for the entire application.
    """
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Paths
    CHROMA_DB_DIR: str = "data/chroma_db"
    UPLOAD_DIR: str = "data/uploads"
    
    # Models
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    RERANKER_MODEL_NAME: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    LLM_MODEL: str = "gemini-2.5-flash"
    LLM_TEMPERATURE: float = 0.3
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 5
    
    # Hybrid Search Settings
    HYBRID_SEARCH_ALPHA: float = 0.7  # 0=BM25 only, 1=vector only
    HYBRID_SEARCH_RRF_K: int = 60  # RRF constant for reciprocal rank fusion
    
    # Vector Store Settings
    VECTOR_STORE_COLLECTION_NAME: str = "legal_docs"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def __init__(self):
        """Ensure required directories exist."""
        Path(self.CHROMA_DB_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
    
    def validate(self):
        """Validate critical settings."""
        if not self.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required. Please set it in .env file.")

settings = Settings()
