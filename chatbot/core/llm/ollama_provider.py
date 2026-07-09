from __future__ import annotations

import httpx

from chatbot.config.settings import get_settings
from chatbot.core.llm.base import LLMProvider
from chatbot.utils.retry import retry


class OllamaProvider(LLMProvider):
    def __init__(self) -> None:
        self.settings = get_settings()

    @retry(retries=get_settings().MAX_RETRIES)
    def generate(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        payload = {
            "model": self.settings.OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "stream": False,
            "options": {"num_predict": max_tokens},
        }
        response = httpx.post(
            f"{self.settings.OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=self.settings.REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()

    @retry(retries=get_settings().MAX_RETRIES)
    def classify(self, prompt: str) -> str:
        return self.generate("Answer with only YES or NO.", prompt, max_tokens=1)

