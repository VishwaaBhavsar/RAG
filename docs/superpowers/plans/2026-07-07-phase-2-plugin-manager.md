# Phase 2 Plugin Manager Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a secure plugin manager that discovers plugins from the designated plugins directory, validates strict manifests, loads valid plugins, and isolates failures so one broken plugin never stops the rest.

**Architecture:** The plugin manager will scan only the configured plugin root, treat each plugin as an isolated directory, validate `manifest.json` before any code import, and import plugin entry points only from paths inside that directory. The manager will report loaded plugins and rejected plugins separately so startup can continue even when one plugin is malformed.

**Tech Stack:** Python 3.12, standard library JSON/importlib/pathlib, pytest, filesystem fixtures.

---

### Task 1: Define manifest and load result models

**Files:**
- Create: `packages/plugins/src/rag_framework/plugins/errors.py`
- Create: `packages/plugins/src/rag_framework/plugins/manifest.py`
- Create: `packages/plugins/src/rag_framework/plugins/manager.py`
- Modify: `packages/plugins/src/rag_framework/plugins/__init__.py`

- [ ] **Step 1: Write the manifest parser and result dataclasses**

```python
@dataclass(frozen=True)
class PluginManifest:
    name: str
    version: str
    type: str
    entry_point: str
    required_config_keys: tuple[str, ...]
    path: Path
```

- [ ] **Step 2: Add strict schema validation**

```python
allowed_keys = {"name", "version", "type", "entry_point", "required_config_keys"}
missing = allowed_keys - data.keys()
unexpected = data.keys() - allowed_keys
```

- [ ] **Step 3: Add a manager that loads each plugin directory independently**

```python
for plugin_dir in sorted(candidate for candidate in root.iterdir() if candidate.is_dir()):
    try:
        manifest = load_manifest(plugin_dir / "manifest.json")
        loaded = load_plugin(plugin_dir, manifest)
    except Exception as exc:
        rejected.append(...)
```

### Task 2: Add fixture plugins and tests

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/fixtures/plugins/valid_echo_plugin/manifest.json`
- Create: `tests/fixtures/plugins/valid_echo_plugin/plugin.py`
- Create: `tests/fixtures/plugins/valid_echo_plugin/README.md`
- Create: `tests/fixtures/plugins/valid_echo_plugin/config.py`
- Create: `tests/fixtures/plugins/invalid_manifest_plugin/manifest.json`
- Create: `tests/fixtures/plugins/invalid_manifest_plugin/plugin.py`
- Create: `tests/fixtures/plugins/invalid_manifest_plugin/README.md`
- Create: `tests/fixtures/plugins/invalid_manifest_plugin/config.py`
- Create: `tests/unit/plugins/test_plugin_manager.py`

- [ ] **Step 1: Add a fixture-based test for a valid plugin**

```python
result = PluginManager(tmp_path / "plugins").load_plugins()
assert [plugin.manifest.name for plugin in result.loaded_plugins] == ["valid-echo"]
```

- [ ] **Step 2: Add a fixture-based test that invalid manifests are rejected without stopping other plugins**

```python
assert [plugin.manifest.name for plugin in result.loaded_plugins] == ["valid-echo"]
assert len(result.rejected_plugins) == 1
```

- [ ] **Step 3: Run the targeted tests**

Run: `pytest tests/unit/plugins/test_plugin_manager.py -v`
Expected: both tests pass.

### Task 3: Document Phase 2 decisions

**Files:**
- Update: `docs/ARCHITECTURE.md`
- Update: `docs/DECISIONS.md`

- [ ] **Step 1: Record the plugin manager's current behavior in the architecture doc**

```markdown
The plugin manager scans each plugin directory independently, validates `manifest.json` before import, and keeps broken plugins isolated from healthy ones.
```

- [ ] **Step 2: Record the manifest and isolation decision in the decision log**

```markdown
## 2026-07-07 - Strict plugin manifests and isolated failures

Decision:
Validate each plugin manifest against a strict schema before import, and continue loading other plugins if one fails.
```

