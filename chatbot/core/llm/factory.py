from __future__ import annotations

from chatbot.config.settings import get_settings
from chatbot.core.llm.anthropic_provider import AnthropicProvider
from chatbot.core.llm.base import LLMProvider
from chatbot.core.llm.ollama_provider import OllamaProvider
from chatbot.core.llm.openai_provider import OpenAIProvider


def get_llm_provider() -> LLMProvider:
    provider_name = get_settings().LLM_PROVIDER.strip().lower()
    if provider_name == "openai":
        return OpenAIProvider()
    if provider_name == "anthropic":
        return AnthropicProvider()
    return OllamaProvider()

