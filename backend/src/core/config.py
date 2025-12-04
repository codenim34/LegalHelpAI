import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Application configuration settings.
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    CHROMA_DB_DIR = "data/chroma_db"
    UPLOAD_DIR = "data/uploads"
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

settings = Settings()
