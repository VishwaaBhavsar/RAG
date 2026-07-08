"""Provider package placeholder.

Purpose:
    Reserve the providers module path for concrete adapters.

Responsibilities:
    - Keep provider-specific code separate from core engine code.
    - Make future imports stable for later phases.

Usage example:
    from rag_framework.providers import OllamaLLMProvider
"""

from .chroma_vector_store import ChromaVectorStore, ChromaVectorStoreConfig, ChromaVectorStoreError
from .cross_encoder_reranker import CrossEncoderReranker, CrossEncoderRerankerConfig, CrossEncoderRerankerError
from .in_memory_vector_store import InMemoryVectorStore
from .multilingual_embeddings import (
    MultilingualSentenceTransformersEmbeddingConfig,
    MultilingualSentenceTransformersEmbeddingError,
    MultilingualSentenceTransformersEmbeddingProvider,
)
from .noop_reranker import NoOpReranker
from .ollama_llm import OllamaLLMConfig, OllamaLLMError, OllamaLLMProvider
from .sentence_transformers_embeddings import (
    SentenceTransformersEmbeddingConfig,
    SentenceTransformersEmbeddingError,
    SentenceTransformersEmbeddingProvider,
)

__all__ = [
    "ChromaVectorStore",
    "ChromaVectorStoreConfig",
    "ChromaVectorStoreError",
    "CrossEncoderReranker",
    "CrossEncoderRerankerConfig",
    "CrossEncoderRerankerError",
    "InMemoryVectorStore",
    "MultilingualSentenceTransformersEmbeddingConfig",
    "MultilingualSentenceTransformersEmbeddingError",
    "MultilingualSentenceTransformersEmbeddingProvider",
    "NoOpReranker",
    "OllamaLLMConfig",
    "OllamaLLMError",
    "OllamaLLMProvider",
    "SentenceTransformersEmbeddingConfig",
    "SentenceTransformersEmbeddingError",
    "SentenceTransformersEmbeddingProvider",
]