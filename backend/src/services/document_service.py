from typing import List
from src.core.logging_config import get_logger
from src.core.exceptions import DocumentProcessingError, FileStorageError

logger = get_logger(__name__)

class DocumentService:
    """
    Orchestrates the document ingestion pipeline.
    """
    
    def __init__(self, document_repo, vector_store_repo, parser, chunker, embedder):
        """
        Initialize with necessary repositories and utilities.
        
        Args:
            document_repo: DocumentRepository instance
            vector_store_repo: VectorStoreRepository instance
            parser: FileParser instance
            chunker: Chunker instance
            embedder: EmbeddingService instance
        """
        self.document_repo = document_repo
        self.vector_store_repo = vector_store_repo
        self.parser = parser
        self.chunker = chunker
        self.embedder = embedder

    async def ingest(self, files: List) -> dict:
        """
        Main logic for ingesting files:
        1. Save file to disk (DocumentRepo).
        2. Parse text (Parser).
        3. Chunk text (Chunker).
        4. Generate embeddings (Embedder).
        5. Store vectors (VectorStoreRepo).
        
        Args:
            files: List of UploadFile objects
            
        Returns:
            dict: Status message with ingestion results
        """
        logger.info(f"Starting document ingestion for {len(files)} file(s)")
        ingested_files = []
        failed_files = []
        
        for file in files:
            try:
                logger.info(f"Processing file: {file.filename}")
                
                # 1. Save file
                file_path = await self.document_repo.save_file(file)
                logger.debug(f"File saved to: {file_path}")
                
                # 2. Parse text
                text = self.parser.parse(file_path)
                logger.debug(f"Text extracted. Length: {len(text)} characters")
                
                if not text or len(text.strip()) == 0:
                    raise DocumentProcessingError(f"No text extracted from {file.filename}")
                
                # 3. Chunk text
                chunks = self.chunker.chunk_text(
                    text, 
                    metadata={'filename': file.filename, 'source': file_path}
                )
                logger.debug(f"Text chunked into {len(chunks)} chunk(s)")
                
                # 4. Generate embeddings
                chunk_texts = [chunk['text'] for chunk in chunks]
                embeddings = self.embedder.embed_documents(chunk_texts)
                logger.debug(f"Generated {len(embeddings)} embedding(s)")
                
                # 5. Store in vector database
                metadatas = [chunk['metadata'] for chunk in chunks]
                self.vector_store_repo.add_documents(chunk_texts, embeddings, metadatas)
                logger.info(f"Successfully ingested: {file.filename}")
                
                ingested_files.append(file.filename)
                
            except Exception as e:
                logger.error(f"Failed to ingest {file.filename}: {str(e)}", exc_info=True)
                failed_files.append({'filename': file.filename, 'error': str(e)})
        
        logger.info(f"Ingestion complete. Success: {len(ingested_files)}, Failed: {len(failed_files)}")
        
        return {
            'status': 'success' if len(ingested_files) > 0 else 'failed',
            'files_ingested': ingested_files,
            'files_failed': failed_files,
            'total_files': len(files),
            'success_count': len(ingested_files),
            'failure_count': len(failed_files)
        }
