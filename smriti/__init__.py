"""
Smriti Memory - An intelligent memory layer for AI applications with RAG capabilities.

This package provides a sophisticated memory system that can store, retrieve, and update
contextual information for AI applications using vector databases and LLM-powered decision making.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .memory_manager import MemoryManager
from .config import MemoryConfig
from .exceptions import SmritiError, MemoryError, ConfigurationError

__all__ = [
    "MemoryManager",
    "MemoryConfig", 
    "SmritiError",
    "MemoryError",
    "ConfigurationError",
    "__version__",
] 