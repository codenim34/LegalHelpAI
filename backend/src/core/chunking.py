from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from src.core.config import settings

class Chunker:
    """
    Handles text chunking strategies.
    """
    
    def __init__(self, chunk_size=None, chunk_overlap=None):
        """
        Initialize chunker with configurable parameters.
        
        Args:
            chunk_size: Maximum size of each chunk (defaults to settings)
            chunk_overlap: Number of characters to overlap between chunks (defaults to settings)
        """
        chunk_size = chunk_size or settings.CHUNK_SIZE
        chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def chunk_text(self, text: str, metadata: dict = None) -> List[dict]:
        """
        Split text into chunks based on the selected strategy.
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of dicts with 'text' and 'metadata' keys
        """
        chunks = self.text_splitter.split_text(text)
        
        result = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = metadata.copy() if metadata else {}
            chunk_metadata['chunk_index'] = i
            result.append({
                'text': chunk,
                'metadata': chunk_metadata
            })
        
        return result
