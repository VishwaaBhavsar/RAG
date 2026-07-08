"""Tests for the FastAPI backend server."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.api.src import server as server_module
from apps.api.src.server import create_app
from rag_framework.core import Document
from rag_framework.providers.ollama_llm import OllamaLLMProvider


PDF_FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "documents" / "sample.pdf"


@pytest.fixture(autouse=True)
def default_fast_rag_providers(monkeypatch) -> None:
    monkeypatch.setenv("RAG_FRAMEWORK_EMBEDDINGS__PROVIDER", "fake")
    monkeypatch.setenv("RAG_FRAMEWORK_VECTORSTORE__PROVIDER", "in-memory")


def test_upload_a_pdf_and_ask_a_question(monkeypatch) -> None:
    monkeypatch.setenv("RAG_FRAMEWORK_LLM__PROVIDER", "ollama")
    monkeypatch.setattr(
        OllamaLLMProvider,
        "generate",
        lambda self, prompt, *, system_prompt=None: "mocked ollama answer",
    )

    client = TestClient(create_app())

    with PDF_FIXTURE.open("rb") as pdf_file:
        upload_response = client.post(
            "/documents/upload",
            files={"file": ("sample.pdf", pdf_file, "application/pdf")},
        )

    assert upload_response.status_code == 200
    assert upload_response.json()["ingested"] == 1
    assert upload_response.json()["total_documents"] == 1

    chat_response = client.post(
        "/chat",
        json={"question": "What is in the document?", "top_k": 3},
    )

    assert chat_response.status_code == 200
    assert chat_response.json()["answer"] == "mocked ollama answer"
    assert chat_response.json()["context"] == "relevant document about retrieval"
    assert chat_response.json()["documents"][0]["content"] == "relevant document about retrieval"


def test_upload_rejects_blank_extraction(monkeypatch) -> None:
    async def fake_load_documents_from_upload(state, file):
        return [Document(content="", metadata={"source": file.filename or "sample.pdf", "chunk_index": 0})]

    monkeypatch.setattr(server_module, "_load_documents_from_upload", fake_load_documents_from_upload)

    client = TestClient(create_app())

    with PDF_FIXTURE.open("rb") as pdf_file:
        response = client.post(
            "/documents/upload",
            files={"file": ("sample.pdf", pdf_file, "application/pdf")},
        )

    assert response.status_code == 400
    assert "No extractable text" in response.json()["detail"]


def test_chat_with_file_upload_and_question(monkeypatch) -> None:
    monkeypatch.setenv("RAG_FRAMEWORK_LLM__PROVIDER", "ollama")
    monkeypatch.setattr(
        OllamaLLMProvider,
        "generate",
        lambda self, prompt, *, system_prompt=None: "mocked combined answer",
    )

    async def fake_load_documents_from_upload(state, file):
        return [Document(content="combined request document", metadata={"source": file.filename or "sample.pdf", "chunk_index": 0})]

    monkeypatch.setattr(server_module, "_load_documents_from_upload", fake_load_documents_from_upload)

    client = TestClient(create_app())

    with PDF_FIXTURE.open("rb") as pdf_file:
        response = client.post(
            "/chat-with-file",
            files={"file": ("sample.pdf", pdf_file, "application/pdf")},
            data={"question": "What is the main topic of the uploaded document?"},
        )

    assert response.status_code == 200
    assert response.json()["answer"] == "mocked combined answer"
    assert response.json()["context"] == "combined request document"
    assert response.json()["documents"][0]["content"] == "combined request document"
def test_chat_with_file_rejects_blank_extraction(monkeypatch) -> None:
    async def fake_load_documents_from_upload(state, file):
        return [Document(content="", metadata={"source": file.filename or "sample.pdf", "chunk_index": 0})]

    monkeypatch.setattr(server_module, "_load_documents_from_upload", fake_load_documents_from_upload)

    client = TestClient(create_app())

    with PDF_FIXTURE.open("rb") as pdf_file:
        response = client.post(
            "/chat-with-file",
            files={"file": ("sample.pdf", pdf_file, "application/pdf")},
            data={"question": "What is the main topic of the uploaded document?"},
        )

    assert response.status_code == 400
    assert "No extractable text" in response.json()["detail"]

def test_chat_with_file_falls_back_when_llm_times_out(monkeypatch) -> None:
    monkeypatch.setenv("RAG_FRAMEWORK_LLM__PROVIDER", "ollama")
    monkeypatch.setattr(
        OllamaLLMProvider,
        "generate",
        lambda self, prompt, *, system_prompt=None: (_ for _ in ()).throw(RuntimeError("Ollama timeout")),
    )

    async def fake_load_documents_from_upload(state, file):
        return [Document(content="Dogs need training and daily care.", metadata={"source": file.filename or "dogs.txt"})]

    monkeypatch.setattr(server_module, "_load_documents_from_upload", fake_load_documents_from_upload)

    client = TestClient(create_app())

    with PDF_FIXTURE.open("rb") as pdf_file:
        response = client.post(
            "/chat-with-file",
            files={"file": ("dogs.txt", pdf_file, "text/plain")},
            data={"question": "What is the main topic of the uploaded document?"},
        )

    assert response.status_code == 200
    assert response.json()["answer"] == "Based on the document: Dogs need training and daily care."



# This fast unit test proves the in-memory retriever ranks by cosine similarity
# when an embeddings provider returns useful vectors. It deliberately does not
# prove that a real embedding model understands semantic similarity. The slow
# integration test in tests/integration/test_semantic_retrieval.py covers that.
def test_chat_retrieves_semantically_similar_document_with_embeddings(monkeypatch) -> None:
    from collections.abc import Sequence

    from rag_framework.core.contracts import BaseEmbeddingProvider, BaseLLMProvider
    from rag_framework.core.registry import Registry
    from rag_framework.providers.in_memory_vector_store import InMemoryVectorStore

    class SemanticTestEmbeddingProvider(BaseEmbeddingProvider):
        def embed(self, texts: Sequence[str]) -> list[list[float]]:
            vectors: list[list[float]] = []
            for text in texts:
                lowered = text.lower()
                if any(term in lowered for term in ("dog", "dogs", "canine", "pet", "pets")):
                    vectors.append([1.0, 0.0])
                elif any(term in lowered for term in ("cake", "cakes", "sugar", "bakery")):
                    vectors.append([0.0, 1.0])
                else:
                    vectors.append([0.0, 0.0])
            return vectors

    class TestLLMProvider(BaseLLMProvider):
        def generate(self, prompt: str, *, system_prompt: str | None = None) -> str:
            return "mocked semantic answer"

    def build_registry() -> Registry:
        registry = Registry()
        registry.register("llm", "test", lambda: TestLLMProvider())
        registry.register("embeddings", "semantic-test", lambda: SemanticTestEmbeddingProvider())
        registry.register("vectorstore", "in-memory", lambda: InMemoryVectorStore())
        return registry

    monkeypatch.setattr(server_module, "_build_registry", build_registry)
    monkeypatch.setenv("RAG_FRAMEWORK_LLM__PROVIDER", "test")
    monkeypatch.setenv("RAG_FRAMEWORK_EMBEDDINGS__PROVIDER", "semantic-test")

    client = TestClient(create_app())

    cake_response = client.post(
        "/ingest",
        json={"text": "Cake recipes use sugar and flour.", "source": "cake-note"},
    )
    dog_response = client.post(
        "/ingest",
        json={"text": "Dogs enjoy daily walks and training.", "source": "dog-note"},
    )

    assert cake_response.status_code == 200
    assert dog_response.status_code == 200

    chat_response = client.post("/chat", json={"question": "canine pets", "top_k": 1})

    assert chat_response.status_code == 200
    assert chat_response.json()["documents"][0]["content"] == "Dogs enjoy daily walks and training."
    assert chat_response.json()["context"] == "Dogs enjoy daily walks and training."


def test_chroma_vector_store_persists_documents_across_app_instances(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("RAG_FRAMEWORK_LLM__PROVIDER", "fake")
    monkeypatch.setenv("RAG_FRAMEWORK_EMBEDDINGS__PROVIDER", "fake")
    monkeypatch.setenv("RAG_FRAMEWORK_VECTORSTORE__PROVIDER", "chroma")
    monkeypatch.setenv("RAG_FRAMEWORK_CHROMA__PATH", str(tmp_path / "chroma"))

    first_client = TestClient(create_app())
    ingest_response = first_client.post(
        "/ingest",
        json={"text": "Dogs remain loyal household companions.", "source": "dog-note"},
    )

    assert ingest_response.status_code == 200
    assert ingest_response.json()["total_documents"] == 1

    second_client = TestClient(create_app())
    chat_response = second_client.post("/chat", json={"question": "household companions", "top_k": 1})

    assert chat_response.status_code == 200
    assert chat_response.json()["documents"][0]["content"] == "Dogs remain loyal household companions."
