"""Tests for the provider registry."""

from __future__ import annotations

import pytest

from rag_framework.core import Registry, register_default_llm_providers
from rag_framework.core.registry import RegistryDuplicateError, RegistryNotFoundError
from rag_framework.providers import OllamaLLMProvider


def test_registers_multiple_providers_for_the_same_type() -> None:
    registry = Registry()

    registry.register("llm", "openai", lambda: "openai")
    registry.register("llm", "ollama", lambda: "ollama")

    assert registry.get_factory("llm", "openai")() == "openai"
    assert registry.get_factory("llm", "ollama")() == "ollama"


def test_registers_built_in_llm_providers() -> None:
    registry = Registry()

    register_default_llm_providers(registry)

    assert registry.create("llm", "fake").__class__.__name__ == "FakeLLMProvider"
    assert isinstance(registry.create("llm", "ollama"), OllamaLLMProvider)


def test_duplicate_registration_is_rejected() -> None:
    registry = Registry()

    registry.register("llm", "openai", lambda: "openai")

    with pytest.raises(RegistryDuplicateError):
        registry.register("llm", "openai", lambda: "duplicate")


def test_missing_lookup_raises_clear_error() -> None:
    registry = Registry()

    with pytest.raises(RegistryNotFoundError):
        registry.get_factory("llm", "openai")