"""Integration tests for real cross-encoder reranking."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from apps.api.src.server import create_app


QUERY = "What forms of payment can I use?"
LEXICAL_DECOY = (
    "Payment methods, checkout, cards, cash, UPI, payment options, "
    "and order billing are described generally."
)
BETTER_ANSWER = "You can pay with UPI, debit cards, credit cards, or cash on delivery."


def _client_with_reranker(monkeypatch, reranker_provider: str) -> TestClient:
    monkeypatch.setenv("RAG_FRAMEWORK_LLM__PROVIDER", "fake")
    monkeypatch.setenv("RAG_FRAMEWORK_EMBEDDINGS__PROVIDER", "sentence-transformers")
    monkeypatch.setenv("RAG_FRAMEWORK_VECTORSTORE__PROVIDER", "in-memory")
    monkeypatch.setenv("RAG_FRAMEWORK_RERANKER__PROVIDER", reranker_provider)
    return TestClient(create_app())


def _ingest_test_documents(client: TestClient) -> None:
    decoy_response = client.post(
        "/ingest",
        json={"text": LEXICAL_DECOY, "source": "lexical-decoy"},
    )
    answer_response = client.post(
        "/ingest",
        json={"text": BETTER_ANSWER, "source": "refund-answer"},
    )

    assert decoy_response.status_code == 200
    assert answer_response.status_code == 200


@pytest.mark.integration
def test_cross_encoder_promotes_better_answer_over_vector_only_match(monkeypatch) -> None:
    """Use real embeddings and the real cross-encoder reranker.

    The lexical decoy is a generic topical passage that real vector retrieval
    ranks first for this query. The better answer lists actual payment methods;
    the real cross-encoder should promote it.
    """

    pytest.importorskip("sentence_transformers")

    vector_only_client = _client_with_reranker(monkeypatch, "none")
    _ingest_test_documents(vector_only_client)

    vector_only_response = vector_only_client.post("/chat", json={"question": QUERY, "top_k": 1})

    assert vector_only_response.status_code == 200
    assert vector_only_response.json()["documents"][0]["content"] == LEXICAL_DECOY

    reranked_client = _client_with_reranker(monkeypatch, "cross-encoder")
    _ingest_test_documents(reranked_client)

    reranked_response = reranked_client.post("/chat", json={"question": QUERY, "top_k": 1})

    assert reranked_response.status_code == 200
    assert reranked_response.json()["documents"][0]["content"] == BETTER_ANSWER
