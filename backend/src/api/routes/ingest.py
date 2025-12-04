from fastapi import APIRouter, UploadFile, File, Depends
from typing import List
from src.api.dependencies import get_document_service
from src.services.document_service import DocumentService

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
    """
    result = await service.ingest(files)
    return result
