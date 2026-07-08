# RAG Framework

A local, extensible Retrieval-Augmented Generation framework for uploading documents and asking questions about them.

The current backend can:

- upload PDF or text files
- extract readable document text
- store uploaded content in an in-memory knowledge base
- embed uploaded content and retrieve relevant document chunks by vector similarity
- answer with a local Ollama LLM, using `llama3.2` by default
- fall back to a simple document-based answer if the LLM times out or says it does not know

This repository is intentionally structured as a framework, not just one script. The core contracts, provider registry, plugins, and API are separated so new loaders, LLM providers, vector stores, and apps can be added without rewriting the whole system.

## Big Picture

```text
User / Postman / Future UI
        |
        v
FastAPI backend
apps/api/src/server.py
        |
        v
Document loading
PDF plugin or text loader
        |
        v
ChromaDB vector store
persistent local vectors + cosine similarity
        |
        v
Reranker
optional cross-encoder reranking
        |
        v
LLM provider
Ollama llama3.2 or fake provider
        |
        v
Answer + retrieved context
```

## Repository Layout

```text
apps/
  api/
    src/server.py                  FastAPI backend and API routes
  admin/                           placeholder for future admin UI
  web/                             placeholder for future web UI

packages/
  core/
    src/rag_framework/core/
      contracts.py                 shared interfaces like BaseLLMProvider and BaseLoader
      registry.py                  provider/plugin factory registry
      fakes.py                     fake test provider implementations
      pipeline.py                  early reusable RAG pipeline skeleton
      chat.py                      early chat abstraction skeleton
      di_container.py              dependency-injection skeleton
      settings.py                  settings/config helpers

  providers/
    src/rag_framework/providers/
      ollama_llm.py                real Ollama LLM provider

  plugins/
    src/rag_framework/plugins/
      manager.py                   loads plugin folders from disk
      manifest.py                  validates plugin manifests
      errors.py                    plugin-specific errors
    plugins/
      pdf_loader/
        manifest.json              plugin metadata
        plugin.py                  PDF text extraction loader
        config.py                  PDF extraction configuration

  shared/                          placeholder for shared utilities

tests/
  unit/                            unit tests for API, providers, plugins, and core
  fixtures/                        sample files and plugin fixtures

docs/
  superpowers/plans/               implementation plans and phase notes

scripts/                           helper scripts for development
docker/                            future container/deployment assets
```

## How The Backend Works

The main backend file is:

```text
apps/api/src/server.py
```

Startup flow:

```text
create_app()
  -> _build_registry()
      -> register_default_llm_providers()
          -> registers fake and ollama LLM providers
      -> PluginManager(...).load_plugins()
          -> loads plugins from packages/plugins/plugins
          -> registers the PDF loader
  -> creates BackendState
      -> registry
      -> in-memory knowledge base
      -> selected LLM provider
  -> registers FastAPI routes
```

Question-answering flow:

```text
/chat-with-file
  -> read uploaded file
  -> if PDF, call PDF loader plugin
  -> if text, decode text directly
  -> embed documents and upsert vectors into ChromaDB
  -> embed the question and retrieve a wider candidate set from ChromaDB
  -> optionally re-rank candidates with a reranker
  -> return the final top-k documents
  -> build prompt with question + context
  -> call selected LLM provider
  -> return answer, context, and matched documents
```

## API Endpoints

Open the interactive API docs after starting the server:

```text
http://127.0.0.1:8000/docs
```

Available endpoints:

```text
GET  /health
POST /documents/upload
POST /ingest
POST /chat
POST /ask
POST /chat-with-file
```

### `GET /health`

Checks that the backend is running.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

### `POST /chat-with-file`

Best endpoint for testing RAG in one request.

Use Postman form-data:

```text
file:     your-document.pdf
question: What is the main topic of the uploaded document?
```

Request:

```text
POST http://127.0.0.1:8000/chat-with-file
Content-Type: multipart/form-data
```

Example Postman CLI:

```powershell
postman request POST 'http://127.0.0.1:8000/chat-with-file' `
  --form 'file=@/C:/Users/Vishava/Downloads/about_faq.pdf' `
  --form 'question=What is the main topic of the uploaded document?'
```

The response includes:

```json
{
  "answer": "...",
  "context": "...",
  "documents": []
}
```

`context` and `documents` are returned on purpose for debugging so you can see exactly what text was retrieved.

### `POST /documents/upload` then `POST /chat`

Use this when you want to upload once, then ask multiple questions.

Upload:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/documents/upload `
  -Form @{ file = Get-Item C:\Users\Vishava\Downloads\about_faq.pdf }
```

Ask:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/chat `
  -ContentType 'application/json' `
  -Body '{"question":"Do they offer sugar-free cakes?"}'
```

### `POST /ingest`

Use this to ingest raw text or a server-side file path.

Text payload:

```json
{
  "text": "Dogs are loyal animals.",
  "source": "manual-note"
}
```

Path payload:

```json
{
  "path": "C:\\Users\\Vishava\\Downloads\\about_faq.pdf"
}
```

## Run Locally

### 1. Create and activate a virtual environment

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

If your terminal shows `(env)`, the venv is active.

### 2. Install the project

```powershell
python -m pip install -e .[dev]
```

If PowerShell has trouble with brackets, use:

```powershell
python -m pip install -e ".[dev]"
```

### 3. Install or start Ollama

This backend uses the local `llama3.2` model by default.

```powershell
ollama pull llama3.2
ollama serve
```

If `ollama serve` says Ollama is already running, that is fine.

### 4. Start the backend

From the repository root:

```powershell
python .\apps\api\src\server.py
```

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Provider Selection

The active LLM provider is selected with:

```text
RAG_FRAMEWORK_LLM__PROVIDER
```

Default:

```text
ollama
```

Use the real local Ollama provider:

```powershell
$env:RAG_FRAMEWORK_LLM__PROVIDER = "ollama"
python .\apps\api\src\server.py
```

Use the fake provider for quick testing without Ollama:

```powershell
$env:RAG_FRAMEWORK_LLM__PROVIDER = "fake"
python .\apps\api\src\server.py
```

Registered LLM providers live in:

```text
packages/core/src/rag_framework/core/registry.py
```

The real Ollama provider lives in:

```text
packages/providers/src/rag_framework/providers/ollama_llm.py
```

The active embeddings provider is selected with:

```text
RAG_FRAMEWORK_EMBEDDINGS__PROVIDER
```

Default:

```text
sentence-transformers
```

Use the real semantic embeddings provider:

```powershell
python -m pip install -e ".[embeddings]"
$env:RAG_FRAMEWORK_EMBEDDINGS__PROVIDER = "sentence-transformers"
python .\apps\api\src\server.py
```

The sentence-transformers provider lives in:

```text
packages/providers/src/rag_framework/providers/sentence_transformers_embeddings.py
```

The active vector store provider is selected with:

```text
RAG_FRAMEWORK_VECTORSTORE__PROVIDER
```

Default:

```text
chroma
```

ChromaDB persists vectors locally in `.chroma_data/` by default. Use the in-memory vector store only for fast tests or temporary smoke runs:

```powershell
$env:RAG_FRAMEWORK_VECTORSTORE__PROVIDER = "in-memory"
python .\apps\api\src\server.py
```

The active reranker provider is selected with:

```text
RAG_FRAMEWORK_RERANKER__PROVIDER
```

Default:

```text
cross-encoder
```

Use `none` for fast or no-download testing:

```powershell
$env:RAG_FRAMEWORK_RERANKER__PROVIDER = "none"
python .\apps\api\src\server.py
```

Use the cross-encoder reranker after you have installed the sentence-transformers dependency:

```powershell
python -m pip install -e ".[embeddings]"
$env:RAG_FRAMEWORK_RERANKER__PROVIDER = "cross-encoder"
python .\apps\api\src\server.py
```

Use the fake embeddings provider only when you want fast local smoke tests without loading the real model:

```powershell
$env:RAG_FRAMEWORK_EMBEDDINGS__PROVIDER = "fake"
python .\apps\api\src\server.py
```

## How Plugins Work

Plugins are filesystem folders under:

```text
packages/plugins/plugins/
```

The backend loads plugins during startup:

```text
apps/api/src/server.py
  -> _build_registry()
  -> PluginManager(plugin_root).load_plugins()
  -> plugin register function adds providers/loaders to Registry
```

The current PDF loader plugin is:

```text
packages/plugins/plugins/pdf_loader/
```

Important files:

```text
manifest.json      describes the plugin and entry point
plugin.py          implements the loader and registration function
config.py          stores PDF extraction settings
README.md          plugin-specific notes
```

The PDF loader implements the core loader interface:

```text
BaseLoader.load(source: str | Path) -> list[Document]
```

That interface is defined in:

```text
packages/core/src/rag_framework/core/contracts.py
```

PDF extraction tries multiple strategies:

```text
pypdf text extraction
  -> pdftotext / Poppler if available
  -> OCR with Poppler + Tesseract if configured and available
  -> simple fallback parser
```

If the PDF is a scanned image and OCR tools are not installed, the API returns a clear `400` explaining that no extractable text was found.

## Where To Change Files For New Features

Use this table when adding features.

| Feature | Files to change |
| --- | --- |
| Add a new API route | `apps/api/src/server.py` |
| Change request/response models | `apps/api/src/server.py` |
| Add a new LLM provider | `packages/providers/src/rag_framework/providers/<name>.py` and `packages/core/src/rag_framework/core/registry.py` |
| Add a new document loader plugin | `packages/plugins/plugins/<plugin_name>/manifest.json`, `plugin.py`, and `config.py` |
| Change plugin loading behavior | `packages/plugins/src/rag_framework/plugins/manager.py` |
| Change plugin manifest validation | `packages/plugins/src/rag_framework/plugins/manifest.py` |
| Add or change core interfaces | `packages/core/src/rag_framework/core/contracts.py` |
| Change provider lookup or registration | `packages/core/src/rag_framework/core/registry.py` |
| Change RAG retrieval behavior in current API | `apps/api/src/server.py`, especially `InMemoryKnowledgeBase.add_documents()` and `InMemoryKnowledgeBase.search()` |
| Add or change vector database support | add a `BaseVectorStore` implementation, register it, and select it with `RAG_FRAMEWORK_VECTORSTORE__PROVIDER` |
| Add or change embedding support | add a `BaseEmbeddingProvider` implementation, register it, and select it with `RAG_FRAMEWORK_EMBEDDINGS__PROVIDER` |
| Add or change reranking support | add a `BaseReranker` implementation, register it, and select it with `RAG_FRAMEWORK_RERANKER__PROVIDER` |
| Add tests for API behavior | `tests/unit/api/` |
| Add tests for providers | `tests/unit/providers/` |
| Add tests for plugins | `tests/unit/plugins/` |

## Retrieval Eval

Run the standalone retrieval evaluation harness with:

```powershell
python scripts/eval_retrieval.py
```

By default it uses the in-memory vector store for a clean, isolated run. To try the
Chroma-backed store instead, pass:

```powershell
python scripts/eval_retrieval.py --vector-store chroma
```

The script prints the fixed corpus and eval cases first, then runs the same cases twice:

- `reranker=none`
- `reranker=cross-encoder`

The summary shows how many cases passed, the pass rate as a percentage, and a failure
breakdown with the retrieved source and top document content. The side-by-side line at
the end makes it easy to compare whether reranking improved retrieval quality.

## Adding A New LLM Provider

1. Implement `BaseLLMProvider`.

```python
from rag_framework.core.contracts import BaseLLMProvider


class MyLLMProvider(BaseLLMProvider):
    def generate(self, prompt: str, *, system_prompt: str | None = None) -> str:
        return "generated answer"
```

2. Put the provider in:

```text
packages/providers/src/rag_framework/providers/my_llm.py
```

3. Register it in:

```text
packages/core/src/rag_framework/core/registry.py
```

4. Select it with:

```powershell
$env:RAG_FRAMEWORK_LLM__PROVIDER = "my-provider-name"
```

## Adding A New Loader Plugin

Create a folder:

```text
packages/plugins/plugins/my_loader/
```

Add:

```text
manifest.json
plugin.py
config.py
README.md
```

The loader class should implement:

```text
BaseLoader
```

The plugin should expose a registration function that receives the registry and registers the loader.

Conceptually:

```python
def register(registry):
    registry.register("loader", "my-loader", lambda: MyLoader())
```

## Why There Are Many README Files

The root `README.md` is the starting point for the whole project.

The smaller README files exist so each folder can explain itself locally:

```text
apps/api/README.md                 API-specific notes
packages/core/README.md            core package notes
packages/plugins/README.md         plugin package notes
packages/plugins/plugins/...       individual plugin notes
packages/providers/README.md       provider package notes
tests/README.md                    testing notes
docs/README.md                     architecture documentation notes
```

This is useful in a monorepo because a new contributor can open any folder and quickly understand what belongs there.

## Test And Lint

Run focused tests:

```powershell
python -m pytest tests\unit\api tests\unit\providers tests\unit\plugins -v --basetemp .pytest-tmp
```

Run lint:

```powershell
python -m ruff check apps\api\src packages\core\src packages\providers\src packages\plugins tests
```

Run type checks:

```powershell
python -m mypy packages\core\src packages\providers\src packages\plugins\src
```

Run slow integration tests for real semantic embeddings:

```powershell
python -m pip install -e ".[embeddings]"
python -m pytest -m integration tests\integration -v
```

Normal pytest runs exclude `integration` tests by default.

## Troubleshooting

### Port 8000 is already in use

Find the process:

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen | Select-Object OwningProcess
```

Stop it:

```powershell
Stop-Process -Id <PID>
```

Or start the server on a different port by editing the `uvicorn.run(...)` call in:

```text
apps/api/src/server.py
```

### PDF says no extractable text found

Common causes:

- the PDF is scanned image-only
- the active virtual environment does not have `pypdf`
- Poppler/Tesseract are not installed for richer extraction/OCR

First try:

```powershell
python -m pip install pypdf
```

Then restart the backend.

### Ollama times out

Make sure Ollama is running and the model exists:

```powershell
ollama pull llama3.2
ollama serve
```

The backend catches LLM failures when document context exists and returns a simple document-based fallback answer instead of crashing.

### `/chat` says it does not know

Use `/documents/upload` first, or use `/chat-with-file` to upload a file and ask in one request.

`/chat` only answers from documents already stored in the current server process memory. Restarting the server clears that memory.

## Current Limitations

- Retrieval is embedding-based with cosine similarity and persists locally through ChromaDB by default.
- There is no frontend UI yet.
- Scanned PDFs need OCR tools to extract text reliably.

These are intentional early-phase tradeoffs. The package boundaries are already prepared so richer embeddings, production-grade remote vector storage, document management, and UI apps can be added later.
