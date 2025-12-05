# Quick Configuration Reference Card 📋

## One-Page Guide to All Settings

### 🔧 Most Commonly Tuned Settings

```python
# In: backend/src/core/config.py

# Control hybrid search behavior (tune this first!)
HYBRID_SEARCH_ALPHA = 0.7  # Range: 0.0-1.0
                           # Higher = more semantic, Lower = more keyword

# How many results to show user
TOP_K_RESULTS = 5  # Typical range: 3-10

# LLM creativity
LLM_TEMPERATURE = 0.3  # Range: 0.0-1.0
                       # Lower = more focused, Higher = more creative
```

### 📊 Tuning Guide

| Use Case | Recommended Settings |
|----------|---------------------|
| **Exact Legal Citations** | `HYBRID_SEARCH_ALPHA = 0.3-0.5` (favor keywords) |
| **Conceptual Questions** | `HYBRID_SEARCH_ALPHA = 0.8-0.9` (favor semantics) |
| **Balanced Queries** | `HYBRID_SEARCH_ALPHA = 0.6-0.7` (default) |
| **More Context** | `TOP_K_RESULTS = 8-10` |
| **Faster Responses** | `TOP_K_RESULTS = 3-5` |
| **Conservative Answers** | `LLM_TEMPERATURE = 0.1-0.3` |
| **Creative Explanations** | `LLM_TEMPERATURE = 0.5-0.7` |

### 🎯 Model Selection

```python
# Embedding Model (speed vs accuracy)
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # Fast, good quality (default)
# Alternative: "all-mpnet-base-v2"  # Slower, better quality
# Alternative: "all-MiniLM-L12-v2"  # Balanced

# Reranker Model (accuracy vs speed)
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"  # Fast (default)
# Alternative: "cross-encoder/ms-marco-MiniLM-L-12-v2"  # More accurate
# Alternative: "cross-encoder/ms-marco-electra-base"  # Best accuracy

# LLM Model
LLM_MODEL = "gemini-2.5-flash"  # Fast, cost-effective (default)
# Alternative: "gemini-pro"  # More capable, slower, pricier
```

### 🔐 Environment Variables (.env file)

```bash
# Required
GOOGLE_API_KEY=your_key_here

# Optional
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR
DEBUG=false     # Set to true for development
```

### 🛠️ Advanced Settings

```python
# Chunking (affects indexing quality)
CHUNK_SIZE = 1000      # Characters per chunk
CHUNK_OVERLAP = 200    # Overlap between chunks

# Hybrid Search Internals
HYBRID_SEARCH_RRF_K = 60  # Reciprocal Rank Fusion constant
                          # Range: 10-100, default 60 is usually optimal

# Vector Store
VECTOR_STORE_COLLECTION_NAME = "legal_docs"  # Change for different datasets
```

### 📁 Directory Structure

```python
CHROMA_DB_DIR = "data/chroma_db"  # Vector database storage
UPLOAD_DIR = "data/uploads"       # Uploaded document storage
```

### 🚀 Quick Start: Common Scenarios

#### Scenario 1: Improve Accuracy (Accept Slower Speed)
```python
EMBEDDING_MODEL_NAME = "all-mpnet-base-v2"
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-12-v2"
TOP_K_RESULTS = 8
HYBRID_SEARCH_ALPHA = 0.7
```

#### Scenario 2: Optimize for Speed
```python
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # default
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"  # default
TOP_K_RESULTS = 3
HYBRID_SEARCH_ALPHA = 0.7
```

#### Scenario 3: Keyword-Heavy Documents (e.g., Legal Codes)
```python
HYBRID_SEARCH_ALPHA = 0.4  # Favor BM25 keyword matching
TOP_K_RESULTS = 5
```

#### Scenario 4: Concept-Heavy Documents (e.g., Legal Opinions)
```python
HYBRID_SEARCH_ALPHA = 0.8  # Favor semantic similarity
TOP_K_RESULTS = 7
```

### 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Responses too generic | Decrease `LLM_TEMPERATURE` to 0.1-0.2 |
| Missing obvious keyword matches | Decrease `HYBRID_SEARCH_ALPHA` to 0.4-0.5 |
| Missing semantic matches | Increase `HYBRID_SEARCH_ALPHA` to 0.8-0.9 |
| Not enough context | Increase `TOP_K_RESULTS` to 8-10 |
| Too slow | Decrease `TOP_K_RESULTS`, use faster models |
| Out of memory | Use smaller models or decrease `TOP_K_RESULTS` |

### 📝 How to Change Settings

1. **Edit** `backend/src/core/config.py`
2. **Restart** the application
3. **Test** with sample queries
4. **Iterate** based on results

### ⚡ Quick Commands

```bash
# Restart application
cd backend
python run.py

# Check current settings
python -c "from src.core.config import settings; \
  print(f'Alpha: {settings.HYBRID_SEARCH_ALPHA}'); \
  print(f'Top-K: {settings.TOP_K_RESULTS}')"

# Validate configuration
python -c "from src.core.config import settings; settings.validate()"
```

### 📚 Full Documentation

- **Detailed Guide**: See `CONFIGURATION.md`
- **Technical Details**: See `REFACTORING_SUMMARY.md`
- **Visual Overview**: See `REFACTORING_VISUAL_SUMMARY.md`

---

**Pro Tip**: Start with defaults, then tune `HYBRID_SEARCH_ALPHA` based on your specific document types and query patterns. Monitor user satisfaction and adjust accordingly.

