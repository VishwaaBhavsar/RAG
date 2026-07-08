"""Core RAG pipeline.

Purpose:
    Orchestrate retrieval, context assembly, and generation through the provider graph.

Responsibilities:
    - Embed the user prompt.
    - Retrieve the most relevant documents from the vector store.
    - Optionally rerank retrieved documents.
    - Build a deterministic context string.
    - Generate the final answer using the LLM provider.

Usage example:
    pipeline = RAGPipeline(provider_graph)
    response = pipeline.run("What does the document say?")
"""

from __future__ import annotations

from dataclasses import dataclass

from .contracts import BaseEmbeddingProvider, BaseReranker, Document
from .di_container import ProviderGraph


@dataclass(frozen=True, slots=True)
class RAGResponse:
    """Result of a RAG pipeline invocation."""

    answer: str
    documents: tuple[Document, ...]
    context: str


class RAGPipeline:
    """Run retrieval-augmented generation against a provider graph."""

    def __init__(self, provider_graph: ProviderGraph, *, top_k: int = 3) -> None:
        self._graph = provider_graph
        self._top_k = top_k

    def run(self, prompt: str) -> RAGResponse:
        """Answer a prompt using retrieval and generation."""

        query_embedding = self._embed_prompt(self._graph.embedding, prompt)
        results = self._graph.vector_store.query(query_embedding, top_k=self._top_k)
        documents = tuple(result.record.document for result in results)
        reranked_documents = self._rerank_documents(prompt, documents, self._graph.reranker)
        context = self._build_context(reranked_documents)
        generation_prompt = self._build_generation_prompt(prompt, context)
        answer = self._graph.llm.generate(generation_prompt, system_prompt=context)
        return RAGResponse(answer=answer, documents=reranked_documents, context=context)

    def _embed_prompt(self, embedding: BaseEmbeddingProvider, prompt: str) -> list[float]:
        embeddings = embedding.embed([prompt])
        if not embeddings:
            return []
        return embeddings[0]

    def _rerank_documents(
        self,
        prompt: str,
        documents: tuple[Document, ...],
        reranker: BaseReranker | None,
    ) -> tuple[Document, ...]:
        if reranker is None:
            return documents
        return tuple(reranker.rerank(prompt, documents))

    def _build_context(self, documents: tuple[Document, ...]) -> str:
        return "\n\n".join(document.content for document in documents)

    def _build_generation_prompt(self, prompt: str, context: str) -> str:
        return f"Question: {prompt}\n\nContext:\n{context}"
