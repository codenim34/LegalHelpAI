from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

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
        # Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=api_key
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
        # 1. Generate embedding
        query_embedding = self.embedder.embed_query(query_text)
        
        # 2. Retrieve relevant chunks
        search_results = self.vector_store_repo.search(query_embedding, k=5)
        
        documents = search_results['documents'] # List of text chunks
        metadatas = search_results['metadatas'] # List of metadata dicts
        
        # Format context
        context = "\n\n".join(documents)
        
        # 3. Generate answer
        chain = self.prompt | self.llm | StrOutputParser()
        response = await chain.ainvoke({"context": context, "question": query_text})
        
        # Extract unique sources
        sources = list(set([m.get('filename', 'Unknown') for m in metadatas]))
        
        return {
            "response": response,
            "sources": sources,
            "context_used": documents # Optional: for debugging
        }
