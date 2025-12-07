"""
Configuration management for the chatbot backend.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini API Configuration
    gemini_api_key: str
    embedding_model: str = "models/text-embedding-004"
    generation_model: str = "gemini-2.5-flash"
    
    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "humanoid_robotics_book"
    
    # Database Configuration
    database_url: str
    
    # Application Configuration
    app_env: str = "development"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Book Content Path
    book_docs_path: str = "../../humanoid-robotics-book/docs"
    
    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    similarity_threshold: float = 0.5
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
