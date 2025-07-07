"""
Configuration management for Smriti Memory.
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from .exceptions import ConfigurationError


@dataclass
class MemoryConfig:
    """Configuration for the Smriti Memory system."""
    
    # Vector Database Configuration
    pinecone_api_key: Optional[str] = None
    pinecone_environment: str = "us-east-1"
    pinecone_cloud: str = "aws"
    
    # LLM Configuration
    groq_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    llm_model: str = "llama-3.1-8b-instant"
    llm_temperature: float = 0.3
    
    # Memory Configuration
    default_namespace: str = "user_understanding"
    max_memory_length: int = 1000
    similarity_threshold: float = 0.7
    max_search_results: int = 10
    
    # Embedding Configuration
    embedding_model: str = "models/embedding-001"
    
    # System Configuration
    enable_logging: bool = True
    log_level: str = "INFO"
    
    def __post_init__(self):
        """Load configuration from environment variables if not provided."""
        self._load_from_env()
        self._validate_config()
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        if not self.pinecone_api_key:
            self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        
        if not self.groq_api_key:
            self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        if not self.gemini_api_key:
            self.gemini_api_key = os.getenv("GEMINI_KEY")
    
    def _validate_config(self):
        """Validate the configuration."""
        required_keys = [
            ("pinecone_api_key", "PINECONE_API_KEY"),
            ("groq_api_key", "GROQ_API_KEY"),
            ("gemini_api_key", "GEMINI_KEY"),
        ]
        
        missing_keys = []
        for attr_name, env_name in required_keys:
            if not getattr(self, attr_name):
                missing_keys.append(f"{env_name} (or set {attr_name})")
        
        if missing_keys:
            raise ConfigurationError(
                f"Missing required configuration: {', '.join(missing_keys)}"
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "pinecone_api_key": self.pinecone_api_key,
            "pinecone_environment": self.pinecone_environment,
            "pinecone_cloud": self.pinecone_cloud,
            "groq_api_key": self.groq_api_key,
            "gemini_api_key": self.gemini_api_key,
            "llm_model": self.llm_model,
            "llm_temperature": self.llm_temperature,
            "default_namespace": self.default_namespace,
            "max_memory_length": self.max_memory_length,
            "similarity_threshold": self.similarity_threshold,
            "max_search_results": self.max_search_results,
            "embedding_model": self.embedding_model,
            "enable_logging": self.enable_logging,
            "log_level": self.log_level,
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "MemoryConfig":
        """Create configuration from dictionary."""
        return cls(**config_dict) 