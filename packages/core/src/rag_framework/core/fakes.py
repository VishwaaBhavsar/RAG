"""In-memory fake provider implementations.

Purpose:
    Provide deterministic test doubles for the core provider contracts.

Responsibilities:
    - Allow unit tests to exercise the contracts without real integrations.
    - Keep behavior simple and predictable.
    - Demonstrate how later real providers should satisfy the ABCs.

Usage example:
    fake_llm = FakeLLMProvider()
    assert fake_llm.generate("hello") == "fake-response:hello"
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from .contracts import (
    BaseEmbeddingProvider,
    BaseLLMProvider,
    BaseLoader,
    BaseMemory,
    BaseReranker,
    BaseTool,
    BaseVectorStore,
    ChatMessage,
    Document,
    VectorRecord,
    VectorSearchResult,
)


@dataclass(slots=True)
class FakeLLMProvider(BaseLLMProvider):
    """Deterministic LLM fake used only in tests."""

    prefix: str = "fake-response"

    def generate(self, prompt: str, *, system_prompt: str | None = None) -> str:
        return f"{self.prefix}:{prompt}"


@dataclass(slots=True)
class FakeEmbeddingProvider(BaseEmbeddingProvider):
    """Deterministic embedding fake used only in tests."""

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [[float(len(text)), float(index)] for index, text in enumerate(texts)]


@dataclass(slots=True)
class FakeVectorStore(BaseVectorStore):
    """In-memory vector store fake used only in tests."""

    records: list[VectorRecord] = field(default_factory=list)

    def upsert(self, records: Sequence[VectorRecord]) -> None:
        self.records.extend(records)

    def query(self, embedding: Sequence[float], *, top_k: int = 5) -> list[VectorSearchResult]:
        limited_records = self.records[:top_k]
        return [
            VectorSearchResult(record=record, score=1.0 / (index + 1))
            for index, record in enumerate(limited_records)
        ]


@dataclass(slots=True)
class FakeLoader(BaseLoader):
    """In-memory loader fake used only in tests."""

    def load(self, source: str | Path) -> list[Document]:
        text = str(source)
        return [Document(content=text, metadata={"source": text})]


@dataclass(slots=True)
class FakeReranker(BaseReranker):
    """Deterministic reranker fake used only in tests."""

    def rerank(self, query: str, documents: Sequence[Document]) -> list[Document]:
        return sorted(documents, key=lambda document: len(document.content), reverse=True)


@dataclass(slots=True)
class FakeTool(BaseTool):
    """Deterministic tool fake used only in tests."""

    tool_name: str = "fake-tool"

    def run(self, input_text: str, *, context: Mapping[str, Any] | None = None) -> str:
        context_size = 0 if context is None else len(context)
        return f"{self.tool_name}:{input_text}:{context_size}"


@dataclass(slots=True)
class FakeMemory(BaseMemory):
    """In-memory chat memory fake used only in tests."""

    sessions: dict[str, list[ChatMessage]] = field(default_factory=dict)

    def append(self, session_id: str, message: ChatMessage) -> None:
        self.sessions.setdefault(session_id, []).append(message)

    def get(self, session_id: str) -> list[ChatMessage]:
        return list(self.sessions.get(session_id, []))

