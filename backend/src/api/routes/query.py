from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List
from src.api.dependencies import get_query_service
from src.services.query_service import QueryService
from src.core.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/query", tags=["Query"])

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="User query")
    
    @validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()

class QueryResponse(BaseModel):
    response: str
    sources: List[str] = []

@router.post("/", response_model=QueryResponse)
async def query_documents(
    request: QueryRequest,
    service: QueryService = Depends(get_query_service)
):
    """
    Endpoint to query the RAG system.
    
    Flow:
    1. Receive user query.
    2. Call QueryService.query(query).
    3. Return response with sources.
    
    Args:
        request: Query request with user question
        
    Returns:
        QueryResponse with answer and source documents
    """
    logger.info(f"Query request received: {request.query[:100]}...")
    
    try:
        result = await service.query(request.query)
        response = QueryResponse(
            response=result["response"],
            sources=result["sources"]
        )
        logger.info(f"Query processed successfully")
        return response
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        raise
