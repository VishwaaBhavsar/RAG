"""FastAPI backend for document ingest and question answering.

Endpoints:
    GET /health
    POST /documents/upload
    POST /ingest
    POST /chat
    POST /ask
    POST /chat-with-file

Run:
    python apps/api/src/server.py
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from rag_framework.core import (
    Document,
    Registry,
    VectorRecord,
    register_default_embedding_providers,
    register_default_llm_providers,
    register_default_vector_store_providers,
)
from rag_framework.core.contracts import BaseEmbeddingProvider, BaseLLMProvider, BaseLoader, BaseVectorStore
from rag_framework.plugins import PluginManager


@dataclass(slots=True)
class InMemoryKnowledgeBase:
    embedding_provider: BaseEmbeddingProvider
    vector_store: BaseVectorStore

    @property
    def documents(self) -> list[Document]:
        vector_store_documents = getattr(self.vector_store, "documents", None)
        if callable(vector_store_documents):
            return list(vector_store_documents())
        if vector_store_documents is not None:
            return list(vector_store_documents)
        return []

    def count(self) -> int:
        vector_store_count = getattr(self.vector_store, "count", None)
        if callable(vector_store_count):
            return int(vector_store_count())
        return len(self.documents)

    def add_documents(self, documents: list[Document]) -> None:
        if not documents:
            return

        embeddings = self.embedding_provider.embed([document.content for document in documents])
        if len(embeddings) != len(documents):
            raise ValueError("embedding provider returned a different number of vectors than documents")

        records = [
            VectorRecord(
                id=_document_id(document),
                embedding=tuple(float(value) for value in embedding),
                document=document,
            )
            for document, embedding in zip(documents, embeddings)
        ]
        self.vector_store.upsert(records)

    def search(self, question: str, *, top_k: int = 3) -> list[Document]:
        query_embeddings = self.embedding_provider.embed([question])
        if len(query_embeddings) != 1:
            raise ValueError("embedding provider must return exactly one query vector")

        query_embedding = tuple(float(value) for value in query_embeddings[0])
        return [result.record.document for result in self.vector_store.query(query_embedding, top_k=top_k)]


@dataclass(slots=True)
class BackendState:
    registry: Registry
    knowledge_base: InMemoryKnowledgeBase
    llm_provider_name: str
    embeddings_provider_name: str
    vector_store_provider_name: str
    pdf_loader_name: str = "pdf"


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=20)
    provider: str | None = None


class TextIngestRequest(BaseModel):
    text: str = Field(min_length=1)
    source: str | None = None


class PathIngestRequest(BaseModel):
    path: str = Field(min_length=1)


class BackendResponse(BaseModel):
    answer: str
    context: str
    documents: list[dict[str, Any]]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _document_id(document: Document) -> str:
    payload = json.dumps(
        {"content": document.content, "metadata": dict(document.metadata)},
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _build_registry() -> Registry:
    registry = Registry()
    register_default_llm_providers(registry)
    register_default_embedding_providers(registry)
    register_default_vector_store_providers(registry)

    plugin_root = _repo_root() / "packages" / "plugins" / "plugins"
    result = PluginManager(plugin_root).load_plugins()
    for loaded_plugin in result.loaded_plugins:
        register = loaded_plugin.entry_point_result
        if callable(register):
            register(registry)

    if result.rejected_plugins:
        rejected = "; ".join(f"{item.directory.name}: {item.reason}" for item in result.rejected_plugins)
        print(f"[backend] rejected plugins: {rejected}")

    return registry


def _load_documents_from_text(text: str, source: str | None = None) -> list[Document]:
    return [Document(content=text, metadata={"source": source or "text"})]


def _load_documents_from_path(state: BackendState, path: str) -> list[Document]:
    loader = cast(BaseLoader, state.registry.create("loader", state.pdf_loader_name))
    return loader.load(Path(path))


async def _load_documents_from_upload(state: BackendState, file: UploadFile) -> list[Document]:
    filename = file.filename or "upload"
    suffix = Path(filename).suffix.lower()
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="uploaded file is empty")

    if suffix == ".pdf" or file.content_type == "application/pdf":
        temp_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix or ".pdf") as temp_file:
                temp_file.write(contents)
                temp_path = Path(temp_file.name)
            return _load_documents_from_path(state, str(temp_path))
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

    text = contents.decode("utf-8", errors="replace")
    return _load_documents_from_text(text, source=filename)


def _looks_uncertain(answer: str) -> bool:
    lowered = answer.lower()
    return any(
        phrase in lowered
        for phrase in (
            "i don't know",
            "do not know",
            "don't have enough information",
            "not enough information",
            "insufficient",
            "difficult to provide",
            "without more context",
        )
    )


def _extractive_answer(context: str) -> str:
    first_line = context.splitlines()[0].strip() if context.splitlines() else context.strip()
    return f"Based on the document: {first_line}"


def _answer_question(state: BackendState, question: str, *, top_k: int = 3, provider_name: str | None = None) -> dict[str, Any]:
    provider = cast(BaseLLMProvider, state.registry.create("llm", provider_name or state.llm_provider_name))
    relevant_documents = state.knowledge_base.search(question, top_k=top_k)
    context = "\n\n".join(document.content for document in relevant_documents)
    prompt = f"Question: {question}\n\nContext: {context}"
    try:
        answer = provider.generate(
            prompt,
            system_prompt="Answer using only the provided context. If the context is insufficient, say you do not know.",
        )
    except RuntimeError as exc:
        if context.strip():
            answer = _extractive_answer(context)
        else:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

    if _looks_uncertain(answer) and context.strip():
        answer = _extractive_answer(context)

    return {
        "answer": answer,
        "context": context,
        "documents": [
            {
                "content": document.content,
                "metadata": dict(document.metadata),
            }
            for document in relevant_documents
        ],
    }


def _filter_meaningful_documents(documents: list[Document], *, source: str) -> list[Document]:
    meaningful_documents = [document for document in documents if document.content.strip()]
    if meaningful_documents:
        return meaningful_documents

    raise HTTPException(
        status_code=400,
        detail=(
            f"No extractable text could be read from {source}. "
            "Try a text-based PDF, or install Poppler and Tesseract for scanned PDFs."
        ),
    )


def create_app() -> FastAPI:
    registry = _build_registry()
    llm_provider_name = os.getenv("RAG_FRAMEWORK_LLM__PROVIDER", "ollama").strip().lower() or "ollama"
    embeddings_provider_name = (
        os.getenv("RAG_FRAMEWORK_EMBEDDINGS__PROVIDER", "sentence-transformers").strip().lower()
        or "sentence-transformers"
    )
    embedding_provider = cast(BaseEmbeddingProvider, registry.create("embeddings", embeddings_provider_name))
    vector_store_provider_name = os.getenv("RAG_FRAMEWORK_VECTORSTORE__PROVIDER", "chroma").strip().lower() or "chroma"
    vector_store = cast(BaseVectorStore, registry.create("vectorstore", vector_store_provider_name))
    state = BackendState(
        registry=registry,
        knowledge_base=InMemoryKnowledgeBase(embedding_provider=embedding_provider, vector_store=vector_store),
        llm_provider_name=llm_provider_name,
        embeddings_provider_name=embeddings_provider_name,
        vector_store_provider_name=vector_store_provider_name,
    )

    app = FastAPI(title="RAG Framework API", version="0.1.0")
    app.state.backend = state

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "llm_provider": state.llm_provider_name,
            "embeddings_provider": state.embeddings_provider_name,
            "vector_store_provider": state.vector_store_provider_name,
            "documents": state.knowledge_base.count(),
        }

    @app.post("/documents/upload")
    async def upload_document(file: UploadFile = File(...)) -> dict[str, Any]:
        try:
            documents = await _load_documents_from_upload(state, file)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        documents = _filter_meaningful_documents(documents, source=file.filename or "uploaded file")
        state.knowledge_base.add_documents(documents)
        return {
            "ingested": len(documents),
            "total_documents": state.knowledge_base.count(),
            "filename": file.filename,
        }

    @app.post("/ingest")
    async def ingest_document(payload: TextIngestRequest | PathIngestRequest) -> dict[str, Any]:
        try:
            if isinstance(payload, TextIngestRequest):
                documents = _load_documents_from_text(payload.text, payload.source)
                source_label = payload.source or "text payload"
            else:
                documents = _load_documents_from_path(state, payload.path)
                source_label = payload.path
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        documents = _filter_meaningful_documents(documents, source=source_label)
        state.knowledge_base.add_documents(documents)
        return {
            "ingested": len(documents),
            "total_documents": state.knowledge_base.count(),
        }

    @app.post("/chat", response_model=BackendResponse)
    def chat(request: ChatRequest) -> dict[str, Any]:
        return _answer_question(state, request.question, top_k=request.top_k, provider_name=request.provider)

    @app.post("/ask", response_model=BackendResponse)
    def ask(request: ChatRequest) -> dict[str, Any]:
        return _answer_question(state, request.question, top_k=request.top_k, provider_name=request.provider)

    @app.post("/chat-with-file", response_model=BackendResponse)
    async def chat_with_file(
        file: UploadFile = File(...),
        question: str = Form(..., min_length=1),
        top_k: int = Form(default=3, ge=1, le=20),
        provider: str | None = Form(default=None),
    ) -> dict[str, Any]:
        try:
            documents = await _load_documents_from_upload(state, file)
            documents = _filter_meaningful_documents(documents, source=file.filename or "uploaded file")
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        state.knowledge_base.add_documents(documents)
        return _answer_question(state, question, top_k=top_k, provider_name=provider)

    return app


app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()





