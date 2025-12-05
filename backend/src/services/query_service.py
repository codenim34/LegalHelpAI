from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.core.config import settings
from src.core.logging_config import get_logger
from src.core.exceptions import QueryError, ConfigurationError

logger = get_logger(__name__)

class QueryService:
    """
    Orchestrates the retrieval and generation pipeline.
    """
    
    def __init__(self, vector_store_repo, embedder):
        """
        Initialize with repositories and clients.
        
        Args:
            vector_store_repo: VectorStoreRepository instance
            embedder: EmbeddingService instance
        """
        self.vector_store_repo = vector_store_repo
        self.embedder = embedder
        
        # Initialize LLM (Gemini)
        if not settings.GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY not found in environment variables")
            raise ConfigurationError("GOOGLE_API_KEY not found in environment variables")
        
        logger.info(f"Initializing LLM: {settings.LLM_MODEL}")
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            google_api_key=settings.GOOGLE_API_KEY
        )
        
        # Define RAG Prompt
        self.prompt = ChatPromptTemplate.from_template("""
        You are a helpful legal assistant and advocate. Use the following context to answer the user's legal question.
        If the answer is not in the context, say you don't know based on the provided documents.
        Always cite the source document and section if possible.
        
        Context:
        {context}
        
        Question:
        {question}
        
        Answer:
        """)

    async def query(self, query_text: str) -> Dict[str, Any]:
        """
        Main logic for answering queries:
        1. Generate query embedding (Embedder).
        2. Retrieve relevant chunks (VectorStoreRepo).
        3. Generate answer (LLM).
        
        Args:
            query_text: User's question
            
        Returns:
            Dict with 'response' and 'sources'
        """
        logger.info(f"Processing query: {query_text[:100]}...")
        
        try:
            # 1. Generate embedding
            logger.debug("Generating query embedding")
            query_embedding = self.embedder.embed_query(query_text)
            
            # 2. Retrieve relevant chunks
            logger.debug(f"Searching vector store (top_k={settings.TOP_K_RESULTS})")
            search_results = self.vector_store_repo.search(
                query_embedding, 
                k=settings.TOP_K_RESULTS
            )
            
            documents = search_results['documents'] # List of text chunks
            metadatas = search_results['metadatas'] # List of metadata dicts
            
            if not documents or len(documents) == 0:
                logger.warning("No relevant documents found in vector store")
                return {
                    "response": "I couldn't find any relevant information in the documents to answer your question.",
                    "sources": [],
                    "context_used": []
                }
            
            logger.debug(f"Found {len(documents)} relevant chunk(s)")
            
            # Format context
            context = "\n\n".join(documents)
            
            # 3. Generate answer
            logger.debug("Generating LLM response")
            chain = self.prompt | self.llm | StrOutputParser()
            response = await chain.ainvoke({"context": context, "question": query_text})
            
            # Extract unique sources
            sources = list(set([m.get('filename', 'Unknown') for m in metadatas]))
            
            logger.info(f"Query processed successfully. Sources: {sources}")
            
            return {
                "response": response,
                "sources": sources,
                "context_used": documents # Optional: for debugging
            }
        
        except Exception as e:
            logger.error(f"Query processing failed: {str(e)}", exc_info=True)
            raise QueryError(f"Failed to process query: {str(e)}")
