"""Core provider contracts.

Purpose:
    Define the abstract interfaces that all provider implementations must follow.

Responsibilities:
    - Keep the core engine decoupled from concrete providers.
    - Provide stable, typed behavior contracts for later packages.
    - Establish shared data models for documents, messages, and vector records.

Usage example:
    class MyLLM(BaseLLMProvider):
        def generate(self, prompt: str, *, system_prompt: str | None = None) -> str:
            return "..."
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class Document:
    """A text document and its metadata."""

    content: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ChatMessage:
    """A single chat message stored in memory or passed to language models."""

    role: str
    content: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class VectorRecord:
    """A document paired with an embedding vector."""

    id: str
    embedding: tuple[float, ...]
    document: Document


@dataclass(frozen=True, slots=True)
class VectorSearchResult:
    """A ranked vector-store search result."""

    record: VectorRecord
    score: float


class BaseLLMProvider(ABC):
    """Abstract interface for text-generation providers."""

    @abstractmethod
    def generate(self, prompt: str, *, system_prompt: str | None = None) -> str:
        """Generate a response for the supplied prompt."""


class BaseEmbeddingProvider(ABC):
    """Abstract interface for embedding providers."""

    @abstractmethod
    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Return embeddings for each input text."""


class BaseVectorStore(ABC):
    """Abstract interface for vector stores."""

    @abstractmethod
    def upsert(self, records: Sequence[VectorRecord]) -> None:
        """Persist vector records in the store."""

    @abstractmethod
    def query(self, embedding: Sequence[float], *, top_k: int = 5) -> list[VectorSearchResult]:
        """Retrieve the best matching records for an embedding."""


class BaseLoader(ABC):
    """Abstract interface for document loaders."""

    @abstractmethod
    def load(self, source: str | Path) -> list[Document]:
        """Load documents from a source path or identifier."""


class BaseReranker(ABC):
    """Abstract interface for rerankers."""

    @abstractmethod
    def rerank(self, query: str, documents: Sequence[Document]) -> list[Document]:
        """Return documents in reranked order for the given query."""


class BaseTool(ABC):
    """Abstract interface for tool execution."""

    @abstractmethod
    def run(self, input_text: str, *, context: Mapping[str, Any] | None = None) -> str:
        """Run the tool and return a textual result."""


class BaseMemory(ABC):
    """Abstract interface for conversational memory."""

    @abstractmethod
    def append(self, session_id: str, message: ChatMessage) -> None:
        """Store a message for a session."""

    @abstractmethod
    def get(self, session_id: str) -> list[ChatMessage]:
        """Return messages stored for a session."""

