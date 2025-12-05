from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.core.logging_config import get_logger
from src.repositories.vector_store_repo import VectorStoreRepository
from pathlib import Path
import sys

logger = get_logger(__name__)
router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health_check():
    """
    Basic health check endpoint.
    Returns 200 if the API is running.
    """
    return {
        "status": "healthy",
        "service": "Legal AI Doc Assistant API",
        "version": "1.0.0"
    }

@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint.
    Checks if all dependencies are available and functioning.
    """
    checks = {
        "api": "ok",
        "vector_store": "unknown",
        "file_storage": "unknown",
        "config": "unknown"
    }
    
    all_healthy = True
    
    # Check vector store
    try:
        repo = VectorStoreRepository()
        repo.collection.count()  # Test connection
        checks["vector_store"] = "ok"
        logger.debug("Vector store health check: OK")
    except Exception as e:
        checks["vector_store"] = f"error: {str(e)}"
        all_healthy = False
        logger.error(f"Vector store health check failed: {e}")
    
    # Check file storage
    try:
        upload_dir = Path(settings.UPLOAD_DIR)
        chroma_dir = Path(settings.CHROMA_DB_DIR)
        if upload_dir.exists() and chroma_dir.exists():
            checks["file_storage"] = "ok"
            logger.debug("File storage health check: OK")
        else:
            checks["file_storage"] = "directories not found"
            all_healthy = False
    except Exception as e:
        checks["file_storage"] = f"error: {str(e)}"
        all_healthy = False
        logger.error(f"File storage health check failed: {e}")
    
    # Check configuration
    try:
        if settings.GOOGLE_API_KEY:
            checks["config"] = "ok"
            logger.debug("Configuration health check: OK")
        else:
            checks["config"] = "GOOGLE_API_KEY not set"
            all_healthy = False
    except Exception as e:
        checks["config"] = f"error: {str(e)}"
        all_healthy = False
        logger.error(f"Configuration health check failed: {e}")
    
    status_code = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ready" if all_healthy else "not_ready",
            "checks": checks,
            "settings": {
                "upload_dir": settings.UPLOAD_DIR,
                "chroma_db_dir": settings.CHROMA_DB_DIR,
                "embedding_model": settings.EMBEDDING_MODEL_NAME,
                "llm_model": settings.LLM_MODEL
            }
        }
    )

@router.get("/info")
async def info():
    """
    System information endpoint.
    Returns configuration and system details (non-sensitive).
    """
    return {
        "service": "Legal AI Doc Assistant API",
        "version": "1.0.0",
        "python_version": sys.version,
        "settings": {
            "chunk_size": settings.CHUNK_SIZE,
            "chunk_overlap": settings.CHUNK_OVERLAP,
            "top_k_results": settings.TOP_K_RESULTS,
            "embedding_model": settings.EMBEDDING_MODEL_NAME,
            "llm_model": settings.LLM_MODEL,
            "debug_mode": settings.DEBUG
        }
    }

