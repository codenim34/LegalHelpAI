from fastapi import FastAPI
from src.api.routes import ingest, query
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Legal AI Doc Assistant API")

# Include routers
app.include_router(ingest.router)
app.include_router(query.router)

@app.get("/")
def read_root():
    """
    Root endpoint to check API status.
    """
    return {"status": "ok", "message": "Legal AI Doc Assistant API is running"}
