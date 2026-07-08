"""Provider factory registry.

Purpose:
    Store and retrieve provider factories by provider type and provider name.

Responsibilities:
    - Provide a single source of truth for provider factory lookup.
    - Reject duplicate registrations deterministically.
    - Keep provider selection data-driven instead of hardcoded.

Usage example:
    registry = Registry()
    registry.register("llm", "openai", lambda: "openai")
    factory = registry.get_factory("llm", "openai")
    assert factory() == "openai"
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, TypeAlias

Factory: TypeAlias = Callable[[], object]


class RegistryError(Exception):
    """Base class for registry errors."""


class RegistryDuplicateError(RegistryError):
    """Raised when attempting to register an existing provider key."""


class RegistryNotFoundError(RegistryError):
    """Raised when a provider lookup misses."""


@dataclass(frozen=True, slots=True)
class RegisteredFactory:
    """A provider factory stored in the registry."""

    provider_type: str
    provider_name: str
    factory: Factory


class Registry:
    """Register and resolve provider factories by type and name."""

    def __init__(self) -> None:
        self._providers: dict[str, dict[str, Factory]] = {}

    def register(self, provider_type: str, provider_name: str, factory: Factory) -> None:
        """Register a provider factory under a type and name."""

        normalized_type = self._normalize_key(provider_type, "provider_type")
        normalized_name = self._normalize_key(provider_name, "provider_name")

        providers_for_type = self._providers.setdefault(normalized_type, {})
        if normalized_name in providers_for_type:
            raise RegistryDuplicateError(
                f"Provider already registered for type '{normalized_type}' and name '{normalized_name}'"
            )
        providers_for_type[normalized_name] = factory

    def get_factory(self, provider_type: str, provider_name: str) -> Factory:
        """Return the registered factory for a provider type and name."""

        normalized_type = self._normalize_key(provider_type, "provider_type")
        normalized_name = self._normalize_key(provider_name, "provider_name")

        try:
            return self._providers[normalized_type][normalized_name]
        except KeyError as exc:
            raise RegistryNotFoundError(
                f"No provider registered for type '{normalized_type}' and name '{normalized_name}'"
            ) from exc

    def create(self, provider_type: str, provider_name: str) -> object:
        """Instantiate the provider registered for a type and name."""

        return self.get_factory(provider_type, provider_name)()

    def _normalize_key(self, value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return value.strip().lower()


def register_default_llm_providers(registry: Registry) -> None:
    """Register the built-in fake and Ollama LLM providers.

    The active provider remains selectable through config/env by choosing the
    provider name (for example, ``fake`` or ``ollama``).
    """

    from .fakes import FakeLLMProvider
    from rag_framework.providers.ollama_llm import OllamaLLMProvider

    registry.register("llm", "fake", lambda: FakeLLMProvider())
    registry.register("llm", "ollama", lambda: OllamaLLMProvider())


def register_default_embedding_providers(registry: Registry) -> None:
    """Register the built-in embedding providers."""

    from .fakes import FakeEmbeddingProvider
    from rag_framework.providers.sentence_transformers_embeddings import SentenceTransformersEmbeddingProvider

    registry.register("embeddings", "fake", lambda: FakeEmbeddingProvider())
    registry.register("embeddings", "sentence-transformers", lambda: SentenceTransformersEmbeddingProvider())



def register_default_vector_store_providers(registry: Registry) -> None:
    """Register the built-in vector store providers."""

    from rag_framework.providers.chroma_vector_store import ChromaVectorStore
    from rag_framework.providers.in_memory_vector_store import InMemoryVectorStore

    registry.register("vectorstore", "chroma", lambda: ChromaVectorStore())
    registry.register("vectorstore", "in-memory", lambda: InMemoryVectorStore())
