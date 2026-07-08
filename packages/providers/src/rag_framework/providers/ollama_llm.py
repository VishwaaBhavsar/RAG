"""Ollama-backed LLM provider."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from rag_framework.core.contracts import BaseLLMProvider


class OllamaLLMError(RuntimeError):
    """Raised when the Ollama LLM provider cannot complete a request."""


@dataclass(frozen=True, slots=True)
class OllamaLLMConfig:
    """Configuration for the local Ollama LLM provider."""

    base_url: str = "http://localhost:11434"
    model: str = "llama3.2"
    timeout_seconds: float = 30.0

    @property
    def generate_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/api/generate"


class OllamaLLMProvider(BaseLLMProvider):
    """Generate text through a local Ollama instance."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2",
        timeout_seconds: float = 30.0,
    ) -> None:
        self.config = OllamaLLMConfig(
            base_url=base_url,
            model=model,
            timeout_seconds=timeout_seconds,
        )

    def generate(self, prompt: str, *, system_prompt: str | None = None) -> str:
        payload: dict[str, Any] = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
        }
        if system_prompt is not None:
            payload["system"] = system_prompt

        request = Request(
            self.config.generate_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.config.timeout_seconds) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:  # pragma: no cover - exercised through the generic error path
            raise OllamaLLMError(f"Ollama request failed with HTTP error: {exc}") from exc
        except URLError as exc:
            raise OllamaLLMError(f"Ollama request failed: {exc.reason}") from exc
        except TimeoutError as exc:
            raise OllamaLLMError(
                f"Ollama request timed out after {self.config.timeout_seconds} seconds"
            ) from exc
        except json.JSONDecodeError as exc:
            raise OllamaLLMError("Ollama response was not valid JSON") from exc

        if not isinstance(response_payload, dict):
            raise OllamaLLMError("Ollama response must be a JSON object")

        response_text = response_payload.get("response")
        if not isinstance(response_text, str):
            error_detail = response_payload.get("error")
            if isinstance(error_detail, str) and error_detail.strip():
                raise OllamaLLMError(error_detail)
            raise OllamaLLMError("Ollama response did not include generated text")

        return response_text
