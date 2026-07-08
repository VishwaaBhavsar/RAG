# Phase 6 Configuration Loading Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Load base application config from YAML plus environment variables using `pydantic-settings`, then merge tenant overrides from PostgreSQL-style records into a validated tenant config.

**Architecture:** The config layer will live in the core package because it is part of the framework runtime contract. Base settings will be parsed through `pydantic-settings`, then tenant override records will be merged over that base model and validated again before the DI container sees them.

**Tech Stack:** Python 3.12, pydantic v2, pydantic-settings, YAML, pytest.

---

### Task 1: Add the typed settings models

**Files:**
- Create: `packages/core/src/rag_framework/core/settings.py`

- [ ] **Step 1: Define the base provider selection and app config models**

```python
class ProviderSelection(BaseModel):
    provider: str
```

- [ ] **Step 2: Define the patch model used for tenant overrides**

```python
class TenantConfigPatch(BaseModel):
    llm: ProviderSelection | None = None
```

### Task 2: Add YAML and env loading

**Files:**
- Create: `packages/core/src/rag_framework/core/settings.py`

- [ ] **Step 1: Load YAML defaults and env overrides through pydantic-settings**

```python
config = AppConfig.load(Path("config/base.yaml"))
```

- [ ] **Step 2: Ensure env vars override YAML values**

```python
os.environ["RAG_FRAMEWORK_LLM__PROVIDER"] = "ollama"
```

### Task 3: Add tenant override merging

**Files:**
- Create: `packages/core/src/rag_framework/core/settings.py`
- Update: `packages/core/src/rag_framework/core/container_runtime.py`

- [ ] **Step 1: Merge tenant overrides over base config**

```python
tenant_config = merge_tenant_config(base_config, {"llm": {"provider": "ollama"}})
```

- [ ] **Step 2: Keep the container unchanged except for reading the merged tenant config**

```python
graph = Container(registry).build(tenant_config)
```

### Task 4: Add tests and documentation updates

**Files:**
- Create: `tests/unit/core/test_settings.py`
- Update: `docs/ARCHITECTURE.md`
- Update: `docs/DECISIONS.md`

- [ ] **Step 1: Write a test proving env overrides YAML**

```python
assert config.llm.provider == "ollama"
```

- [ ] **Step 2: Write a test proving tenant overrides change the container output**

```python
assert graph.llm is ollama_llm
```

- [ ] **Step 3: Record the config-loading decision in the living docs**

```markdown
## 2026-07-07 - YAML and env config loading with tenant merge

Decision:
Load base config with pydantic-settings, then merge tenant overrides into a validated tenant config.
```

