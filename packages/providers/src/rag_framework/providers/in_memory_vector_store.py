"""In-memory vector store provider."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from rag_framework.core.contracts import BaseVectorStore, Document, VectorRecord, VectorSearchResult


def _cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if not left or not right:
        return 0.0

    dot_product = sum(left_value * right_value for left_value, right_value in zip(left, right))
    left_magnitude = sum(value * value for value in left) ** 0.5
    right_magnitude = sum(value * value for value in right) ** 0.5
    if left_magnitude == 0.0 or right_magnitude == 0.0:
        return 0.0
    return dot_product / (left_magnitude * right_magnitude)


@dataclass(slots=True)
class InMemoryVectorStore(BaseVectorStore):
    """Store vectors in process memory for fast tests and smoke runs."""

    records: list[VectorRecord] = field(default_factory=list)

    @property
    def documents(self) -> list[Document]:
        return [record.document for record in self.records]

    def count(self) -> int:
        return len(self.records)

    def upsert(self, records: Sequence[VectorRecord]) -> None:
        records_by_id = {record.id: record for record in self.records}
        for record in records:
            records_by_id[record.id] = record
        self.records = list(records_by_id.values())

    def query(self, embedding: Sequence[float], *, top_k: int = 5) -> list[VectorSearchResult]:
        scored_records = [
            (
                _cosine_similarity(embedding, record.embedding),
                -index,
                record,
            )
            for index, record in enumerate(self.records)
        ]
        scored_records.sort(reverse=True)
        return [
            VectorSearchResult(record=record, score=score)
            for score, _, record in scored_records[:top_k]
        ]
