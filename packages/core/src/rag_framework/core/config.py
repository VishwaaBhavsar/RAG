"""Core configuration models.

Purpose:
    Define the typed config objects used by the core container and future config loaders.

Responsibilities:
    - Represent provider selections in a typed, framework-owned way.
    - Keep tenant configuration independent from any specific config source.
    - Provide stable models for later YAML and database resolution.

Usage example:
    tenant = TenantConfig(llm=ProviderSelection(provider="openai"), ...)
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ProviderSelection:
    """A selected provider name for a single component slot."""

    provider: str


@dataclass(frozen=True, slots=True)
class TenantConfig:
    """Typed tenant configuration used by the DI container."""

    llm: ProviderSelection
    embedding: ProviderSelection
    vectordb: ProviderSelection
    loader: ProviderSelection | None = None
    tools: tuple[ProviderSelection, ...] = field(default_factory=tuple)
    reranker: ProviderSelection | None = None
    memory: ProviderSelection | None = None

