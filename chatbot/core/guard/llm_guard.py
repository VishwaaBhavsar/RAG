from __future__ import annotations

from chatbot.config.domain_config import build_classifier_prompt
from chatbot.core.llm.base import LLMProvider


def classify_with_llm(provider: LLMProvider, message: str) -> bool:
    output = provider.classify(build_classifier_prompt(message)).strip().lower()
    if output.startswith("yes"):
        return True
    if output.startswith("no"):
        return False
    return "yes" in output and "no" not in output
