"""Core chat engine.

Purpose:
    Provide a single chat-facing interface on top of the RAG pipeline.

Responsibilities:
    - Delegate generation to the pipeline.
    - Optionally persist user and assistant turns to memory.
    - Offer a small API that future app entry points can call directly.

Usage example:
    chat = ChatEngine(provider_graph)
    response = chat.answer("session-1", "What is in the document?")
"""

from __future__ import annotations

from dataclasses import dataclass

from .contracts import ChatMessage
from .di_container import ProviderGraph
from .pipeline import RAGPipeline, RAGResponse


@dataclass(slots=True)
class ChatEngine:
    """Chat interface that wraps the RAG pipeline."""

    provider_graph: ProviderGraph
    pipeline: RAGPipeline | None = None

    def __post_init__(self) -> None:
        if self.pipeline is None:
            self.pipeline = RAGPipeline(self.provider_graph)

    def answer(self, session_id: str, prompt: str) -> RAGResponse:
        """Answer a chat prompt and optionally record the exchange in memory."""

        if self.provider_graph.memory is not None:
            self.provider_graph.memory.append(session_id, ChatMessage(role="user", content=prompt))

        assert self.pipeline is not None
        response = self.pipeline.run(prompt)

        if self.provider_graph.memory is not None:
            self.provider_graph.memory.append(
                session_id,
                ChatMessage(role="assistant", content=response.answer),
            )

        return response
