# Decisions

## 2026-07-07 - Multi-tenant single deployment

Decision:
Build the framework as a single deployment that serves many tenants, with tenant-specific configuration and isolation enforced at runtime.

Why:
This keeps the framework reusable across clients while preserving a single operational footprint and enabling per-tenant provider selection through configuration.

Rejected alternatives:
- Clone-and-configure deployments per customer, which would multiply operational overhead and make framework improvements harder to share.
- A single global configuration, which would not support tenant isolation or per-tenant provider graphs.

## 2026-07-07 - Phase 1 repository skeleton first

Decision:
Start with a documentation-first monorepo skeleton before adding runtime code.

Why:
The later phases depend on stable boundaries between packages. A documented skeleton makes those boundaries explicit before implementation begins.

Rejected alternatives:
- Building the plugin manager or registry first, which would risk locking in package boundaries before the broader architecture was visible.

## 2026-07-07 - Strict plugin manifests and isolated failures

Decision:
Validate every plugin manifest against a strict schema before any import, and keep plugin failures isolated so one broken plugin does not stop the rest of startup.

Why:
This reduces the attack surface of plugin loading, keeps malformed plugins from executing, and preserves partial startup when one plugin is invalid.

Rejected alternatives:
- Best-effort manifest parsing, which would make the loader permissive and harder to reason about.
- Failing the entire scan when one plugin is invalid, which would turn a single bad plugin into a full startup outage.

## 2026-07-07 - Registry keyed by provider type and provider name

Decision:
Use a typed registry that maps provider type plus provider name to a single factory and rejects duplicate registrations.

Why:
This keeps provider selection data-driven, makes it easy to have multiple implementations of the same interface, and creates a stable lookup layer for the DI container.

Rejected alternatives:
- A single flat registry keyed only by provider name, which would make cross-type collisions easy and blur the meaning of the registered implementation.
- Hardcoded provider branching in the core engine, which would defeat the plugin-based architecture and make configuration-driven switching impossible.

## 2026-07-07 - Abstract provider interfaces in core

Decision:
Define the provider ABCs in the core package and keep deterministic fake implementations there for tests.

Why:
The core engine must depend on behavior contracts rather than concrete integrations, and the fake implementations give later phases a stable way to test orchestration without external services.

Rejected alternatives:
- Defining the interfaces in provider packages, which would invert the dependency direction and let concrete integrations own the contract surface.
- Skipping fake implementations, which would make the next phases harder to verify in isolation.

## 2026-07-07 - DI container builds provider graphs from tenant config

Decision:
Have the core container resolve provider factories from the registry using typed tenant config selections.

Why:
This keeps the graph assembly logic centralized, makes the runtime provider graph fully data-driven, and preserves the registry as the only place that knows how names map to implementations.

Rejected alternatives:
- Instantiating providers directly inside business logic, which would bypass the registry and hardcode implementation choices.
- Embedding provider-specific conditionals in the container, which would turn orchestration into a switch statement and make later provider additions invasive.

## 2026-07-08 - YAML and env config loading with tenant merge

Decision:
Load base app config with `pydantic-settings` from YAML plus environment variables, then merge tenant overrides into a validated tenant config before building the provider graph.

Why:
This keeps configuration data-driven, allows env vars to override defaults without code changes, and preserves a single validation path for both startup config and tenant-specific changes.

Rejected alternatives:
- Parsing YAML manually and skipping `pydantic-settings`, which would weaken validation and make env handling more ad hoc.
- Treating tenant overrides as an untyped dict passed straight into the container, which would push config validation into orchestration code.

## 2026-07-08 - Core RAG pipeline and chat engine

Decision:
Use the provider graph to drive retrieval, context assembly, and generation inside the core package, with a chat engine wrapper on top.

Why:
This keeps the retrieval and generation flow centralized, avoids direct dependencies on concrete providers, and gives the application layer a single chat-facing API.

Rejected alternatives:
- Putting retrieval logic in application entry points, which would duplicate orchestration and weaken the framework boundary.
- Having the pipeline import concrete providers directly, which would break the registry/DI abstraction and make future provider swaps invasive.

## 2026-07-08 - Self-contained PDF loader plugin

Decision:
Keep the first real loader implementation in its own plugin directory under `packages/plugins/plugins/pdf_loader/`, with plugin-local config and a manifest-driven entry point that registers a loader factory.

Why:
This proves the plugin manager can load a standalone plugin end to end, keeps plugin-specific configuration outside the core engine, and makes it clear where additional loaders should live as the plugin surface grows.

Rejected alternatives:
- Moving the first loader into `packages/core/`, which would blur the plugin boundary and make the core package responsible for plugin-local concerns.
- Hardcoding loader registration in startup code, which would bypass the manifest/manager flow and reduce the value of the plugin system.
## 2026-07-08 - FastAPI document ingest and chat backend

Decision:
Add a small FastAPI service in pps/api/src/server.py with document upload and /chat endpoints, backed by the existing plugin loader and Ollama LLM provider.

Why:
This gives the framework a concrete HTTP surface for ingesting documents and asking questions while preserving the core/registry/provider boundaries already established in earlier phases.

Rejected alternatives:
- Keeping only the custom http.server implementation, which made the backend harder to extend and less ergonomic for file uploads.
- Moving ingestion and chat logic into the core pipeline, which would blur application concerns with framework orchestration.
