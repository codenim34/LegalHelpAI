from fastapi import FastAPI

# TODO: Import routers from src.api.routes

app = FastAPI(title="Legal AI Doc Assistant API")

# TODO: Include routers
# app.include_router(ingest.router)
# app.include_router(query.router)

@app.get("/")
def read_root():
    """
    Root endpoint to check API status.
    """
    return {"status": "ok", "message": "Legal AI Doc Assistant API is running"}
