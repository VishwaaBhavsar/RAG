"""Integration tests for multilingual semantic retrieval."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from apps.api.src.server import create_app


@pytest.mark.integration
def test_multilingual_embeddings_retrieve_hindi_document_for_related_hindi_query(monkeypatch) -> None:
    """Use the real multilingual embedding model for a Hindi semantic match."""

    pytest.importorskip("sentence_transformers")

    monkeypatch.setenv("RAG_FRAMEWORK_LLM__PROVIDER", "fake")
    monkeypatch.setenv("RAG_FRAMEWORK_EMBEDDINGS__PROVIDER", "multilingual")
    monkeypatch.setenv("RAG_FRAMEWORK_VECTORSTORE__PROVIDER", "in-memory")
    monkeypatch.setenv("RAG_FRAMEWORK_RERANKER__PROVIDER", "none")

    client = TestClient(create_app())

    target_response = client.post(
        "/ingest",
        json={
            "text": "कुत्ते वफादार साथी होते हैं। उन्हें सैर, खेल और प्रशिक्षण पसंद होता है।",
            "source": "hindi-dog-note",
        },
    )
    decoy_response = client.post(
        "/ingest",
        json={
            "text": "चॉकलेट केक में आटा, चीनी, मक्खन और फ्रॉस्टिंग होती है।",
            "source": "hindi-cake-note",
        },
    )

    assert target_response.status_code == 200
    assert decoy_response.status_code == 200

    response = client.post("/chat", json={"question": "वफादार पालतू जो टहलना और प्रशिक्षण पसंद करे", "top_k": 1})

    assert response.status_code == 200
    assert response.json()["documents"][0]["metadata"]["source"] == "hindi-dog-note"