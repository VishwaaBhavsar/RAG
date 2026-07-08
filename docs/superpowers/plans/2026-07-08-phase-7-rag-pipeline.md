# Phase 7 RAG Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire a core chat engine and RAG pipeline through the DI container and registry only, then prove an end-to-end query flows through retrieval, context assembly, and generation using fake providers.

**Architecture:** The RAG pipeline will stay in the core package because it is orchestration logic, not provider logic. It will consume the provider graph built by the DI container, call the embedding provider, vector store, optional reranker, and LLM in sequence, and never import concrete implementations directly. The chat engine will wrap the pipeline so future app entry points have a single interface for chat requests.

**Tech Stack:** Python 3.12, dataclasses, typing, pytest, existing core contracts and fake providers.

---

### Task 1: Define the orchestration models

**Files:**
- Create: `packages/core/src/rag_framework/core/pipeline.py`
- Create: `packages/core/src/rag_framework/core/chat.py`
- Update: `packages/core/src/rag_framework/core/__init__.py`

- [ ] **Step 1: Add a pipeline result model that exposes the retrieved documents and generated answer**

```python
@dataclass(frozen=True, slots=True)
class RAGResponse:
    answer: str
    documents: tuple[Document, ...]
    context: str
```

- [ ] **Step 2: Add a small chat engine wrapper**

```python
class ChatEngine:
    def answer(self, session_id: str, prompt: str) -> RAGResponse:
        return self._pipeline.run(prompt)
```

### Task 2: Implement the RAG pipeline

**Files:**
- Create: `packages/core/src/rag_framework/core/pipeline.py`

- [ ] **Step 1: Embed the query and retrieve matching records**

```python
query_embedding = self._embedding.embed([prompt])[0]
results = self._vector_store.query(query_embedding, top_k=self._top_k)
```

- [ ] **Step 2: Assemble a deterministic context string from the retrieved documents**

```python
context = "\n\n".join(document.content for document in documents)
```

- [ ] **Step 3: Generate the final answer through the LLM provider**

```python
answer = self._llm.generate(prompt, system_prompt=context)
```

### Task 3: Add an end-to-end test

**Files:**
- Create: `tests/unit/core/test_rag_pipeline.py`
- Update: `docs/ARCHITECTURE.md`
- Update: `docs/DECISIONS.md`

- [ ] **Step 1: Write a test that seeds a fake vector store with a document and runs the chat engine**

```python
response = engine.answer("session-1", "What is in the document?")
assert "relevant document" in response.context
```

- [ ] **Step 2: Verify the answer came from the fake LLM and that the flow used the retrieved context**

```python
assert response.answer.startswith("answer:")
assert "relevant document" in response.answer
```

- [ ] **Step 3: Record the RAG pipeline in the living docs**

```markdown
## 2026-07-08 - Core RAG pipeline and chat engine

Decision:
Use the provider graph to drive retrieval, context assembly, and generation inside the core package.
```

