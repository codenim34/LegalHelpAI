from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List
from src.api.dependencies import get_document_service
from src.services.document_service import DocumentService
from src.core.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/")
async def ingest_documents(
    files: List[UploadFile] = File(...),
    service: DocumentService = Depends(get_document_service)
):
    """
    Endpoint to upload and process documents.
    
    Flow:
    1. Receive files.
    2. Call DocumentService.ingest(files).
    3. Return success message.
    
    Args:
        files: List of uploaded files (PDF, DOCX, images)
        
    Returns:
        Ingestion result with success/failure counts
    """
    logger.info(f"Ingestion request received for {len(files)} file(s)")
    
    if not files:
        logger.warning("No files provided in ingestion request")
        raise HTTPException(status_code=400, detail="No files provided")
    
    try:
        result = await service.ingest(files)
        logger.info(f"Ingestion completed: {result}")
        return result
    except Exception as e:
        logger.error(f"Ingestion failed: {e}", exc_info=True)
        raise
