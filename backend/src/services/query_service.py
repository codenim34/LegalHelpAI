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

    def __init__(self, vector_store_repo, embedder, reranker):
        """
        Initialize with repositories and clients.

        Args:
            vector_store_repo: VectorStoreRepository instance
            embedder: EmbeddingService instance
            reranker: Reranker instance
        """
        self.vector_store_repo = vector_store_repo
        self.embedder = embedder
        self.reranker = reranker

        # Initialize LLM (Gemini)
        if not settings.GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY not found in environment variables")
            raise ConfigurationError(
                "GOOGLE_API_KEY not found in environment variables"
            )

        logger.info(f"Initializing LLM: {settings.LLM_MODEL}")
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            google_api_key=settings.GOOGLE_API_KEY,
        )

        # Define RAG Prompt
        self.prompt = ChatPromptTemplate.from_template("""
  You are a helpful legal assistant and advocate of Bangladesh Court. Use the provided context to answer the user's legal question when it is relevant and reliable.
- Prefer the provided context for facts that are directly supported by it.
- If the context does not fully answer the question, you may use your general Bangladesh legal knowledge to provide a clear, accurate answer.
- When you use the context, cite the source document and section (if available). If you use general knowledge, clearly state that the answer is from general legal knowledge and not found in the provided context.
- If the context conflicts with known law or appears outdated, point out the conflict and rely on correct legal principles.
- Provide step-by-step actionable guidance where appropriate, and include any important caveats (jurisdiction limits, dates, need to consult a qualified lawyer).
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
        3. Re-rank chunks (Reranker).
        4. Generate answer (LLM).

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

            # 2. Retrieve relevant chunks using HYBRID SEARCH (BM25 + Vector)
            # Retrieve more candidates (2x) for re-ranking
            initial_k = settings.TOP_K_RESULTS * 2
            logger.debug(f"Performing hybrid search (top_k={initial_k}, alpha={settings.HYBRID_SEARCH_ALPHA})")
            
            search_results = self.vector_store_repo.hybrid_search(
                query_embedding=query_embedding,
                query_text=query_text,
                k=initial_k,
                alpha=settings.HYBRID_SEARCH_ALPHA,
            )

            documents = search_results["documents"]
            metadatas = search_results["metadatas"]

            if not documents:
                logger.warning("No relevant documents found in vector store")
                return {
                    "response": "I couldn't find any relevant information in the documents to answer your question.",
                    "sources": [],
                    "context_used": [],
                }

            # 3. Re-ranking
            logger.debug(f"Re-ranking {len(documents)} documents")
            reranked_results = self.reranker.rerank(
                query=query_text,
                documents=documents,
                top_k=settings.TOP_K_RESULTS
            )
            
            # Extract re-ranked docs and metadatas
            ranked_docs = []
            ranked_metadatas = []
            
            for doc_text, score, original_idx in reranked_results:
                ranked_docs.append(doc_text)
                ranked_metadatas.append(metadatas[original_idx])
            
            logger.debug(f"Selected top {len(ranked_docs)} documents after re-ranking")

            # Format context
            context = "\n\n".join(ranked_docs)

            # 4. Generate answer
            logger.debug("Generating LLM response")
            chain = self.prompt | self.llm | StrOutputParser()
            response = await chain.ainvoke({"context": context, "question": query_text})

            # Extract unique sources
            sources = list(set([m.get("filename", "Unknown") for m in ranked_metadatas]))

            logger.info(f"Query processed successfully. Sources: {sources}")

            return {
                "response": response,
                "sources": sources,
                "context_used": ranked_docs,
            }

        except Exception as e:
            logger.error(f"Query processing failed: {str(e)}", exc_info=True)
            raise QueryError(f"Failed to process query: {str(e)}")
