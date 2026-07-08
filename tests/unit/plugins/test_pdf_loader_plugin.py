"""Tests for the PDF loader plugin."""

from __future__ import annotations

from pathlib import Path

from rag_framework.core import Document, Registry
from rag_framework.plugins import PluginManager


PLUGIN_ROOT = Path(__file__).resolve().parents[3] / "packages" / "plugins" / "plugins"
PDF_FIXTURE = Path(__file__).resolve().parents[2] / "fixtures" / "documents" / "sample.pdf"


def test_pdf_loader_plugin_is_discovered_registered_and_loads_documents() -> None:
    result = PluginManager(PLUGIN_ROOT).load_plugins()

    assert [plugin.manifest.name for plugin in result.loaded_plugins] == ["pdf-loader"]
    assert result.rejected_plugins == ()

    register = result.loaded_plugins[0].entry_point_result
    assert callable(register)

    registry = Registry()
    register(registry)

    loader = registry.create("loader", "pdf")
    documents = loader.load(PDF_FIXTURE)

    assert isinstance(documents[0], Document)
    assert documents == [
        Document(
            content="relevant document about retrieval",
            metadata={"source": str(PDF_FIXTURE), "chunk_index": 0},
        )
    ]