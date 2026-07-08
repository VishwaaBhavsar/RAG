# Phase 5 DI Container Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dependency injection container that turns a tenant config into a provider graph by resolving factories from the registry, with no hardcoded provider implementations in the container.

**Architecture:** The container will live in the core package next to the registry and contracts because it is orchestration logic, not integration logic. It will take a typed tenant config, resolve each configured provider through the registry, and return a graph object containing the instantiated providers for the request or tenant.

**Tech Stack:** Python 3.12, dataclasses, typing, pytest, mypy.

---

### Task 1: Define tenant config and provider graph models

**Files:**
- Create: `packages/core/src/rag_framework/core/config.py`
- Create: `packages/core/src/rag_framework/core/container.py`
- Update: `packages/core/src/rag_framework/core/__init__.py`

- [ ] **Step 1: Add typed config models**

```python
@dataclass(frozen=True, slots=True)
class ProviderSelection:
    provider: str
```

- [ ] **Step 2: Add a provider graph dataclass**

```python
@dataclass(frozen=True, slots=True)
class ProviderGraph:
    llm: BaseLLMProvider
    embedding: BaseEmbeddingProvider
```

### Task 2: Implement the container

**Files:**
- Create: `packages/core/src/rag_framework/core/container.py`

- [ ] **Step 1: Resolve each provider from the registry**

```python
llm = cast(BaseLLMProvider, self._registry.create("llm", config.llm.provider))
```

- [ ] **Step 2: Resolve optional providers and tools without hardcoded branching**

```python
tools = tuple(
    cast(BaseTool, self._registry.create("tool", tool.provider))
    for tool in config.tools
)
```

### Task 3: Add tests and update documentation

**Files:**
- Create: `tests/unit/core/test_container.py`
- Update: `docs/ARCHITECTURE.md`
- Update: `docs/DECISIONS.md`

- [ ] **Step 1: Write a test that builds a graph from fake registry factories**

```python
graph = container.build(tenant_config)
assert isinstance(graph.llm, FakeLLMProvider)
```

- [ ] **Step 2: Record the DI container in the architecture doc**

```markdown
The core DI container now builds a provider graph from a tenant config by resolving registry factories for each selected provider.
```

- [ ] **Step 3: Record the container decision in the decision log**

```markdown
## 2026-07-07 - DI container builds provider graphs from tenant config

Decision:
Have the core container resolve provider factories from the registry using tenant config selections.
```

