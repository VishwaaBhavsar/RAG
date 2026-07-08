"""End-to-end tests for the core RAG pipeline and chat engine."""

from __future__ import annotations

from rag_framework.core import (
    ChatEngine,
    Container,
    Document,
    FakeEmbeddingProvider,
    FakeLLMProvider,
    FakeMemory,
    FakeVectorStore,
    ProviderSelection,
    Registry,
    TenantConfig,
    VectorRecord,
)


def test_chat_engine_runs_retrieval_context_assembly_and_generation() -> None:
    registry = Registry()
    llm = FakeLLMProvider(prefix="answer")
    embedding = FakeEmbeddingProvider()
    vector_store = FakeVectorStore()
    memory = FakeMemory()

    vector_store.upsert(
        [
            VectorRecord(
                id="doc-1",
                embedding=(1.0, 2.0),
                document=Document(
                    content="relevant document about retrieval",
                    metadata={"source": "fixture"},
                ),
            )
        ]
    )

    registry.register("llm", "fake", lambda: llm)
    registry.register("embedding", "fake", lambda: embedding)
    registry.register("vectordb", "fake", lambda: vector_store)
    registry.register("memory", "fake", lambda: memory)

    graph = Container(registry).build(
        TenantConfig(
            llm=ProviderSelection(provider="fake"),
            embedding=ProviderSelection(provider="fake"),
            vectordb=ProviderSelection(provider="fake"),
            memory=ProviderSelection(provider="fake"),
        )
    )

    response = ChatEngine(graph).answer("session-1", "What is in the document?")

    assert response.documents[0].content == "relevant document about retrieval"
    assert response.context == "relevant document about retrieval"
    assert response.answer.startswith("answer:Question: What is in the document?")
    assert "relevant document about retrieval" in response.answer
    assert memory.get("session-1")[0].content == "What is in the document?"
    assert memory.get("session-1")[1].role == "assistant"
