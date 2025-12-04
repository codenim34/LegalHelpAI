from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

class Chunker:
    """
    Handles text chunking strategies.
    """
    
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        """
        Initialize chunker with configurable parameters.
        
        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
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
