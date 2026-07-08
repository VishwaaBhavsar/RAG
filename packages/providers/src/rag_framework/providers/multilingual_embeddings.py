"""Multilingual sentence-transformers embedding provider."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from rag_framework.core.contracts import BaseEmbeddingProvider


class MultilingualSentenceTransformersEmbeddingError(RuntimeError):
    """Raised when multilingual sentence-transformers embeddings cannot be generated."""


@dataclass(frozen=True, slots=True)
class MultilingualSentenceTransformersEmbeddingConfig:
    """Configuration for the multilingual sentence-transformers embedding provider."""

    model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


class MultilingualSentenceTransformersEmbeddingProvider(BaseEmbeddingProvider):
    """Generate embeddings with the multilingual sentence-transformers model."""

    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2") -> None:
        self.config = MultilingualSentenceTransformersEmbeddingConfig(model_name=model_name)
        self._model = None

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []

        model = self._load_model()
        embeddings = model.encode(list(texts), convert_to_numpy=False, normalize_embeddings=True)
        return [[float(value) for value in embedding] for embedding in embeddings]

    def _load_model(self):
        if self._model is not None:
            return self._model

        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover - depends on optional local install
            raise MultilingualSentenceTransformersEmbeddingError(
                "sentence-transformers is not installed. Install it or set "
                "RAG_FRAMEWORK_EMBEDDINGS__PROVIDER=fake for local smoke tests."
            ) from exc

        self._model = SentenceTransformer(self.config.model_name)
        return self._model