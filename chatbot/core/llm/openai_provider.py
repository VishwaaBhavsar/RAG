from __future__ import annotations

import httpx

from chatbot.config.settings import get_settings
from chatbot.core.llm.base import LLMProvider
from chatbot.utils.retry import retry


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        self.settings = get_settings()

    @retry(retries=get_settings().MAX_RETRIES)
    def generate(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        payload = {
            "model": self.settings.OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "max_tokens": max_tokens,
        }
        headers = {"Authorization": f"Bearer {self.settings.OPENAI_API_KEY}"} if self.settings.OPENAI_API_KEY else {}
        base_url = str(self.settings.OPENAI_BASE_URL or "https://api.openai.com/v1")
        response = httpx.post(f"{base_url}/chat/completions", json=payload, headers=headers, timeout=self.settings.REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    @retry(retries=get_settings().MAX_RETRIES)
    def classify(self, prompt: str) -> str:
        return self.generate("Answer with only YES or NO.", prompt, max_tokens=1)

