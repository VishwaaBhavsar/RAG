"""Tests for the dependency injection container."""

from __future__ import annotations

import pytest

from rag_framework.core import (
    Container,
    ContainerError,
    FakeEmbeddingProvider,
    FakeLLMProvider,
    FakeLoader,
    FakeMemory,
    FakeReranker,
    FakeTool,
    FakeVectorStore,
    ProviderSelection,
    Registry,
    TenantConfig,
)


def test_container_builds_a_provider_graph_from_registry_factories() -> None:
    registry = Registry()
    llm = FakeLLMProvider(prefix="llm-openai")
    embedding = FakeEmbeddingProvider()
    vector_store = FakeVectorStore()
    loader = FakeLoader()
    reranker = FakeReranker()
    memory = FakeMemory()
    calculator = FakeTool(tool_name="calculator")
    translator = FakeTool(tool_name="translator")

    registry.register("llm", "openai", lambda: llm)
    registry.register("embedding", "bge", lambda: embedding)
    registry.register("vectordb", "qdrant", lambda: vector_store)
    registry.register("loader", "pdf", lambda: loader)
    registry.register("reranker", "default", lambda: reranker)
    registry.register("memory", "default", lambda: memory)
    registry.register("tool", "calculator", lambda: calculator)
    registry.register("tool", "translator", lambda: translator)

    config = TenantConfig(
        llm=ProviderSelection(provider="openai"),
        embedding=ProviderSelection(provider="bge"),
        vectordb=ProviderSelection(provider="qdrant"),
        loader=ProviderSelection(provider="pdf"),
        tools=(
            ProviderSelection(provider="calculator"),
            ProviderSelection(provider="translator"),
        ),
        reranker=ProviderSelection(provider="default"),
        memory=ProviderSelection(provider="default"),
    )

    graph = Container(registry).build(config)

    assert graph.llm is llm
    assert graph.embedding is embedding
    assert graph.vector_store is vector_store
    assert graph.loader is loader
    assert graph.reranker is reranker
    assert graph.memory is memory
    assert graph.tools == (calculator, translator)


def test_container_raises_when_a_required_provider_is_missing() -> None:
    registry = Registry()
    config = TenantConfig(
        llm=ProviderSelection(provider="openai"),
        embedding=ProviderSelection(provider="bge"),
        vectordb=ProviderSelection(provider="qdrant"),
    )

    with pytest.raises(ContainerError):
        Container(registry).build(config)

