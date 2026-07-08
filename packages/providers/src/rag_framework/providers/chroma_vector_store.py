"""ChromaDB-backed vector store provider."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from rag_framework.core.contracts import BaseVectorStore, Document, VectorRecord, VectorSearchResult


class ChromaVectorStoreError(RuntimeError):
    """Raised when ChromaDB vector storage cannot be used."""


@dataclass(frozen=True, slots=True)
class ChromaVectorStoreConfig:
    """Configuration for the local persistent ChromaDB store."""

    persist_path: str = ".chroma_data"
    collection_name: str = "rag_documents"


class ChromaVectorStore(BaseVectorStore):
    """Persist vectors and documents in a local ChromaDB collection."""

    def __init__(self, persist_path: str | None = None, collection_name: str = "rag_documents") -> None:
        self.config = ChromaVectorStoreConfig(
            persist_path=persist_path or os.getenv("RAG_FRAMEWORK_CHROMA__PATH", ".chroma_data"),
            collection_name=collection_name,
        )
        self._collection = self._load_collection()

    def count(self) -> int:
        return int(self._collection.count())

    def upsert(self, records: Sequence[VectorRecord]) -> None:
        if not records:
            return

        self._collection.upsert(
            ids=[record.id for record in records],
            embeddings=[list(record.embedding) for record in records],
            documents=[record.document.content for record in records],
            metadatas=[_metadata_to_chroma(record.document.metadata) for record in records],
        )

    def query(self, embedding: Sequence[float], *, top_k: int = 5) -> list[VectorSearchResult]:
        if self.count() == 0:
            return []

        result = self._collection.query(
            query_embeddings=[list(float(value) for value in embedding)],
            n_results=top_k,
            include=["documents", "metadatas", "distances", "embeddings"],
        )
        ids = result.get("ids", [[]])[0]
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        embeddings = result.get("embeddings", [[]])[0]

        search_results: list[VectorSearchResult] = []
        for index, record_id in enumerate(ids):
            document = Document(
                content=documents[index] if index < len(documents) and documents[index] is not None else "",
                metadata=_metadata_from_chroma(metadatas[index] if index < len(metadatas) else {}),
            )
            record_embedding = tuple(float(value) for value in embeddings[index]) if index < len(embeddings) else tuple()
            distance = float(distances[index]) if index < len(distances) else 1.0
            search_results.append(
                VectorSearchResult(
                    record=VectorRecord(id=str(record_id), embedding=record_embedding, document=document),
                    score=1.0 - distance,
                )
            )
        return search_results

    def _load_collection(self):
        try:
            import chromadb
        except ImportError as exc:  # pragma: no cover - depends on local install
            raise ChromaVectorStoreError(
                "chromadb is not installed. Install project dependencies or set "
                "RAG_FRAMEWORK_VECTORSTORE__PROVIDER=in-memory for fast local tests."
            ) from exc

        Path(self.config.persist_path).mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=self.config.persist_path)
        return client.get_or_create_collection(
            name=self.config.collection_name,
            metadata={"hnsw:space": "cosine"},
        )


def _metadata_to_chroma(metadata: object) -> dict[str, str | int | float | bool]:
    return {"metadata_json": json.dumps(metadata, sort_keys=True, default=str)}


def _metadata_from_chroma(metadata: dict[str, Any] | None) -> dict[str, Any]:
    if not metadata:
        return {}
    metadata_json = metadata.get("metadata_json")
    if not isinstance(metadata_json, str):
        return {}
    try:
        loaded_metadata = json.loads(metadata_json)
    except json.JSONDecodeError:
        return {}
    return loaded_metadata if isinstance(loaded_metadata, dict) else {}
