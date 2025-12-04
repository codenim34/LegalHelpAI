from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    """
    Request model for the query endpoint.
    """
    query: str

class QueryResponse(BaseModel):
    """
    Response model for the query endpoint.
    """
    response: str
    sources: List[str] = []

class DocumentMetadata(BaseModel):
    """
    Metadata for an ingested document.
    """
    filename: str
    content_type: str
