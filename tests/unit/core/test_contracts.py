"""Tests for the core provider contracts and fake implementations."""

from __future__ import annotations

from pathlib import Path

from rag_framework.core import (
    ChatMessage,
    Document,
    FakeEmbeddingProvider,
    FakeLLMProvider,
    FakeLoader,
    FakeMemory,
    FakeReranker,
    FakeTool,
    FakeVectorStore,
    VectorRecord,
)


def test_fake_llm_provider_generates_deterministic_output() -> None:
    provider = FakeLLMProvider()

    assert provider.generate("hello") == "fake-response:hello"


def test_fake_embedding_provider_returns_position_based_embeddings() -> None:
    provider = FakeEmbeddingProvider()

    assert provider.embed(["alpha", "beta"]) == [[5.0, 0.0], [4.0, 1.0]]


def test_fake_vector_store_upsert_and_query() -> None:
    store = FakeVectorStore()
    record_one = VectorRecord(
        id="1",
        embedding=(1.0, 2.0),
        document=Document(content="first", metadata={"rank": 1}),
    )
    record_two = VectorRecord(
        id="2",
        embedding=(3.0, 4.0),
        document=Document(content="second", metadata={"rank": 2}),
    )

    store.upsert([record_one, record_two])
    results = store.query([0.5, 0.5], top_k=1)

    assert results[0].record == record_one
    assert results[0].score == 1.0


def test_fake_loader_returns_documents_from_source() -> None:
    loader = FakeLoader()

    assert loader.load(Path("sample.txt")) == [
        Document(content="sample.txt", metadata={"source": "sample.txt"})
    ]


def test_fake_reranker_orders_by_document_length() -> None:
    reranker = FakeReranker()
    documents = [
        Document(content="tiny", metadata={}),
        Document(content="much longer", metadata={}),
    ]

    assert reranker.rerank("query", documents) == [
        Document(content="much longer", metadata={}),
        Document(content="tiny", metadata={}),
    ]


def test_fake_tool_uses_context_size_in_output() -> None:
    tool = FakeTool(tool_name="calc")

    assert tool.run("2+2", context={"a": 1, "b": 2}) == "calc:2+2:2"


def test_fake_memory_stores_and_returns_messages() -> None:
    memory = FakeMemory()
    message = ChatMessage(role="user", content="hello")

    memory.append("session-1", message)

    assert memory.get("session-1") == [message]
    assert memory.get("missing") == []

