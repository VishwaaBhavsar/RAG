"""Tests for the plugin manager."""

from __future__ import annotations

from pathlib import Path
from shutil import copytree

from rag_framework.plugins import PluginManager


FIXTURES_ROOT = Path(__file__).resolve().parents[2] / "fixtures" / "plugins"


def _copy_fixture_plugins(destination: Path, names: list[str]) -> Path:
    plugins_root = destination / "plugins"
    plugins_root.mkdir(parents=True, exist_ok=True)
    for name in names:
        copytree(FIXTURES_ROOT / name, plugins_root / name)
    return plugins_root


def test_loads_valid_plugin_fixture(tmp_path: Path) -> None:
    plugins_root = _copy_fixture_plugins(tmp_path, ["valid_echo_plugin"])

    result = PluginManager(plugins_root).load_plugins()

    assert [plugin.manifest.name for plugin in result.loaded_plugins] == ["valid-echo"]
    assert result.loaded_plugins[0].entry_point_result == {
        "plugin": "valid-echo",
        "loaded": True,
    }
    assert result.rejected_plugins == ()


def test_rejects_invalid_manifest_without_stopping_valid_plugins(tmp_path: Path) -> None:
    plugins_root = _copy_fixture_plugins(
        tmp_path,
        ["valid_echo_plugin", "invalid_manifest_plugin"],
    )

    result = PluginManager(plugins_root).load_plugins()

    assert [plugin.manifest.name for plugin in result.loaded_plugins] == ["valid-echo"]
    assert len(result.rejected_plugins) == 1
    assert result.rejected_plugins[0].error_type == "PluginManifestError"

