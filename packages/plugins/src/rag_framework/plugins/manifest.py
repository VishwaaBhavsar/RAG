"""Strict plugin manifest parsing and validation.

Purpose:
    Load plugin manifests from JSON and validate them before any plugin code is imported.

Responsibilities:
    - Enforce the manifest schema required by the framework.
    - Prevent path traversal or unsupported entry points from being loaded.
    - Return a typed manifest object for downstream loading code.

Usage example:
    manifest = load_manifest(Path("plugins/example/manifest.json"))
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Any

from .errors import PluginManifestError

_ENTRY_POINT_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+\.py(?::[A-Za-z_][A-Za-z0-9_]*)?$")


@dataclass(frozen=True, slots=True)
class PluginManifest:
    """Validated plugin metadata."""

    name: str
    version: str
    type: str
    entry_point: str
    required_config_keys: tuple[str, ...]
    path: Path


def load_manifest(manifest_path: Path) -> PluginManifest:
    """Load and validate a plugin manifest from JSON."""

    try:
        raw_text = manifest_path.read_text(encoding="utf-8")
        data = json.loads(raw_text)
    except FileNotFoundError as exc:
        raise PluginManifestError(f"Missing manifest file: {manifest_path}") from exc
    except json.JSONDecodeError as exc:
        raise PluginManifestError(f"Invalid JSON in manifest file: {manifest_path}") from exc

    if not isinstance(data, dict):
        raise PluginManifestError(f"Manifest must be a JSON object: {manifest_path}")

    allowed_keys = {"name", "version", "type", "entry_point", "required_config_keys"}
    data_keys = set(data)
    missing_keys = allowed_keys - data_keys
    unexpected_keys = data_keys - allowed_keys

    if missing_keys:
        raise PluginManifestError(
            f"Manifest is missing required keys {sorted(missing_keys)}: {manifest_path}"
        )
    if unexpected_keys:
        raise PluginManifestError(
            f"Manifest contains unexpected keys {sorted(unexpected_keys)}: {manifest_path}"
        )

    name = _require_non_empty_str(data["name"], "name", manifest_path)
    version = _require_non_empty_str(data["version"], "version", manifest_path)
    plugin_type = _require_non_empty_str(data["type"], "type", manifest_path)
    entry_point = _require_non_empty_str(data["entry_point"], "entry_point", manifest_path)
    if not _ENTRY_POINT_PATTERN.match(entry_point):
        raise PluginManifestError(
            f"entry_point must be a relative Python file optionally followed by a callable name: {manifest_path}"
        )

    required_config_keys = _require_string_sequence(
        data["required_config_keys"], "required_config_keys", manifest_path
    )

    return PluginManifest(
        name=name,
        version=version,
        type=plugin_type,
        entry_point=entry_point,
        required_config_keys=required_config_keys,
        path=manifest_path,
    )


def _require_non_empty_str(value: Any, field_name: str, manifest_path: Path) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PluginManifestError(f"{field_name} must be a non-empty string: {manifest_path}")
    return value


def _require_string_sequence(value: Any, field_name: str, manifest_path: Path) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise PluginManifestError(f"{field_name} must be a list of strings: {manifest_path}")

    validated: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise PluginManifestError(
                f"{field_name} must contain only non-empty strings: {manifest_path}"
            )
        validated.append(item)
    return tuple(validated)

