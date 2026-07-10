from __future__ import annotations

import logging
from dataclasses import dataclass

from chatbot.config.domain_config import OFF_TOPIC_REPLY, SYSTEM_PROMPT, build_classifier_prompt
from chatbot.config.settings import get_settings
from chatbot.core.llm.base import LLMProvider

logger = logging.getLogger(__name__)

MODEL_UNAVAILABLE_REPLY = "I'm having trouble reaching the language model right now. Please try again."


@dataclass(frozen=True)
class ChatResult:
    response: str
    on_topic: bool


class Chatbot:
    def __init__(
        self,
        *,
        provider: LLMProvider,
        guard: object | None = None,
        system_prompt: str = SYSTEM_PROMPT,
        off_topic_reply: str = OFF_TOPIC_REPLY,
        max_tokens: int | None = None,
    ) -> None:
        settings = get_settings()
        self.provider = provider
        self.guard = guard
        self.system_prompt = system_prompt
        self.off_topic_reply = off_topic_reply
        self.max_tokens = max_tokens or settings.MAX_TOKENS

    def chat(self, message: str) -> ChatResult:
        if not message.strip():
            return ChatResult(response=self.off_topic_reply, on_topic=False)

        if self.guard is not None:
            try:
                guard_result = self.guard.classify(message)
            except Exception:
                return ChatResult(response=self.off_topic_reply, on_topic=False)

            guard_ambiguous = bool(getattr(guard_result, "ambiguous", False))
            guard_on_topic = bool(getattr(guard_result, "on_topic", False))

            if not guard_ambiguous and not guard_on_topic:
                return ChatResult(response=self.off_topic_reply, on_topic=False)

            if guard_ambiguous:
                try:
                    classifier_output = self.provider.classify(build_classifier_prompt(message), max_tokens=5, temperature=0.0)
                except Exception:
                    logger.exception("LLM classification failed")
                    if hasattr(self.provider, "classify_output"):
                        return ChatResult(response=self.off_topic_reply, on_topic=False)
                    return ChatResult(response=MODEL_UNAVAILABLE_REPLY, on_topic=True)
                if classifier_output.strip().upper() != "YES":
                    return ChatResult(response=self.off_topic_reply, on_topic=False)

        try:
            response = self.provider.generate(self.system_prompt, message, self.max_tokens)
        except Exception:
            logger.exception("LLM generation failed")
            return ChatResult(response=MODEL_UNAVAILABLE_REPLY, on_topic=True)
        return ChatResult(response=response, on_topic=response.strip() != self.off_topic_reply.strip())
