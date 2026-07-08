"""Plugin management package.

Purpose:
    Expose the plugin manager and manifest types behind a small, stable surface.

Responsibilities:
    - Keep the public API for plugin discovery easy to import.
    - Hide the internal module split behind package-level exports.

Usage example:
    from rag_framework.plugins import PluginManager
"""

from .errors import PluginError, PluginLoadError, PluginManifestError
from .manifest import PluginManifest, load_manifest
from .manager import LoadedPlugin, PluginLoadResult, PluginManager, RejectedPlugin

__all__ = [
    "LoadedPlugin",
    "PluginError",
    "PluginLoadError",
    "PluginLoadResult",
    "PluginManager",
    "PluginManifest",
    "PluginManifestError",
    "RejectedPlugin",
    "load_manifest",
]
