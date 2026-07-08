"""PDF loader plugin configuration.

Purpose:
    Define the plugin-local configuration schema for chunk sizing and future loader knobs.

Responsibilities:
    - Keep plugin-specific settings out of the core engine.
    - Provide a typed place for configuration validation once the plugin is loaded.

Usage example:
    settings = PdfLoaderConfig(pdf_chunk_size=1024)
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PdfLoaderConfig(BaseModel):
    """Configuration for the PDF loader plugin."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    pdf_chunk_size: int = Field(default=1024, ge=1)
    enable_ocr: bool = Field(default=True)
    ocr_dpi: int = Field(default=200, ge=72, le=600)
