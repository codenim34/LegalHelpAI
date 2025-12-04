from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from src.api.dependencies import get_query_service
from src.services.query_service import QueryService

router = APIRouter(prefix="/query", tags=["Query"])

class QueryRequest(BaseModel):
    query: str

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
    """
    try:
        result = await service.query(request.query)
        return QueryResponse(
            response=result["response"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
