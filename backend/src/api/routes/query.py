from fastapi import APIRouter, Depends
# from src.models.schemas import QueryRequest, QueryResponse

router = APIRouter(prefix="/query", tags=["Query"])

# TODO: Inject QueryService dependency

@router.post("/")
async def query_documents():
    """
    Endpoint to query the RAG system.
    
    Flow:
    1. Receive user query.
    2. Call QueryService.query(query).
    3. Return response with sources.
    """
    # TODO: Call service layer
    pass
