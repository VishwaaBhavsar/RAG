from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int,
        temperature: float | None = None,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def classify(self, prompt: str, max_tokens: int = 5, temperature: float = 0.0) -> str:
        raise NotImplementedError
