from __future__ import annotations

from dataclasses import dataclass

import pytest

from chatbot.config.domain_config import TOPIC_EXAMPLES, SYSTEM_PROMPT, build_classifier_prompt
from chatbot.core.chatbot import Chatbot
from chatbot.core.guard.embedding_guard import EmbeddingGuard
from chatbot.core.guard.llm_guard import classify_with_llm


@pytest.fixture(scope="module")
def guard() -> EmbeddingGuard:
    return EmbeddingGuard()


@dataclass(frozen=True)
class _GuardDecision:
    on_topic: bool
    ambiguous: bool
    score: float = 0.0
    matched_example: str | None = None


class _FakeGuard:
    def __init__(self, decision: _GuardDecision) -> None:
        self.decision = decision

    def classify(self, message: str) -> _GuardDecision:  # noqa: ARG002
        return self.decision


class _FakeProvider:
    def __init__(self, classify_output: str | Exception, generate_output: str = "final answer") -> None:
        self.classify_output = classify_output
        self.generate_output = generate_output
        self.classify_calls: list[tuple[str, int, float]] = []
        self.generate_calls: list[tuple[str, str, int, float | None]] = []

    def classify(self, prompt: str, max_tokens: int = 5, temperature: float = 0.0) -> str:
        self.classify_calls.append((prompt, max_tokens, temperature))
        if isinstance(self.classify_output, Exception):
            raise self.classify_output
        return self.classify_output

    def generate(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int,
        temperature: float | None = None,
    ) -> str:
        self.generate_calls.append((system_prompt, user_message, max_tokens, temperature))
        return self.generate_output


def test_healthcare_prompt_includes_safety_boundaries() -> None:
    prompt = SYSTEM_PROMPT.lower()

    assert "domain-locked healthcare information assistant" in prompt
    assert "do not diagnose" in prompt
    assert "call local emergency services now" in prompt
    assert "self-harm" in prompt
    assert "outside healthcare" in prompt


def test_classifier_prompt_is_strict_and_binary() -> None:
    prompt = build_classifier_prompt("what's the best school near me?").lower()

    assert "reply with only yes or no" in prompt
    assert "primarily about human health" in prompt
    assert "mostly about another topic" in prompt


def test_healthcare_topic_examples_include_abstract_and_wellness_phrasing() -> None:
    assert len(TOPIC_EXAMPLES) == 16
    assert "How does stress affect the body?" in TOPIC_EXAMPLES
    assert "What role does sleep play in immune health?" in TOPIC_EXAMPLES
    assert "How does exercise impact heart health?" in TOPIC_EXAMPLES
    assert "What is the connection between diet and mental health?" in TOPIC_EXAMPLES


@pytest.mark.parametrize(
    ("message",),
    [
        ("how does stress affect the body?",),
        ("what role does sleep play in immune health?",),
        ("how does exercise impact heart health?",),
        ("what is the connection between diet and mental health?",),
        ("how does chronic stress affect blood pressure?",),
        ("why is sleep important for recovery?",),
    ],
)
def test_abstract_healthcare_phrasing_is_not_confidently_off_topic(guard: EmbeddingGuard, message: str) -> None:
    result = guard.classify(message)

    assert result.on_topic or result.ambiguous, (
        f"Expected '{message}' to remain in the on-topic or ambiguous band, got "
        f"on_topic={result.on_topic}, ambiguous={result.ambiguous}, score={result.score}, "
        f"matched_example={result.matched_example!r}"
    )


def test_embedding_guard_accepts_clear_on_topic_input(guard: EmbeddingGuard) -> None:
    result = guard.classify("What are common side effects of ibuprofen?")

    assert result.on_topic is True
    assert result.ambiguous is False


def test_embedding_guard_rejects_clear_off_topic_input(guard: EmbeddingGuard) -> None:
    result = guard.classify("How do I fix my car engine?")

    assert result.on_topic is False
    assert result.ambiguous is False


def test_llm_classifier_accepts_exact_yes_only() -> None:
    provider = _FakeProvider("YES")

    assert classify_with_llm(provider, "I have stomachache.") is True
    assert provider.classify_calls[0][1:] == (5, 0.0)


def test_llm_classifier_rejects_invalid_output() -> None:
    provider = _FakeProvider("YES, maybe")

    assert classify_with_llm(provider, "I have stomachache.") is False


def test_llm_classifier_rejects_provider_failure() -> None:
    provider = _FakeProvider(RuntimeError("boom"))

    assert classify_with_llm(provider, "I have stomachache.") is False


def test_chatbot_accepts_ambiguous_message_through_llm_fallback() -> None:
    provider = _FakeProvider("YES", generate_output="health answer")
    chatbot = Chatbot(provider=provider, guard=_FakeGuard(_GuardDecision(on_topic=False, ambiguous=True)))

    result = chatbot.chat("I have stomachache.")

    assert result.on_topic is True
    assert result.response == "health answer"
    assert provider.generate_calls


def test_chatbot_rejects_ambiguous_message_through_llm_fallback() -> None:
    provider = _FakeProvider("NO")
    chatbot = Chatbot(provider=provider, guard=_FakeGuard(_GuardDecision(on_topic=False, ambiguous=True)))

    result = chatbot.chat("I have stomachache.")

    assert result.on_topic is False
    assert result.response == chatbot.off_topic_reply
    assert provider.generate_calls == []


def test_chatbot_rejects_invalid_classifier_response() -> None:
    provider = _FakeProvider("maybe")
    chatbot = Chatbot(provider=provider, guard=_FakeGuard(_GuardDecision(on_topic=False, ambiguous=True)))

    result = chatbot.chat("I have stomachache.")

    assert result.on_topic is False
    assert result.response == chatbot.off_topic_reply
    assert provider.generate_calls == []


def test_chatbot_rejects_provider_failure_during_llm_classification() -> None:
    provider = _FakeProvider(RuntimeError("boom"))
    chatbot = Chatbot(provider=provider, guard=_FakeGuard(_GuardDecision(on_topic=False, ambiguous=True)))

    result = chatbot.chat("I have stomachache.")

    assert result.on_topic is False
    assert result.response == chatbot.off_topic_reply
    assert provider.generate_calls == []
