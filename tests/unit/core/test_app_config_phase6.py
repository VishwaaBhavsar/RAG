"""Tests for Phase 6 configuration loading and tenant override merging."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
import yaml

from rag_framework.core.app_config import (
    AppConfig,
    ProviderSelection,
    TenantConfig,
    TenantConfigPatch,
    load_app_config,
    merge_tenant_config,
)
from rag_framework.core.di_container import Container
from rag_framework.core.fakes import (
    FakeEmbeddingProvider,
    FakeLLMProvider,
    FakeLoader,
    FakeMemory,
    FakeReranker,
    FakeTool,
    FakeVectorStore,
)
from rag_framework.core.registry import Registry


def _write_base_config(path: Path, llm_provider: str = "openai") -> Path:
    path.write_text(
        yaml.safe_dump(
            {
                "llm": {"provider": llm_provider},
                "embedding": {"provider": "bge"},
                "vectordb": {"provider": "qdrant"},
                "loader": {"provider": "pdf"},
                "tools": [{"provider": "calculator"}],
                "reranker": {"provider": "default"},
                "memory": {"provider": "default"},
            }
        ),
        encoding="utf-8",
    )
    return path


def test_load_app_config_reads_yaml_and_env_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp_dir:
        yaml_file = _write_base_config(Path(temp_dir) / "app.yaml", llm_provider="openai")
        monkeypatch.setenv("RAG_FRAMEWORK_LLM__PROVIDER", "ollama")

        config = load_app_config(yaml_file)

        assert isinstance(config, AppConfig)
        assert config.llm.provider == "ollama"
        assert config.embedding.provider == "bge"
        assert config.vectordb.provider == "qdrant"
        assert config.tools == (ProviderSelection(provider="calculator"),)


def test_merge_tenant_config_and_container_builds_new_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp_dir:
        yaml_file = _write_base_config(Path(temp_dir) / "app.yaml", llm_provider="openai")
        monkeypatch.delenv("RAG_FRAMEWORK_LLM__PROVIDER", raising=False)

        base_config = load_app_config(yaml_file)
        tenant_config = merge_tenant_config(
            base_config,
            TenantConfigPatch.model_validate({"llm": {"provider": "ollama"}}),
        )

        assert isinstance(tenant_config, TenantConfig)
        assert tenant_config.llm == ProviderSelection(provider="ollama")

        registry = Registry()
        openai_llm = FakeLLMProvider(prefix="openai")
        ollama_llm = FakeLLMProvider(prefix="ollama")
        embedding = FakeEmbeddingProvider()
        vector_store = FakeVectorStore()
        loader = FakeLoader()
        calculator = FakeTool(tool_name="calculator")
        reranker = FakeReranker()
        memory = FakeMemory()

        registry.register("llm", "openai", lambda: openai_llm)
        registry.register("llm", "ollama", lambda: ollama_llm)
        registry.register("embedding", "bge", lambda: embedding)
        registry.register("vectordb", "qdrant", lambda: vector_store)
        registry.register("loader", "pdf", lambda: loader)
        registry.register("tool", "calculator", lambda: calculator)
        registry.register("reranker", "default", lambda: reranker)
        registry.register("memory", "default", lambda: memory)

        graph = Container(registry).build(tenant_config)

        assert graph.llm is ollama_llm
        assert graph.embedding is embedding
        assert graph.vector_store is vector_store
        assert graph.loader is loader
        assert graph.tools == (calculator,)
        assert graph.reranker is reranker
        assert graph.memory is memory
