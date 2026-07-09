from __future__ import annotations

import pytest

from chatbot.config.domain_config import TOPIC_EXAMPLES, SYSTEM_PROMPT, build_classifier_prompt
from chatbot.core.guard.embedding_guard import EmbeddingGuard


@pytest.fixture(scope="module")
def guard() -> EmbeddingGuard:
    return EmbeddingGuard()


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
