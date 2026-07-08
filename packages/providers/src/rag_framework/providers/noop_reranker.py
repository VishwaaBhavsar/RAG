"""No-op reranker provider."""

from __future__ import annotations

from typing import Sequence

from rag_framework.core.contracts import BaseReranker, Document


class NoOpReranker(BaseReranker):
    """Return documents in their current order."""

    def rerank(self, query: str, documents: Sequence[Document]) -> list[Document]:
        return list(documents)
