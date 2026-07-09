from __future__ import annotations

from dataclasses import dataclass

from chatbot.core.chatbot import Chatbot
from chatbot.core.guard.embedding_guard import EmbeddingGuard
from chatbot.core.llm.base import LLMProvider


@dataclass
class FakeLLMProvider(LLMProvider):
    generated_calls: list[tuple[str, str, int]]
    classify_calls: list[str]

    def generate(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        self.generated_calls.append((system_prompt, user_message, max_tokens))
        return f"ANSWER::{user_message}"

    def classify(self, prompt: str) -> str:
        self.classify_calls.append(prompt)
        return "YES"


def test_chatbot_short_circuits_off_topic_queries() -> None:
    provider = FakeLLMProvider(generated_calls=[], classify_calls=[])
    chatbot = Chatbot(provider=provider)

    result = chatbot.chat("what's the best school near me?")

    assert result.on_topic is False
    assert result.response == chatbot.domain_config.OFF_TOPIC_REPLY
    assert provider.generated_calls == []
    assert provider.classify_calls == []


def test_chatbot_uses_llm_for_on_topic_queries() -> None:
    provider = FakeLLMProvider(generated_calls=[], classify_calls=[])
    chatbot = Chatbot(provider=provider)

    result = chatbot.chat("what causes chest pain?")

    assert result.on_topic is True
    assert result.response.startswith("ANSWER::")
    assert provider.generated_calls
    assert "domain-locked healthcare information assistant" in provider.generated_calls[0][0].lower()
    assert "call local emergency services now" in provider.generated_calls[0][0].lower()


def test_chatbot_uses_classify_for_ambiguous_queries() -> None:
    provider = FakeLLMProvider(generated_calls=[], classify_calls=[])
    chatbot = Chatbot(provider=provider, guard=EmbeddingGuard(upper_threshold=0.99, lower_threshold=0.0))

    result = chatbot.chat("how do I make a plan?")

    assert provider.classify_calls
    assert "reply with only yes or no" in provider.classify_calls[0].lower()
    assert result.response.startswith("ANSWER::")
