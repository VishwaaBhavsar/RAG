from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Load the repo-root .env so runtime overrides like REQUEST_TIMEOUT_SECONDS apply.
        env_file=str(Path(__file__).resolve().parents[2] / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    LLM_PROVIDER: str = "ollama"

    ANTHROPIC_API_KEY: str | None = None
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-latest"
    ANTHROPIC_BASE_URL: str | None = None

    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4.1-mini"
    OPENAI_BASE_URL: str | None = None

    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    GUARD_UPPER_THRESHOLD: float = 0.62
    GUARD_LOWER_THRESHOLD: float = 0.35

    LOG_LEVEL: str = "INFO"
    REQUEST_TIMEOUT_SECONDS: float = 900.0
    MAX_RETRIES: int = 1
    RATE_LIMIT_PER_MINUTE: int = 30
    MAX_TOKENS: int = 512


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
