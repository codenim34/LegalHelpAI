"""
Custom exceptions for the Legal AI application.
Provides specific error types for better error handling and debugging.
"""

class LegalAIException(Exception):
    """Base exception for all Legal AI application errors."""
    pass

class DocumentProcessingError(LegalAIException):
    """Raised when document processing fails (parsing, chunking, etc.)."""
    pass

class VectorStoreError(LegalAIException):
    """Raised when vector store operations fail (add, search, etc.)."""
    pass

class EmbeddingError(LegalAIException):
    """Raised when embedding generation fails."""
    pass

class QueryError(LegalAIException):
    """Raised when query processing fails."""
    pass

class ConfigurationError(LegalAIException):
    """Raised when configuration is invalid or missing."""
    pass

class FileStorageError(LegalAIException):
    """Raised when file storage operations fail."""
    pass

class UnsupportedFileTypeError(LegalAIException):
    """Raised when an unsupported file type is uploaded."""
    pass

