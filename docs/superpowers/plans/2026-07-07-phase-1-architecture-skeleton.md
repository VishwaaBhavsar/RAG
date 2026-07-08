# Phase 1 Architecture Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the repository skeleton, living architecture documents, and documented placeholder folders for the multi-tenant RAG framework.

**Architecture:** This phase establishes the monorepo shape without runtime behavior. The repository will expose clear boundaries for `apps/`, `packages/`, `tests/`, `docs/`, `scripts/`, and `docker/`, and the docs will capture the multi-tenant single-deployment decision so future phases do not drift.

**Tech Stack:** Markdown documentation, filesystem scaffolding, Python 3.12 pinning placeholder, monorepo layout.

---

### Task 1: Create the top-level repository skeleton

**Files:**
- Create: `README.md`
- Create: `.python-version`
- Create: `apps/README.md`
- Create: `packages/README.md`
- Create: `tests/README.md`
- Create: `docs/README.md`
- Create: `scripts/README.md`
- Create: `docker/README.md`

- [ ] **Step 1: Write the top-level README and folder READMEs**

```markdown
# RAG Framework

This repository is the Phase 1 skeleton for a reusable, multi-tenant AI RAG framework.
```

- [ ] **Step 2: Pin Python 3.12 exactly**

```text
3.12.4
```

- [ ] **Step 3: Verify the folders exist**

Run: `Get-ChildItem -Force`
Expected: `apps`, `packages`, `tests`, `docs`, `scripts`, and `docker` are present.

### Task 2: Document the initial architecture and decisions

**Files:**
- Create: `docs/ARCHITECTURE.md`
- Create: `docs/DECISIONS.md`
- Create: `docs/superpowers/README.md`
- Create: `docs/superpowers/plans/README.md`

- [ ] **Step 1: Write the initial architecture notes**

```markdown
# Architecture

## Current State

This repository is currently at Phase 1: repository skeleton and architecture documentation.
```

- [ ] **Step 2: Record the multi-tenant deployment decision**

```markdown
## 2026-07-07 - Multi-tenant single deployment

Decision:
Build the framework as a single deployment that serves many tenants, with tenant-specific configuration and isolation enforced at runtime.
```

- [ ] **Step 3: Verify the docs are readable**

Run: `Get-Content docs/ARCHITECTURE.md`
Expected: the architecture summary is present and references the planned repository structure.

### Task 3: Add documented package placeholders

**Files:**
- Create: `apps/api/README.md`
- Create: `apps/api/src/README.md`
- Create: `apps/admin/README.md`
- Create: `apps/admin/src/README.md`
- Create: `apps/web/README.md`
- Create: `apps/web/src/README.md`
- Create: `packages/core/README.md`
- Create: `packages/core/src/README.md`
- Create: `packages/core/src/rag_framework/README.md`
- Create: `packages/core/src/rag_framework/core/README.md`
- Create: `packages/core/src/rag_framework/core/__init__.py`
- Create: `packages/providers/README.md`
- Create: `packages/providers/src/README.md`
- Create: `packages/providers/src/rag_framework/README.md`
- Create: `packages/providers/src/rag_framework/providers/README.md`
- Create: `packages/providers/src/rag_framework/providers/__init__.py`
- Create: `packages/plugins/README.md`
- Create: `packages/plugins/src/README.md`
- Create: `packages/plugins/src/rag_framework/README.md`
- Create: `packages/plugins/src/rag_framework/plugins/README.md`
- Create: `packages/plugins/src/rag_framework/plugins/__init__.py`
- Create: `packages/shared/README.md`
- Create: `packages/shared/src/README.md`
- Create: `packages/shared/src/rag_framework/README.md`
- Create: `packages/shared/src/rag_framework/shared/README.md`
- Create: `packages/shared/src/rag_framework/shared/__init__.py`

- [ ] **Step 1: Add a short purpose note to each package folder**

```markdown
# Core Package

This package will host the framework's core engine, registry, DI container, configuration system, event system, logger, and error handling.
```

- [ ] **Step 2: Add namespace package markers for the first importable modules**

```python
"""Core framework module placeholder for future Phase 4 interfaces and Phase 5-7 orchestration."""

__all__: list[str] = []
```

- [ ] **Step 3: Verify the package folders are documented**

Run: `Get-ChildItem packages -Recurse -Filter README.md`
Expected: every planned package folder has a short README.

