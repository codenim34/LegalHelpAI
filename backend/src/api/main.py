from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.api.routes import ingest, query
from src.core.exceptions import LegalAIException
from src.core.logging_config import setup_logging, get_logger
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Setup logging
setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="Legal AI Doc Assistant API",
    description="RAG-based legal document assistant with document ingestion and query capabilities",
    version="1.0.0"
)

# Exception handlers
@app.exception_handler(LegalAIException)
async def legal_ai_exception_handler(request: Request, exc: LegalAIException):
    """Handle custom Legal AI exceptions."""
    logger.error(f"LegalAI error: {exc.__class__.__name__}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
            "detail": "An error occurred while processing your request."
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Invalid request data",
            "details": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred. Please try again later."
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Starting Legal AI Doc Assistant API...")
    logger.info("Application initialized successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down Legal AI Doc Assistant API...")

# Include routers
from src.api.routes import health
app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(query.router)

@app.get("/")
def read_root():
    """
    Root endpoint to check API status.
    """
    logger.info("Root endpoint accessed")
    return {
        "status": "ok", 
        "message": "Legal AI Doc Assistant API is running",
        "version": "1.0.0"
    }
