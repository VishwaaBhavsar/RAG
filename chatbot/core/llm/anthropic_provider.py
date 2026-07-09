from __future__ import annotations

import httpx

from chatbot.config.settings import get_settings
from chatbot.core.llm.base import LLMProvider
from chatbot.utils.retry import retry


class AnthropicProvider(LLMProvider):
    def __init__(self) -> None:
        self.settings = get_settings()

    @retry(retries=get_settings().MAX_RETRIES)
    def generate(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        payload = {
            "model": self.settings.ANTHROPIC_MODEL,
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_message}],
        }
        headers = {
            "x-api-key": self.settings.ANTHROPIC_API_KEY or "",
            "anthropic-version": "2023-06-01",
        }
        base_url = str(self.settings.ANTHROPIC_BASE_URL or "https://api.anthropic.com/v1")
        response = httpx.post(f"{base_url}/messages", json=payload, headers=headers, timeout=self.settings.REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
        return "".join(block.get("text", "") for block in data.get("content", [])).strip()

    @retry(retries=get_settings().MAX_RETRIES)
    def classify(self, prompt: str) -> str:
        return self.generate("Answer with only YES or NO.", prompt, max_tokens=1)

