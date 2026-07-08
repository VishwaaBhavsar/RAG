# Phase 8 PDF Loader Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the first real plugin, a PDF loader, in its own plugin directory so it can be discovered by the plugin manager, registered through the registry, and configured through the existing config system without touching the core engine.

**Architecture:** The PDF loader will live entirely inside its plugin directory and expose a registration callable through `plugin.py`. The loader will implement `BaseLoader`, parse a small PDF fixture file with a self-contained text extractor, and register itself under `loader:pdf` so the container can resolve it by config just like any other provider.

**Tech Stack:** Python 3.12, existing core contracts and registry, pytest, a self-contained PDF text extractor.

---

### Task 1: Create the plugin directory and loader implementation

**Files:**
- Create: `packages/plugins/plugins/README.md`
- Create: `packages/plugins/plugins/pdf_loader/README.md`
- Create: `packages/plugins/plugins/pdf_loader/manifest.json`
- Create: `packages/plugins/plugins/pdf_loader/plugin.py`
- Create: `packages/plugins/plugins/pdf_loader/config.py`

- [ ] **Step 1: Add a plugin manifest that passes strict validation**

```json
{
  "name": "pdf-loader",
  "version": "1.0.0",
  "type": "loader",
  "entry_point": "plugin.py:load",
  "required_config_keys": ["pdf_chunk_size"]
}
```

- [ ] **Step 2: Implement a loader that extracts text from a simple PDF content stream**

```python
class PdfLoader(BaseLoader):
    def load(self, source: str | Path) -> list[Document]:
        ...
```

- [ ] **Step 3: Return a registration callable from the plugin entry point**

```python
def load() -> Callable[[Registry], None]:
    def register(registry: Registry) -> None:
        registry.register("loader", "pdf", lambda: PdfLoader())
    return register
```

### Task 2: Add a real PDF fixture

**Files:**
- Create: `tests/fixtures/documents/sample.pdf`

- [ ] **Step 1: Add a tiny PDF fixture with extractable text**

```text
(relevant document about retrieval) Tj
```

### Task 3: Add discovery and registration tests

**Files:**
- Create: `tests/unit/plugins/test_pdf_loader_plugin.py`
- Update: `docs/ARCHITECTURE.md`
- Update: `docs/DECISIONS.md`

- [ ] **Step 1: Verify the plugin manager discovers and loads the plugin**

```python
loaded = PluginManager(plugins_root).load_plugins()
assert loaded.loaded_plugins[0].manifest.name == "pdf-loader"
```

- [ ] **Step 2: Verify the plugin registers a PDF loader into the registry**

```python
register = loaded.loaded_plugins[0].entry_point_result
register(registry)
assert isinstance(registry.create("loader", "pdf"), PdfLoader)
```

- [ ] **Step 3: Verify the loader reads the PDF fixture and returns document chunks**

```python
documents = registry.create("loader", "pdf").load(fixture_path)
assert documents[0].content == "relevant document about retrieval"
```

- [ ] **Step 4: Record the plugin in the living docs**

```markdown
## 2026-07-08 - First real plugin: PDF loader

Decision:
Keep the PDF loader in its own plugin directory and have it register a loader factory through the registry.
```

