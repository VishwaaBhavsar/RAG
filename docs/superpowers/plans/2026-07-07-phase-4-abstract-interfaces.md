# Phase 4 Abstract Interfaces Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Define the framework's abstract provider interfaces and ship in-memory fake implementations used only by tests, so later provider packages can plug into the core engine without changing it.

**Architecture:** The core package will own the abstract contracts because every later phase depends on them. Each interface will describe behavior, not vendor details, and the fake implementations will live beside the contracts so tests can exercise the abstractions without importing real providers.

**Tech Stack:** Python 3.12, `abc.ABC`, dataclasses, typing, pytest, mypy.

---

### Task 1: Define the shared contract models

**Files:**
- Create: `packages/core/src/rag_framework/core/contracts.py`
- Update: `packages/core/src/rag_framework/core/__init__.py`

- [ ] **Step 1: Add data models for documents, messages, and vector records**

```python
@dataclass(frozen=True, slots=True)
class Document:
    content: str
    metadata: Mapping[str, Any]
```

- [ ] **Step 2: Export the contract types from the core package**

```python
from .contracts import BaseLLMProvider, Document
```

### Task 2: Define the abstract provider interfaces

**Files:**
- Create: `packages/core/src/rag_framework/core/contracts.py`

- [ ] **Step 1: Define the ABCs for every provider category**

```python
class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, *, system_prompt: str | None = None) -> str:
        raise NotImplementedError
```

- [ ] **Step 2: Keep signatures concrete enough for later provider packages**

```python
class BaseVectorStore(ABC):
    @abstractmethod
    def query(self, embedding: Sequence[float], *, top_k: int = 5) -> list[VectorSearchResult]:
        raise NotImplementedError
```

### Task 3: Add in-memory fake implementations

**Files:**
- Create: `packages/core/src/rag_framework/core/fakes.py`

- [ ] **Step 1: Implement fake providers for all interfaces**

```python
class FakeLLMProvider(BaseLLMProvider):
    def generate(self, prompt: str, *, system_prompt: str | None = None) -> str:
        return f"fake-response:{prompt}"
```

- [ ] **Step 2: Keep the fake providers deterministic for tests**

```python
class FakeVectorStore(BaseVectorStore):
    def query(self, embedding: Sequence[float], *, top_k: int = 5) -> list[VectorSearchResult]:
        return self._documents[:top_k]
```

### Task 4: Add tests and documentation updates

**Files:**
- Create: `tests/unit/core/test_contracts.py`
- Update: `docs/ARCHITECTURE.md`
- Update: `docs/DECISIONS.md`

- [ ] **Step 1: Add tests that prove each fake implementation works**

```python
assert FakeLLMProvider().generate("hello") == "fake-response:hello"
```

- [ ] **Step 2: Record the contract layer in the architecture doc**

```markdown
The core package now defines the abstract provider interfaces and test-only fake implementations that later packages will implement for real providers.
```

- [ ] **Step 3: Record the interface-first decision in the decision log**

```markdown
## 2026-07-07 - Abstract provider interfaces in core

Decision:
Define the provider ABCs in the core package and keep fake implementations there for tests.
```

