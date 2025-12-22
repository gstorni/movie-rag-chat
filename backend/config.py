"""
Configuration management for the RAG application.
Loads environment variables and provides typed config access.
"""

import os
from dotenv import load_dotenv

# Load .env from parent directory (shared with main app)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

class Config:
    """Application configuration loaded from environment variables."""

    # Database - Use Docker network IP for supabase-db container
    _pg_host = os.getenv('RAG_POSTGRES_HOST') or os.getenv('POSTGRES_HOST', '172.19.0.8')
    POSTGRES_HOST: str = '172.19.0.8' if _pg_host in ('db', '192.168.10.158') else _pg_host
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'postgres')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'pyzsMzRH20kil9H3Qv7TieinQgEodWH6')

    # OpenAI
    OPENAI_API_KEY: str = os.getenv('VITE_OPENAI_API_KEY', '')
    EMBEDDING_MODEL: str = 'text-embedding-3-small'
    CHAT_MODEL: str = 'gpt-4o-mini'

    # Vector Search
    EMBEDDING_DIMENSIONS: int = 1536
    VECTOR_SIMILARITY_THRESHOLD: float = 0.7
    MAX_VECTOR_RESULTS: int = 5

    # Server
    API_HOST: str = '0.0.0.0'
    API_PORT: int = 8080

    @classmethod
    def get_database_url(cls) -> str:
        """Build PostgreSQL connection URL."""
        return f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"


config = Config()
