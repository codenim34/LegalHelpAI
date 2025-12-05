# Core Module

## Purpose
Contains **core business logic components** and essential system configurations that define how the Legal AI application works.

## Structure

### Essential Components

#### `config.py` ⚙️
- **Purpose**: Centralized application configuration
- **Contains**: Settings, environment variables, validation
- **Why core**: Essential for application initialization

#### `exceptions.py` 🛡️
- **Purpose**: Custom exception hierarchy
- **Contains**: Application-specific error types
- **Why core**: Defines error handling strategy

#### `logging_config.py` 📝
- **Purpose**: Application-wide logging setup
- **Contains**: Log formatters, handlers, configuration
- **Why core**: Essential for observability

#### `chunking.py` 📄
- **Purpose**: Text chunking strategy for RAG
- **Contains**: Chunker class with configurable parameters
- **Why core**: Defines how documents are processed (core RAG logic)

## Design Philosophy

### `core/` vs `utils/`

| Aspect | `core/` | `utils/` |
|--------|---------|----------|
| **Purpose** | Business logic, system essentials | Generic helpers |
| **Specificity** | Domain-specific | Generic, reusable |
| **Dependencies** | Other modules depend on these | Standalone utilities |
| **Examples** | Chunking strategy, config | File parsing, reranking |

### Why is `chunking.py` in `core/`?

**Reasoning**:
1. **Strategic Component**: Defines how your RAG system processes documents
2. **Business Logic**: Chunking strategy is specific to legal document processing
3. **Core to RAG**: Without proper chunking, the entire system fails
4. **Not Generic**: While it uses LangChain, the configuration is domain-specific

**Alternative View**: Could be in `utils/` if viewed as a generic utility, but semantically it's more "core" to your RAG pipeline.

## What Was Removed

### ~~`llm_client.py`~~ ❌ (Deleted)
- **Why removed**: Unused stub, redundant
- **Actual implementation**: LLM is directly used in `QueryService` via LangChain
- **No migration needed**: Was never used in the codebase

## Usage Examples

### Config
```python
from src.core.config import settings
print(settings.CHUNK_SIZE)
```

### Exceptions
```python
from src.core.exceptions import DocumentProcessingError
raise DocumentProcessingError("Failed to parse document")
```

### Logging
```python
from src.core.logging_config import get_logger
logger = get_logger(__name__)
logger.info("Processing...")
```

### Chunking
```python
from src.core.chunking import Chunker
chunker = Chunker()  # Uses settings automatically
chunks = chunker.chunk_text(text, metadata={...})
```

## Maintenance Notes

- All core components use centralized `settings`
- All components have logging configured
- All components have proper error handling
- Core components are singletons (cached via `@lru_cache()`)

