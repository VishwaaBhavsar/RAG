from __future__ import annotations

from chatbot.config.domain_config import build_classifier_prompt
from chatbot.core.llm.base import LLMProvider


def classify_with_llm(provider: LLMProvider, message: str) -> bool:
    try:
        output = provider.classify(build_classifier_prompt(message), max_tokens=5, temperature=0.0)
    except Exception:
        return False

    normalized = output.strip().upper()
    if normalized == "YES":
        return True
    if normalized == "NO":
        return False
    return False
