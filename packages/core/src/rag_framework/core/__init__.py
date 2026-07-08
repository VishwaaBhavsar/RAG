"""Core framework module.

Purpose:
    Expose the core registry, provider contracts, configuration models, DI container, and chat orchestration.

Responsibilities:
    - Provide an import location for core abstractions.
    - Keep the package boundary visible before implementation begins.
    - Export the registry used by later DI and configuration phases.
    - Export the abstract provider interfaces, test fakes, settings loader, RAG pipeline, and chat engine.

Usage example:
    from rag_framework.core import AppConfig, ChatEngine, Container, Registry
"""

from .app_config import (
    AppConfig,
    ConfigLoaderError,
    ProviderSelection,
    TenantConfig,
    TenantConfigPatch,
    load_app_config,
    merge_tenant_config,
)
from .chat import ChatEngine
from .contracts import (
    BaseEmbeddingProvider,
    BaseLLMProvider,
    BaseLoader,
    BaseMemory,
    BaseReranker,
    BaseTool,
    BaseVectorStore,
    ChatMessage,
    Document,
    VectorRecord,
    VectorSearchResult,
)
from .di_container import Container, ContainerError, ProviderGraph
from .fakes import (
    FakeEmbeddingProvider,
    FakeLLMProvider,
    FakeLoader,
    FakeMemory,
    FakeReranker,
    FakeTool,
    FakeVectorStore,
)
from .pipeline import RAGPipeline, RAGResponse
from .registry import (
    Registry,
    RegistryDuplicateError,
    RegistryError,
    RegistryNotFoundError,
    register_default_embedding_providers,
    register_default_llm_providers,
    register_default_vector_store_providers,
)

__all__ = [
    "AppConfig",
    "BaseEmbeddingProvider",
    "BaseLLMProvider",
    "BaseLoader",
    "BaseMemory",
    "BaseReranker",
    "BaseTool",
    "BaseVectorStore",
    "ChatEngine",
    "ChatMessage",
    "ConfigLoaderError",
    "Container",
    "ContainerError",
    "Document",
    "FakeEmbeddingProvider",
    "FakeLLMProvider",
    "FakeLoader",
    "FakeMemory",
    "FakeReranker",
    "FakeTool",
    "FakeVectorStore",
    "ProviderGraph",
    "ProviderSelection",
    "RAGPipeline",
    "RAGResponse",
    "Registry",
    "RegistryDuplicateError",
    "RegistryError",
    "RegistryNotFoundError",
    "TenantConfig",
    "TenantConfigPatch",
    "VectorRecord",
    "VectorSearchResult",
    "load_app_config",
    "merge_tenant_config",
    "register_default_embedding_providers",
    "register_default_llm_providers",
    "register_default_vector_store_providers",
]