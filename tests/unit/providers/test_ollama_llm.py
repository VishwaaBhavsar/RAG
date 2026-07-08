"""Tests for the Ollama LLM provider."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from rag_framework.providers.ollama_llm import OllamaLLMError, OllamaLLMProvider


class _FakeHTTPResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    def __enter__(self) -> "_FakeHTTPResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


class _CapturedRequest(SimpleNamespace):
    pass


def test_ollama_llm_provider_posts_to_local_model_and_returns_generated_text(monkeypatch) -> None:
    captured = {}

    def fake_urlopen(request, timeout=None):
        captured["url"] = request.full_url
        captured["headers"] = dict(request.headers)
        captured["body"] = request.data.decode("utf-8")
        captured["timeout"] = timeout
        return _FakeHTTPResponse({"response": "ollama:hello from llama3.2"})

    monkeypatch.setattr("rag_framework.providers.ollama_llm.urlopen", fake_urlopen)

    provider = OllamaLLMProvider()
    result = provider.generate("hello", system_prompt="be brief")

    assert result == "ollama:hello from llama3.2"
    assert captured["url"].endswith("/api/generate")
    assert json.loads(captured["body"]) == {
        "model": "llama3.2",
        "prompt": "hello",
        "system": "be brief",
        "stream": False,
    }
    assert captured["timeout"] == provider.config.timeout_seconds

def test_ollama_llm_provider_wraps_timeout(monkeypatch) -> None:
    def fake_urlopen(request, timeout=None):
        raise TimeoutError("timed out")

    monkeypatch.setattr("rag_framework.providers.ollama_llm.urlopen", fake_urlopen)

    provider = OllamaLLMProvider(timeout_seconds=0.1)

    with pytest.raises(OllamaLLMError, match="timed out"):
        provider.generate("hello")


