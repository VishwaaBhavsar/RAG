"""Plugin discovery and loading.

Purpose:
    Discover plugins from a designated root directory, validate each manifest, and load valid plugins.

Responsibilities:
    - Scan only the configured plugin root.
    - Validate manifests before importing any code.
    - Isolate failures so one broken plugin does not stop the others.

Usage example:
    manager = PluginManager(Path("tests/fixtures/plugins"))
    result = manager.load_plugins()
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import util as importlib_util
from pathlib import Path
from types import ModuleType
from typing import Any

from .errors import PluginLoadError, PluginManifestError
from .manifest import PluginManifest, load_manifest


@dataclass(frozen=True, slots=True)
class LoadedPlugin:
    """A successfully loaded plugin."""

    directory: Path
    manifest: PluginManifest
    module: ModuleType
    entry_point_result: Any


@dataclass(frozen=True, slots=True)
class RejectedPlugin:
    """A plugin that failed discovery or loading."""

    directory: Path
    reason: str
    error_type: str


@dataclass(frozen=True, slots=True)
class PluginLoadResult:
    """Aggregate plugin loading outcome."""

    loaded_plugins: tuple[LoadedPlugin, ...]
    rejected_plugins: tuple[RejectedPlugin, ...]


class PluginManager:
    """Load plugins from a single configured directory."""

    def __init__(self, plugins_root: Path) -> None:
        self._plugins_root = plugins_root.resolve()

    def load_plugins(self) -> PluginLoadResult:
        """Load every valid plugin found under the configured root."""

        loaded_plugins: list[LoadedPlugin] = []
        rejected_plugins: list[RejectedPlugin] = []

        if not self._plugins_root.exists():
            return PluginLoadResult(loaded_plugins=tuple(), rejected_plugins=tuple())

        for plugin_dir in sorted(path for path in self._plugins_root.iterdir() if path.is_dir()):
            try:
                manifest = load_manifest(plugin_dir / "manifest.json")
                module = self._import_plugin_module(plugin_dir, manifest.entry_point)
                entry_point_result = self._invoke_entry_point(module, manifest.entry_point)
                loaded_plugins.append(
                    LoadedPlugin(
                        directory=plugin_dir,
                        manifest=manifest,
                        module=module,
                        entry_point_result=entry_point_result,
                    )
                )
            except (PluginManifestError, PluginLoadError) as exc:
                rejected_plugins.append(
                    RejectedPlugin(
                        directory=plugin_dir,
                        reason=str(exc),
                        error_type=type(exc).__name__,
                    )
                )
            except Exception as exc:  # pragma: no cover - defensive isolation boundary
                rejected_plugins.append(
                    RejectedPlugin(
                        directory=plugin_dir,
                        reason=f"Unexpected plugin failure: {exc}",
                        error_type=type(exc).__name__,
                    )
                )

        return PluginLoadResult(
            loaded_plugins=tuple(loaded_plugins),
            rejected_plugins=tuple(rejected_plugins),
        )

    def _import_plugin_module(self, plugin_dir: Path, entry_point: str) -> ModuleType:
        module_relative_path, _ = _split_entry_point(entry_point)
        module_path = (plugin_dir / module_relative_path).resolve()
        if plugin_dir not in module_path.parents and module_path != plugin_dir / module_relative_path:
            raise PluginLoadError(f"Entry point escapes the plugin directory: {entry_point}")
        if not module_path.is_file():
            raise PluginLoadError(f"Plugin entry point does not exist: {module_path}")

        module_name = f"rag_framework.plugin.{plugin_dir.name}"
        spec = importlib_util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise PluginLoadError(f"Unable to create an import spec for {module_path}")

        module = importlib_util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _invoke_entry_point(self, module: ModuleType, entry_point: str) -> Any:
        _, callable_name = _split_entry_point(entry_point)
        if callable_name is None:
            return module

        attribute = getattr(module, callable_name, None)
        if attribute is None or not callable(attribute):
            raise PluginLoadError(
                f"Entry point callable '{callable_name}' was not found in plugin module '{module.__name__}'"
            )
        return attribute()


def _split_entry_point(entry_point: str) -> tuple[str, str | None]:
    module_path, _, callable_name = entry_point.partition(":")
    return module_path, callable_name or None

