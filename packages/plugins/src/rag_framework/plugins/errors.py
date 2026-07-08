"""Plugin manager exceptions.

Purpose:
    Provide explicit error types for plugin manifest validation and plugin loading failures.

Responsibilities:
    - Make failure modes easy to distinguish in tests and logs.
    - Keep manifest parsing errors separate from import or entry-point errors.

Usage example:
    raise PluginManifestError("manifest.json is missing required keys")
"""

from __future__ import annotations


class PluginError(Exception):
    """Base class for plugin manager errors."""


class PluginManifestError(PluginError):
    """Raised when a plugin manifest fails strict validation."""


class PluginLoadError(PluginError):
    """Raised when a plugin cannot be imported or initialized."""

