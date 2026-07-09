from __future__ import annotations

from fastapi.testclient import TestClient

from chatbot.api import app as app_module


class FakeProvider:
    def generate(self, system_prompt: str, user_message: str, max_tokens: int) -> str:
        return "cached answer"

    def classify(self, prompt: str) -> str:
        return "YES"


class FakeChatbot:
    instances = 0

    def __init__(self, *, provider) -> None:
        FakeChatbot.instances += 1
        self.provider = provider

    def chat(self, message: str):
        return type("Result", (), {"response": "cached answer", "on_topic": True})()


def test_chatbot_is_created_once_and_reused(monkeypatch) -> None:
    FakeChatbot.instances = 0
    monkeypatch.setattr(app_module, "get_llm_provider", lambda: FakeProvider())
    monkeypatch.setattr(app_module, "Chatbot", FakeChatbot)

    with TestClient(app_module.app) as client:
        first = client.post("/chat", json={"message": "what causes chest pain?"})
        second = client.post("/chat", json={"message": "what causes chest pain?"})

    assert first.status_code == 200
    assert second.status_code == 200
    assert FakeChatbot.instances == 1

