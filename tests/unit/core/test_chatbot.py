from __future__ import annotations

from types import SimpleNamespace

from chatbot.core.chatbot import ChatResult, Chatbot, MODEL_UNAVAILABLE_REPLY


class _FakeGuard:
    def __init__(self, result: object) -> None:
        self._result = result

    def classify(self, message: str):
        return self._result


class _FakeProvider:
    def __init__(self, *, generate_exc: Exception | None = None, classify_exc: Exception | None = None) -> None:
        self.generate_exc = generate_exc
        self.classify_exc = classify_exc

    def generate(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        if self.generate_exc is not None:
            raise self.generate_exc
        return "healthcare answer"

    def classify(self, prompt: str) -> str:
        if self.classify_exc is not None:
            raise self.classify_exc
        return "YES"


def test_chatbot_returns_llm_answer_for_on_topic_message() -> None:
    chatbot = Chatbot(
        provider=_FakeProvider(),
        guard=_FakeGuard(SimpleNamespace(ambiguous=False, on_topic=True)),
        max_tokens=16,
    )

    result = chatbot.chat("What should I do for a fever?")

    assert result == ChatResult(response="healthcare answer", on_topic=True)


def test_chatbot_falls_back_when_generation_fails() -> None:
    chatbot = Chatbot(
        provider=_FakeProvider(generate_exc=RuntimeError("timed out")),
        guard=_FakeGuard(SimpleNamespace(ambiguous=False, on_topic=True)),
        max_tokens=16,
    )

    result = chatbot.chat("What should I do for a fever?")

    assert result.response == MODEL_UNAVAILABLE_REPLY
    assert result.on_topic is True


def test_chatbot_falls_back_when_ambiguous_classification_fails() -> None:
    chatbot = Chatbot(
        provider=_FakeProvider(classify_exc=RuntimeError("timed out")),
        guard=_FakeGuard(SimpleNamespace(ambiguous=True, on_topic=False)),
        max_tokens=16,
    )

    result = chatbot.chat("I have a question")

    assert result.response == MODEL_UNAVAILABLE_REPLY
    assert result.on_topic is True
