"""
Custom exceptions for the Smriti Memory package.
"""


class SmritiError(Exception):
    """Base exception for all Smriti-related errors."""
    
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ConfigurationError(SmritiError):
    """Raised when there's an issue with configuration."""
    pass


class MemoryError(SmritiError):
    """Raised when there's an issue with memory operations."""
    pass


class VectorDBError(SmritiError):
    """Raised when there's an issue with vector database operations."""
    pass


class LLMError(SmritiError):
    """Raised when there's an issue with LLM operations."""
    pass


class ValidationError(SmritiError):
    """Raised when input validation fails."""
    pass 