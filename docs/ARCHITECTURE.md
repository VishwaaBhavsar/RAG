# Architecture

## Current State

This repository is currently at Phase 9: repository skeleton, secure plugin manager, core provider registry, abstract provider contracts, DI container, YAML/env configuration loading, a core RAG pipeline plus chat engine, the first concrete plugin in its own plugin directory, and a FastAPI backend for document upload and chat.

The first runtime components now exist in `packages/plugins/` and `packages/core/`. The plugin manager scans each plugin directory independently, validates `manifest.json` before import, and records loaded and rejected plugins separately so startup can continue even if one plugin is broken. The first real plugin now lives under `packages/plugins/plugins/pdf_loader/`, keeping plugin-local config and entry-point code outside the core engine. The core registry stores provider factories by provider type and provider name so config can resolve directly to a factory lookup. The core package now also owns the abstract provider interfaces and in-memory fakes used for tests, plus the DI container that assembles a provider graph from tenant config, the settings loader that parses YAML plus environment overrides, and the chat/RAG orchestration layer that drives retrieval, context assembly, and generation.

## Intended System Shape

The framework will evolve into a multi-tenant single-deployment RAG platform with:
- a core engine for chat, retrieval, configuration, events, logging, and error handling,
- provider packages for LLMs, embeddings, vector stores, loaders, rerankers, tools, and memory,
- a plugin system that discovers and validates plugins at startup,
- shared utilities that are safe to reuse across packages,
- application entry points in `apps/` that consume the framework rather than owning business logic.

## Repository Structure

- `apps/api/` - FastAPI backend entry point.
- `apps/admin/` - future admin UI shell.
- `apps/web/` - future user-facing web shell.
- `packages/core/` - core engine, registry, configuration, DI, and orchestration primitives.
- `packages/providers/` - concrete provider implementations and adapter code.
- `packages/plugins/` - plugin discovery, validation, and loading support.
- `packages/shared/` - reusable shared primitives, types, and helpers.
- `tests/` - test fixtures and later integration coverage.
- `docs/` - architecture and decision history.
- `docker/` - container assets and deployment helpers.
- `scripts/` - local tooling and maintenance scripts.

## Notes

The docs will be updated at the end of every phase to record what exists, how the parts connect, and why key decisions were made.

## Phase 2 Summary

The plugin manager now treats each plugin as an isolated directory. A plugin is only imported after its manifest passes strict schema validation, and a failure in one plugin does not prevent healthy plugins from loading.

## Phase 3 Summary

The core registry now provides provider lookup by type and name. That gives later phases a single indirection layer between configuration and concrete implementations, which is the foundation for the DI container and tenant-specific provider graphs.

## Phase 4 Summary

The core package now defines the provider ABCs and data contracts that every concrete provider must satisfy. It also includes deterministic fake implementations that test later phases can use without reaching for real external services.

## Phase 5 Summary

The core DI container now resolves provider instances from the registry using a typed tenant config. It builds a provider graph without importing concrete implementations directly, which is the key seam for later configuration loading and request-scoped graph creation.

## Phase 6 Summary

The core settings layer now loads base app config from YAML and environment variables using `pydantic-settings`. Tenant overrides can be merged over that base config and revalidated before the DI container sees the final provider graph.

## Phase 7 Summary

The core chat engine and RAG pipeline now use the provider graph to embed a query, retrieve context, assemble a prompt, and generate an answer without importing concrete provider implementations.

## Phase 8 Summary

The first concrete plugin is now a self-contained PDF loader under `packages/plugins/plugins/pdf_loader/`. It is discovered through the plugin manager, validated through the manifest loader, and registered into the core registry as a loader factory without moving plugin-specific config into the core package.
## Phase 9 Summary

The API app now exposes a real FastAPI backend in pps/api/src/server.py. It accepts uploaded documents, supports JSON ingestion for text or file paths, and serves a /chat endpoint that routes questions through the Ollama-backed LLM provider while keeping plugin loading and core orchestration separate.
