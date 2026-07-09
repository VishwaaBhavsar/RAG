from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from chatbot.api.schemas import ChatRequest, ChatResponse, HealthResponse
from chatbot.config.domain_config import DOMAIN_NAME
from chatbot.config.settings import get_settings
from chatbot.core.chatbot import Chatbot
from chatbot.core.llm.factory import get_llm_provider
from chatbot.utils.logger import configure_logging, get_logger

settings = get_settings()
configure_logging(settings.LOG_LEVEL)
logger = get_logger(__name__)

app = FastAPI(title="Domain-Locked Chatbot", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

_request_history: dict[str, deque[float]] = defaultdict(deque)


def _client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _rate_limited(request: Request) -> bool:
    now = time.time()
    window_start = now - 60.0
    ip = _client_ip(request)
    history = _request_history[ip]
    while history and history[0] < window_start:
        history.popleft()
    if len(history) >= settings.RATE_LIMIT_PER_MINUTE:
        return True
    history.append(now)
    return False


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.on_event("startup")
async def startup_chatbot() -> None:
    app.state.chatbot = Chatbot(provider=get_llm_provider())


@app.get("/health", response_model=HealthResponse)
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "domain": DOMAIN_NAME,
        "provider": settings.LLM_PROVIDER,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: Request, payload: ChatRequest) -> dict[str, Any]:
    if _rate_limited(request):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    chatbot = getattr(request.app.state, "chatbot", None)
    if chatbot is None:
        chatbot = Chatbot(provider=get_llm_provider())
        request.app.state.chatbot = chatbot
    result = chatbot.chat(payload.message)
    return {"response": result.response, "on_topic": result.on_topic}