from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Sequence

import numpy as np
from sentence_transformers import SentenceTransformer

from chatbot.config.domain_config import TOPIC_EXAMPLES
from chatbot.config.settings import get_settings


@dataclass(frozen=True)
class GuardResult:
    on_topic: bool
    ambiguous: bool
    score: float
    matched_example: str | None


@lru_cache(maxsize=1)
def _load_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)


class EmbeddingGuard:
    def __init__(
        self,
        *,
        topic_examples: Sequence[str] | None = None,
        embedding_model: str | None = None,
        upper_threshold: float | None = None,
        lower_threshold: float | None = None,
    ) -> None:
        settings = get_settings()
        self.topic_examples = list(topic_examples or TOPIC_EXAMPLES)
        self.embedding_model_name = embedding_model or settings.EMBEDDING_MODEL
        self.upper_threshold = upper_threshold if upper_threshold is not None else settings.GUARD_UPPER_THRESHOLD
        self.lower_threshold = lower_threshold if lower_threshold is not None else settings.GUARD_LOWER_THRESHOLD
        self._model = _load_model(self.embedding_model_name)
        self._topic_embeddings = self._normalize(self._model.encode(self.topic_examples, convert_to_numpy=True, show_progress_bar=False))

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0.0] = 1.0
        return vectors / norms

    def classify(self, message: str) -> GuardResult:
        query_embedding = self._normalize(self._model.encode([message], convert_to_numpy=True, show_progress_bar=False))[0]
        similarities = self._topic_embeddings @ query_embedding
        best_index = int(np.argmax(similarities))
        best_score = float(similarities[best_index])
        matched_example = self.topic_examples[best_index]

        if best_score >= self.upper_threshold:
            return GuardResult(on_topic=True, ambiguous=False, score=best_score, matched_example=matched_example)
        if best_score < self.lower_threshold:
            return GuardResult(on_topic=False, ambiguous=False, score=best_score, matched_example=matched_example)
        return GuardResult(on_topic=False, ambiguous=True, score=best_score, matched_example=matched_example)

