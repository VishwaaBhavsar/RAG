from __future__ import annotations

import logging
from dataclasses import dataclass

from chatbot.config import domain_config
from chatbot.config.domain_config import OFF_TOPIC_REPLY, SYSTEM_PROMPT
from chatbot.config.settings import get_settings
from chatbot.core.guard.embedding_guard import EmbeddingGuard
from chatbot.core.guard.llm_guard import classify_with_llm
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
        guard: EmbeddingGuard | None = None,
        system_prompt: str = SYSTEM_PROMPT,
        off_topic_reply: str = OFF_TOPIC_REPLY,
        max_tokens: int | None = None,
    ) -> None:
        settings = get_settings()
        self.provider = provider
        self.guard = guard or EmbeddingGuard()
        self.domain_config = domain_config
        self.system_prompt = system_prompt
        self.off_topic_reply = off_topic_reply
        self.max_tokens = max_tokens or settings.MAX_TOKENS

    def chat(self, message: str) -> ChatResult:
        try:
            guard_result = self.guard.classify(message)
        except Exception:
            return ChatResult(response=self.off_topic_reply, on_topic=False)

        guard_score = getattr(guard_result, "score", None)
        guard_ambiguous = bool(getattr(guard_result, "ambiguous", False))
        guard_on_topic = bool(getattr(guard_result, "on_topic", False))
        guard_matched_example = getattr(guard_result, "matched_example", None)
        logger.debug(
            "Guard decision message=%r score=%s ambiguous=%s on_topic=%s matched_example=%r",
            message,
            guard_score,
            guard_ambiguous,
            guard_on_topic,
            guard_matched_example,
        )

        if not guard_ambiguous and not guard_on_topic:
            return ChatResult(response=self.off_topic_reply, on_topic=False)

        if guard_ambiguous:
            try:
                stage2_result = classify_with_llm(self.provider, message)
                logger.debug("Stage 2 LLM classify result=%s", stage2_result)
                if not stage2_result:
                    return ChatResult(response=self.off_topic_reply, on_topic=False)
            except Exception:
                logger.exception("LLM classification failed")
                return ChatResult(response=MODEL_UNAVAILABLE_REPLY, on_topic=True)

        try:
            response = self.provider.generate(self.system_prompt, message, self.max_tokens)
        except Exception:
            logger.exception("LLM generation failed")
            return ChatResult(response=MODEL_UNAVAILABLE_REPLY, on_topic=True)
        return ChatResult(response=response, on_topic=True)
