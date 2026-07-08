"""Integration tests for real semantic retrieval."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from apps.api.src.server import create_app


@pytest.mark.integration
def test_sentence_transformers_retrieves_dog_document_for_canine_query(monkeypatch) -> None:
    """Use the real embedding provider to prove semantic retrieval works.

    This intentionally avoids a hand-written fake embedding provider. It may
    download/load the configured sentence-transformers model, so normal pytest
    runs exclude it through the default marker config. Run explicitly with:

        pytest -m integration tests/integration/test_semantic_retrieval.py -v
    """

    pytest.importorskip("sentence_transformers")

    monkeypatch.setenv("RAG_FRAMEWORK_LLM__PROVIDER", "fake")
    monkeypatch.setenv("RAG_FRAMEWORK_EMBEDDINGS__PROVIDER", "sentence-transformers")

    client = TestClient(create_app())

    cake_response = client.post(
        "/ingest",
        json={
            "text": "Chocolate cake recipes use sugar, flour, butter, and frosting.",
            "source": "cake-note",
        },
    )
    dog_response = client.post(
        "/ingest",
        json={
            "text": "Dogs are loyal animals that enjoy walks, play, and training.",
            "source": "dog-note",
        },
    )

    assert cake_response.status_code == 200
    assert dog_response.status_code == 200

    response = client.post("/chat", json={"question": "canine companions", "top_k": 1})

    assert response.status_code == 200
    assert response.json()["documents"][0]["content"] == (
        "Dogs are loyal animals that enjoy walks, play, and training."
    )
