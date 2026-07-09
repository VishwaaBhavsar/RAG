from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def classify(self, prompt: str) -> str:
        raise NotImplementedError

