# Utils Module

## Purpose
Contains **generic utilities and helpers** that are reusable across different projects or contexts.

## Structure

### Utilities

#### `parsers.py` 📄
- **Purpose**: File parsing for different formats
- **Contains**: PDF, DOCX, and image parsing
- **Why utils**: Generic file parsing that could be reused in any project

#### `reranker.py` 🎯
- **Purpose**: Optional result reranking
- **Contains**: Reranking logic for search results
- **Why utils**: Generic ranking utility

## Design Philosophy

### `utils/` vs `core/`

| Aspect | `utils/` | `core/` |
|--------|----------|---------|
| **Purpose** | Generic helpers | Business logic, system essentials |
| **Specificity** | Generic, reusable | Domain-specific |
| **Dependencies** | Standalone | Other modules depend on these |
| **Examples** | File parsing, reranking | Chunking strategy, config |

### What Belongs in `utils/`?

✅ **Should be in utils:**
- Generic file parsing (PDF, DOCX, images)
- Reranking algorithms
- Data transformations
- Format converters
- Helper functions

❌ **Should NOT be in utils:**
- Business logic (→ `services/`)
- Core strategies (→ `core/`)
- Data access (→ `repositories/`)
- API routes (→ `api/`)

## Usage Examples

### File Parser
```python
from src.utils.parsers import FileParser

parser = FileParser()
text = parser.parse("/path/to/document.pdf")
```

### Reranker
```python
from src.utils.reranker import Reranker

reranker = Reranker()
reranked_results = reranker.rerank(query, results)
```

## Characteristics of Good Utils

1. **Self-contained**: Minimal dependencies
2. **Reusable**: Could work in different projects
3. **Generic**: Not tied to specific business logic
4. **Stateless**: Typically don't hold state (or hold minimal state)
5. **Testable**: Easy to unit test in isolation

## Current Utils

### `parsers.py`
- ✅ Generic file parsing
- ✅ Works with standard formats
- ✅ Could be used in any document processing app
- Status: **Properly placed**

### `reranker.py`
- ✅ Generic ranking algorithm
- ✅ Not specific to legal documents
- ✅ Could be used in any RAG system
- Status: **Properly placed**

## Maintenance Notes

- Utils should have minimal dependencies on `core/` or `services/`
- Use dependency injection for configuration
- Keep utils focused and single-purpose
- Document clearly what each utility does

