from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Chunk:
    """
    Represents a text chunk with metadata.
    """
    text: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None

@dataclass
class Document:
    """
    Represents a full document.
    """
    filename: str
    content: str
    chunks: List[Chunk] = None
