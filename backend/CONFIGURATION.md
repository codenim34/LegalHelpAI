# Configuration Guide

This document explains the configuration options available in the LegalHelpAI backend.

## Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```env
# Required: Google API Key for Gemini LLM
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Optional: Enable debug mode
DEBUG=false
```

## Application Settings

All application settings are centralized in `src/core/config.py`. You can override defaults by modifying the `Settings` class or setting environment variables where applicable.

### Model Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `EMBEDDING_MODEL_NAME` | `"all-MiniLM-L6-v2"` | HuggingFace embedding model for document/query embeddings |
| `RERANKER_MODEL_NAME` | `"cross-encoder/ms-marco-MiniLM-L-6-v2"` | CrossEncoder model for re-ranking retrieved documents |
| `LLM_MODEL` | `"gemini-2.5-flash"` | Google Gemini model for answer generation |
| `LLM_TEMPERATURE` | `0.3` | Temperature for LLM responses (0.0-1.0) |

### RAG Pipeline Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `CHUNK_SIZE` | `1000` | Number of characters per text chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between consecutive chunks |
| `TOP_K_RESULTS` | `5` | Number of final results to return to LLM |

### Hybrid Search Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `HYBRID_SEARCH_ALPHA` | `0.7` | Weight for combining vector and BM25 scores (0=BM25 only, 1=vector only) |
| `HYBRID_SEARCH_RRF_K` | `60` | RRF constant for Reciprocal Rank Fusion (standard value) |

**Tuning Hybrid Search:**
- Increase `HYBRID_SEARCH_ALPHA` (e.g., 0.8-0.9) to favor semantic similarity
- Decrease `HYBRID_SEARCH_ALPHA` (e.g., 0.3-0.5) to favor keyword matching
- Adjust `HYBRID_SEARCH_RRF_K` (typically 10-100) to control rank influence

### Vector Store Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `VECTOR_STORE_COLLECTION_NAME` | `"legal_docs"` | ChromaDB collection name |
| `CHROMA_DB_DIR` | `"data/chroma_db"` | Directory for ChromaDB persistence |

### File Upload Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `UPLOAD_DIR` | `"data/uploads"` | Directory for uploaded documents |

### Server Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `HOST` | `"0.0.0.0"` | Server host address |
| `PORT` | `8000` | Server port |
| `DEBUG` | `false` | Enable debug mode (via env var) |

## Best Practices

### ✅ Good Practices (Implemented)

1. **Centralized Configuration**: All settings in one place (`config.py`)
2. **Environment Variable Support**: Sensitive data (API keys) via `.env`
3. **Type Hints**: All settings have type annotations
4. **Defaults**: Sensible defaults for all non-sensitive settings
5. **Validation**: Critical settings validated on startup
6. **Dependency Injection**: Services receive configuration via constructor parameters or settings import

### 🎯 How We Refactored

#### Before (Bad Practice)
```python
# Hardcoded model name in constructor
def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
    self.model = CrossEncoder(model_name)
```

#### After (Good Practice)
```python
# Configuration from settings with optional override
def __init__(self, model_name: str = None):
    model_name = model_name or settings.RERANKER_MODEL_NAME
    self.model = CrossEncoder(model_name)
```

## Customization Examples

### Example 1: Use a Different Embedding Model
```python
# In src/core/config.py
EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-mpnet-base-v2"
```

### Example 2: Adjust Hybrid Search for More Keyword Matching
```python
# In src/core/config.py
HYBRID_SEARCH_ALPHA: float = 0.4  # 40% vector, 60% BM25
```

### Example 3: Use a Different Reranker Model
```python
# In src/core/config.py
RERANKER_MODEL_NAME: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"  # Larger, more accurate
```

## Troubleshooting

### Issue: Models not loading
- **Check**: Model names are correct and available on HuggingFace
- **Check**: You have internet connection on first run (models are downloaded)
- **Check**: Sufficient disk space for model caching

### Issue: GOOGLE_API_KEY error
- **Fix**: Create a `.env` file in `backend/` directory
- **Fix**: Add `GOOGLE_API_KEY=your_key_here`
- **Check**: API key is valid and has Gemini API access

### Issue: Poor search quality
- **Tune**: Adjust `HYBRID_SEARCH_ALPHA` based on your data
- **Tune**: Increase `TOP_K_RESULTS` for more context
- **Consider**: Using a larger embedding model or reranker

## Migration Notes

If upgrading from older versions, note these changes:
- Hardcoded model names removed from class constructors
- Hardcoded alpha values removed from query logic
- Collection name now configurable via settings
- RRF constant now configurable for hybrid search tuning

