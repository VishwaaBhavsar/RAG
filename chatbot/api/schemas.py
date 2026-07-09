from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    response: str
    on_topic: bool


class HealthResponse(BaseModel):
    status: str
    domain: str
    provider: str

