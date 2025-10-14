from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    project_name: str = "Builda API"
    environment: str = "development"
    backend_cors_origins: List[str] = ["http://localhost:3000"]

    # External services
    openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_key: Optional[str] = None

    # Data stores
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/builda"
    redis_url: Optional[str] = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
