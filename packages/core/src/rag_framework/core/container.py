"""Dependency injection container.

Purpose:
    Build a provider graph for a tenant from typed config and registry factories.

Responsibilities:
    - Resolve all provider instances through the registry.
    - Keep provider selection data-driven.
    - Assemble a request- or tenant-scoped graph without importing concrete providers.

Usage example:
    container = Container(registry)
    graph = container.build(tenant_config)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from .config import ProviderSelection, TenantConfig
from .contracts import (
    BaseEmbeddingProvider,
    BaseLLMProvider,
    BaseLoader,
    BaseMemory,
    BaseReranker,
    BaseTool,
    BaseVectorStore,
)
from .registry import Registry, RegistryError


@dataclass(frozen=True, slots=True)
class ProviderGraph:
    """Instantiated providers for a tenant."""

    llm: BaseLLMProvider
    embedding: BaseEmbeddingProvider
    vector_store: BaseVectorStore
    loader: BaseLoader | None
    tools: tuple[BaseTool, ...]
    reranker: BaseReranker | None
    memory: BaseMemory | None


class ContainerError(Exception):
    """Base class for dependency injection errors."""


class Container:
    """Build provider graphs from tenant configuration."""

    def __init__(self, registry: Registry) -> None:
        self._registry = registry

    def build(self, config: TenantConfig) -> ProviderGraph:
        """Resolve a provider graph for a tenant config."""

        llm = cast(BaseLLMProvider, self._resolve_required("llm", config.llm))
        embedding = cast(BaseEmbeddingProvider, self._resolve_required("embedding", config.embedding))
        vector_store = cast(BaseVectorStore, self._resolve_required("vectordb", config.vectordb))
        loader = cast(BaseLoader | None, self._resolve_optional("loader", config.loader))
        reranker = cast(BaseReranker | None, self._resolve_optional("reranker", config.reranker))
        memory = cast(BaseMemory | None, self._resolve_optional("memory", config.memory))
        tools = tuple(
            cast(BaseTool, self._resolve_required("tool", tool_selection))
            for tool_selection in config.tools
        )

        return ProviderGraph(
            llm=llm,
            embedding=embedding,
            vector_store=vector_store,
            loader=loader,
            tools=tools,
            reranker=reranker,
            memory=memory,
        )

    def _resolve_required(self, provider_type: str, selection: ProviderSelection) -> object:
        provider_name = self._normalize_selection(selection, provider_type)
        try:
            return self._registry.create(provider_type, provider_name)
        except RegistryError as exc:
            raise ContainerError(
                f"Unable to resolve required provider '{provider_type}:{provider_name}'"
            ) from exc

    def _resolve_optional(
        self,
        provider_type: str,
        selection: ProviderSelection | None,
    ) -> object | None:
        if selection is None:
            return None
        provider_name = self._normalize_selection(selection, provider_type)
        try:
            return self._registry.create(provider_type, provider_name)
        except RegistryError as exc:
            raise ContainerError(
                f"Unable to resolve optional provider '{provider_type}:{provider_name}'"
            ) from exc

    def _normalize_selection(self, selection: ProviderSelection, provider_type: str) -> str:
        if not isinstance(selection.provider, str) or not selection.provider.strip():
            raise ContainerError(f"Provider selection for '{provider_type}' must be a non-empty string")
        return selection.provider.strip()
