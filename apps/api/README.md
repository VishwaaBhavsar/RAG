# API App

This folder now hosts the FastAPI backend for document ingest and question answering.

Run it from the repo root with:

```powershell
python apps/api/src/server.py
```

If you want the development dependencies too, install them first:

```powershell
python -m pip install -e .[dev]
```

Endpoints:
- `GET /health`
- `POST /documents/upload` for PDF or text file uploads
- `POST /ingest` for JSON text or file paths
- `POST /chat` for question answering
- `POST /ask` as a compatibility alias for `/chat`
- `POST /chat-with-file` for one-shot file upload plus question answering

The server uses the PDF loader plugin for uploaded PDFs and the Ollama LLM provider for answers.

