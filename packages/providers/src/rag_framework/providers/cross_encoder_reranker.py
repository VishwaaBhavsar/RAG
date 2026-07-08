"""Cross-encoder reranker provider."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from rag_framework.core.contracts import BaseReranker, Document


class CrossEncoderRerankerError(RuntimeError):
    """Raised when cross-encoder reranking cannot be performed."""


@dataclass(frozen=True, slots=True)
class CrossEncoderRerankerConfig:
    """Configuration for the sentence-transformers cross-encoder reranker."""

    model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class CrossEncoderReranker(BaseReranker):
    """Rerank retrieved documents with a sentence-transformers cross-encoder."""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> None:
        self.config = CrossEncoderRerankerConfig(model_name=model_name)
        self._model = None

    def rerank(self, query: str, documents: Sequence[Document]) -> list[Document]:
        if not documents:
            return []

        model = self._load_model()
        pairs = [(query, document.content) for document in documents]
        scores = model.predict(pairs)
        scored_documents = [
            (float(score), -index, document)
            for index, (score, document) in enumerate(zip(scores, documents))
        ]
        scored_documents.sort(reverse=True)
        return [document for _, _, document in scored_documents]

    def _load_model(self):
        if self._model is not None:
            return self._model

        try:
            from sentence_transformers import CrossEncoder
        except ImportError as exc:  # pragma: no cover - depends on optional local install
            raise CrossEncoderRerankerError(
                "sentence-transformers is not installed. Install the embeddings extra or set "
                "RAG_FRAMEWORK_RERANKER__PROVIDER=none."
            ) from exc

        self._model = CrossEncoder(self.config.model_name)
        return self._model
