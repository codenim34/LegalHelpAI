from typing import List

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
        ingested_files = []
        
        for file in files:
            # 1. Save file
            file_path = await self.document_repo.save_file(file)
            
            # 2. Parse text
            text = self.parser.parse(file_path)
            
            # 3. Chunk text
            chunks = self.chunker.chunk_text(
                text, 
                metadata={'filename': file.filename, 'source': file_path}
            )
            
            # 4. Generate embeddings
            chunk_texts = [chunk['text'] for chunk in chunks]
            embeddings = self.embedder.embed_documents(chunk_texts)
            
            # 5. Store in vector database
            metadatas = [chunk['metadata'] for chunk in chunks]
            self.vector_store_repo.add_documents(chunk_texts, embeddings, metadatas)
            
            ingested_files.append(file.filename)
        
        return {
            'status': 'success',
            'files_ingested': ingested_files,
            'total_files': len(files)
        }
