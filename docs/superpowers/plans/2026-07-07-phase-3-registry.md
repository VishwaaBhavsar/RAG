# Phase 3 Registry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a typed registry that stores provider factories by provider type and provider name, so the framework can look up different implementations without hardcoded branching.

**Architecture:** The registry will live in `packages/core` because it is part of the framework's core engine, not a plugin or provider implementation. It will expose registration and lookup APIs keyed by a provider category plus a human-readable provider name, and it will reject duplicate registrations deterministically.

**Tech Stack:** Python 3.12, dataclasses, typing, pytest.

---

### Task 1: Define registry boundaries

**Files:**
- Create: `packages/core/src/rag_framework/core/registry.py`
- Update: `packages/core/src/rag_framework/core/__init__.py`

- [ ] **Step 1: Add typed registry models**

```python
@dataclass(frozen=True, slots=True)
class RegisteredFactory:
    provider_type: str
    provider_name: str
    factory: Factory
```

- [ ] **Step 2: Export the registry API from the core package**

```python
from .registry import Registry
```

### Task 2: Add registry tests

**Files:**
- Create: `tests/unit/core/test_registry.py`

- [ ] **Step 1: Write a test that registers two providers with the same provider type**

```python
registry.register("llm", "openai", lambda: "openai")
registry.register("llm", "ollama", lambda: "ollama")
```

- [ ] **Step 2: Verify lookup returns the correct factory for each provider name**

```python
assert registry.get("llm", "openai")() == "openai"
assert registry.get("llm", "ollama")() == "ollama"
```

- [ ] **Step 3: Verify duplicate registration raises a clear error**

```python
with pytest.raises(RegistryError):
    registry.register("llm", "openai", lambda: "duplicate")
```

### Task 3: Update docs for Phase 3

**Files:**
- Update: `docs/ARCHITECTURE.md`
- Update: `docs/DECISIONS.md`

- [ ] **Step 1: Record the registry role in the architecture doc**

```markdown
The core registry stores provider factories by provider type and provider name so configuration can map directly to runtime behavior.
```

- [ ] **Step 2: Record the duplicate-registration decision in the decision log**

```markdown
## 2026-07-07 - Registry keyed by provider type and provider name

Decision:
Use a typed registry that maps provider type plus provider name to a single factory and rejects duplicates.
```

