from fastapi import APIRouter, UploadFile, File, Depends
from typing import List

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

# TODO: Inject DocumentService dependency

@router.post("/")
async def ingest_documents(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload and process documents.
    
    Flow:
    1. Receive files.
    2. Call DocumentService.ingest(files).
    3. Return success message.
    """
    # TODO: Call service layer
    pass
