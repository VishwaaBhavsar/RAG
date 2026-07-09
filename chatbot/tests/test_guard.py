from __future__ import annotations

import pytest

from chatbot.config.domain_config import DOMAIN_NAME
from chatbot.core.guard.embedding_guard import EmbeddingGuard


@pytest.fixture(scope="session")
def embedding_guard() -> EmbeddingGuard:
    return EmbeddingGuard()


@pytest.mark.integration
def test_healthcare_domain_classifies_on_topic_medical_questions(embedding_guard: EmbeddingGuard) -> None:
    result = embedding_guard.classify("what causes chest pain?")

    assert DOMAIN_NAME == "healthcare"
    assert result.on_topic is True


@pytest.mark.integration
def test_healthcare_domain_classifies_off_topic_school_questions(embedding_guard: EmbeddingGuard) -> None:
    result = embedding_guard.classify("what's the best school near me?")

    assert result.on_topic is False


@pytest.mark.integration
def test_healthcare_domain_keeps_common_medication_questions_on_topic(embedding_guard: EmbeddingGuard) -> None:
    result = embedding_guard.classify("what are the side effects of ibuprofen?")

    assert result.on_topic is True
