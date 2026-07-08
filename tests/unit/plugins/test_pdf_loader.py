"""Tests for the PDF loader plugin."""

from __future__ import annotations

from pathlib import Path

import pytest

from packages.plugins.plugins.pdf_loader.plugin import PdfLoader, PdfTextExtractionError


def _write_pdf_fixture(tmp_path: Path) -> Path:
    pdf_path = tmp_path / "sample.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n% test fixture\n")
    return pdf_path


def test_pdf_loader_prefers_pdftotext_over_ocr(monkeypatch, tmp_path) -> None:
    pdf_path = _write_pdf_fixture(tmp_path)
    loader = PdfLoader()

    monkeypatch.setattr(loader, "_extract_from_content_streams", lambda raw_bytes: [])
    monkeypatch.setattr(loader, "_extract_with_pdftotext", lambda path: ["text from pdftotext"])
    monkeypatch.setattr(loader, "_extract_with_ocr", lambda path: ["ocr text"])

    documents = loader.load(pdf_path)

    assert len(documents) == 1
    assert documents[0].content == "text from pdftotext"
    assert documents[0].metadata["chunk_index"] == 0


def test_pdf_loader_uses_ocr_when_text_extraction_fails(monkeypatch, tmp_path) -> None:
    pdf_path = _write_pdf_fixture(tmp_path)
    loader = PdfLoader()

    monkeypatch.setattr(loader, "_extract_from_content_streams", lambda raw_bytes: [])
    monkeypatch.setattr(loader, "_extract_with_pdftotext", lambda path: [])
    monkeypatch.setattr(loader, "_extract_with_ocr", lambda path: ["scanned document text"])

    documents = loader.load(pdf_path)

    assert len(documents) == 1
    assert documents[0].content == "scanned document text"


def test_pdf_loader_raises_clear_error_when_no_text_is_found(monkeypatch, tmp_path) -> None:
    pdf_path = _write_pdf_fixture(tmp_path)
    loader = PdfLoader()

    monkeypatch.setattr(loader, "_extract_from_content_streams", lambda raw_bytes: [])
    monkeypatch.setattr(loader, "_extract_with_pdftotext", lambda path: [])
    monkeypatch.setattr(loader, "_extract_with_ocr", lambda path: [])

    with pytest.raises(PdfTextExtractionError, match="No extractable text found"):
        loader.load(pdf_path)
