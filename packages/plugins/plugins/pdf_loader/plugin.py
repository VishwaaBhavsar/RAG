"""PDF loader plugin.

Purpose:
    Provide the framework's first concrete document loader as a self-contained plugin.

Responsibilities:
    - Parse text out of PDFs using multiple strategies.
    - Fall back to external text extraction tools when available.
    - Fall back to OCR for scanned PDFs when the environment supports it.
    - Register the loader factory into the core registry.

Usage example:
    register = load()
    register(registry)
"""

from __future__ import annotations

import base64
import importlib.util
import re
import shutil
import subprocess
import tempfile
import zlib
from io import BytesIO
from pathlib import Path
from typing import Callable, Iterable

from rag_framework.core import BaseLoader, Document, Registry

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover - dependency optional in some environments
    PdfReader = None

_STREAM_PATTERN = re.compile(
    rb"<<(?P<dictionary>.*?)>>\s*stream\r?\n(?P<data>.*?)\r?\nendstream",
    re.DOTALL,
)
_FILTER_PATTERN = re.compile(rb"/([A-Za-z0-9]+Decode)")
_TEXT_OPERATOR_PATTERN = re.compile(
    r'(\[(?:.|\n)*?\]|\((?:\\.|[^()])*\)|<[^>]+>)\s*(?:Tj|TJ|\'|")',
    re.DOTALL,
)
_ARRAY_TOKEN_PATTERN = re.compile(r"\((?:\\.|[^()])*\)|<[^>]+>")


def _load_pdf_loader_config_class() -> type[object]:
    config_path = Path(__file__).with_name("config.py")
    spec = importlib.util.spec_from_file_location("pdf_loader_config", config_path)
    if spec is None or spec.loader is None:
        return type("PdfLoaderConfigFallback", (), {})

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    config_cls = getattr(module, "PdfLoaderConfig", None)
    if config_cls is None:
        return type("PdfLoaderConfigFallback", (), {})
    return config_cls


PdfLoaderConfig = _load_pdf_loader_config_class()


class PdfTextExtractionError(ValueError):
    """Raised when a PDF cannot be converted into usable text."""


class PdfLoader(BaseLoader):
    """Extract text chunks from a PDF file."""

    def __init__(self, config: object | None = None) -> None:
        self._config = config if config is not None else PdfLoaderConfig()

    def load(self, source: str | Path) -> list[Document]:
        path = Path(source)
        raw_bytes = path.read_bytes()
        chunks = self._extract_text_candidates(path, raw_bytes)
        documents = self._build_documents(path, chunks)
        if documents:
            return documents

        raise PdfTextExtractionError(self._failure_message(path))

    def _extract_text_candidates(self, path: Path, raw_bytes: bytes) -> list[str]:
        strategies = (
            self._extract_with_pypdf(raw_bytes),
            self._extract_from_content_streams(raw_bytes),
            self._extract_with_pdftotext(path),
            self._extract_with_ocr(path),
        )
        for candidates in strategies:
            normalized = self._normalize_chunks(candidates)
            if normalized:
                return normalized
        return []

    def _extract_from_content_streams(self, raw_bytes: bytes) -> list[str]:
        chunks: list[str] = []
        for dictionary, stream_data in self._iter_pdf_streams(raw_bytes):
            decoded_stream = self._decode_stream(dictionary, stream_data)
            if not decoded_stream:
                continue
            chunks.extend(self._extract_text_from_content_stream(decoded_stream))
        return chunks
    def _extract_with_pypdf(self, raw_bytes: bytes) -> list[str]:
        if PdfReader is None:
            return []

        try:
            reader = PdfReader(BytesIO(raw_bytes))
        except Exception:
            return []

        pages: list[str] = []
        for page in reader.pages:
            try:
                text = page.extract_text() or ""
            except Exception:
                continue
            if text.strip():
                pages.append(text)
        return pages

    def _iter_pdf_streams(self, raw_bytes: bytes) -> Iterable[tuple[bytes, bytes]]:
        for match in _STREAM_PATTERN.finditer(raw_bytes):
            dictionary = match.group("dictionary")
            stream_data = match.group("data").strip(b"\r\n")
            yield dictionary, stream_data

    def _decode_stream(self, dictionary: bytes, stream_data: bytes) -> str:
        filters = [filter_name.decode("ascii", errors="ignore") for filter_name in _FILTER_PATTERN.findall(dictionary)]
        decoded_bytes = stream_data
        for filter_name in filters:
            if filter_name == "ASCII85Decode":
                try:
                    decoded_bytes = base64.a85decode(decoded_bytes, adobe=True)
                except (ValueError, TypeError):
                    return ""
            elif filter_name == "FlateDecode":
                for wbits in (zlib.MAX_WBITS, -zlib.MAX_WBITS):
                    try:
                        decoded_bytes = zlib.decompress(decoded_bytes, wbits)
                        break
                    except zlib.error:
                        continue
                else:
                    return ""

        decoded = decoded_bytes.decode("latin-1", errors="ignore")
        return decoded if self._looks_like_text(decoded) else ""

    def _extract_text_from_content_stream(self, content: str) -> list[str]:
        chunks: list[str] = []
        for match in _TEXT_OPERATOR_PATTERN.finditer(content):
            chunks.extend(text for text in self._decode_pdf_token(match.group(1)) if self._looks_like_text(text))
        return chunks

    def _decode_pdf_token(self, token: str) -> list[str]:
        if token.startswith("["):
            return self._decode_pdf_array(token)
        if token.startswith("<"):
            return [self._decode_pdf_hex_string(token[1:-1])]
        return [self._decode_pdf_literal_string(token)]

    def _decode_pdf_array(self, token: str) -> list[str]:
        chunks: list[str] = []
        for match in _ARRAY_TOKEN_PATTERN.finditer(token):
            item = match.group(0)
            if item.startswith("("):
                chunks.append(self._decode_pdf_literal_string(item))
            elif item.startswith("<"):
                chunks.append(self._decode_pdf_hex_string(item[1:-1]))
        return chunks

    def _decode_pdf_literal_string(self, token: str) -> str:
        text = token[1:-1]
        result: list[str] = []
        index = 0
        while index < len(text):
            char = text[index]
            if char != "\\":
                result.append(char)
                index += 1
                continue

            index += 1
            if index >= len(text):
                break

            escaped = text[index]
            if escaped == "n":
                result.append("\n")
                index += 1
                continue
            if escaped == "r":
                result.append("\r")
                index += 1
                continue
            if escaped == "t":
                result.append("\t")
                index += 1
                continue
            if escaped == "b":
                result.append("\b")
                index += 1
                continue
            if escaped == "f":
                result.append("\f")
                index += 1
                continue
            if escaped in {"\\", "(", ")"}:
                result.append(escaped)
                index += 1
                continue
            if escaped in {"\r", "\n"}:
                index += 1
                if escaped == "\r" and index < len(text) and text[index] == "\n":
                    index += 1
                continue

            octal_digits = [escaped]
            lookahead = index + 1
            while lookahead < len(text) and len(octal_digits) < 3 and text[lookahead] in "01234567":
                octal_digits.append(text[lookahead])
                lookahead += 1
            if all(char in "01234567" for char in octal_digits):
                result.append(chr(int("".join(octal_digits), 8)))
                index = lookahead
                continue

            result.append(escaped)
            index += 1
        return "".join(result)

    def _decode_pdf_hex_string(self, token: str) -> str:
        cleaned = re.sub(r"\s+", "", token)
        if not cleaned:
            return ""
        if len(cleaned) % 2 == 1:
            cleaned += "0"

        try:
            raw = bytes.fromhex(cleaned)
        except ValueError:
            return ""

        if raw.startswith(b"\xfe\xff"):
            return raw[2:].decode("utf-16-be", errors="ignore")
        if raw.startswith(b"\xff\xfe"):
            return raw[2:].decode("utf-16-le", errors="ignore")
        if raw.count(b"\x00") >= max(1, len(raw) // 4):
            try:
                return raw.decode("utf-16-be", errors="ignore")
            except UnicodeError:
                pass
        return raw.decode("latin-1", errors="ignore")

    def _extract_with_pdftotext(self, path: Path) -> list[str]:
        executable = shutil.which("pdftotext")
        if executable is None:
            return []

        try:
            result = subprocess.run(
                [executable, "-layout", str(path), "-"],
                check=True,
                capture_output=True,
                text=True,
            )
        except (OSError, subprocess.CalledProcessError):
            return []

        output = result.stdout.strip()
        if not output:
            return []

        return [page.strip() for page in output.split("\f") if page.strip()]

    def _extract_with_ocr(self, path: Path) -> list[str]:
        if not getattr(self._config, "enable_ocr", True):
            return []

        pdftoppm = shutil.which("pdftoppm")
        tesseract = shutil.which("tesseract")
        if pdftoppm is None or tesseract is None:
            return []

        dpi = int(getattr(self._config, "ocr_dpi", 200))
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                prefix = Path(temp_dir) / "page"
                subprocess.run(
                    [pdftoppm, "-png", "-r", str(dpi), str(path), str(prefix)],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                image_paths = sorted(Path(temp_dir).glob("page-*.png"))
                pages: list[str] = []
                for image_path in image_paths:
                    try:
                        result = subprocess.run(
                            [tesseract, str(image_path), "stdout", "--psm", "6"],
                            check=True,
                            capture_output=True,
                            text=True,
                        )
                    except (OSError, subprocess.CalledProcessError):
                        continue

                    page_text = result.stdout.strip()
                    if page_text:
                        pages.append(page_text)
                return pages
        except (OSError, subprocess.CalledProcessError):
            return []

    def _normalize_chunks(self, chunks: Iterable[str]) -> list[str]:
        normalized: list[str] = []
        for chunk in chunks:
            cleaned = self._normalize_text(chunk)
            if cleaned:
                normalized.append(cleaned)
        return normalized

    def _normalize_text(self, text: str) -> str:
        return "\n".join(line.rstrip() for line in text.splitlines()).strip()

    def _looks_like_text(self, text: str) -> bool:
        cleaned = text.strip()
        if len(cleaned) < 4:
            return False

        printable = sum(1 for char in cleaned if char.isprintable())
        letters = sum(1 for char in cleaned if char.isalpha())
        spaces = sum(1 for char in cleaned if char.isspace())
        return printable / len(cleaned) >= 0.85 and (letters + spaces) / len(cleaned) >= 0.5

    def _build_documents(self, path: Path, chunks: Iterable[str]) -> list[Document]:
        documents: list[Document] = []
        for index, chunk in enumerate(self._normalize_chunks(chunks)):
            documents.append(
                Document(
                    content=chunk,
                    metadata={"source": str(path), "chunk_index": index},
                )
            )
        return documents

    def _failure_message(self, path: Path) -> str:
        return (
            f"No extractable text found in '{path.name}'. "
            "Try a text-based PDF, install pdftotext/Poppler for richer extraction, "
            "or install Poppler and Tesseract for OCR on scanned documents."
        )


def load() -> Callable[[Registry], None]:
    """Return a registry registration hook for the PDF loader plugin."""

    def register(registry: Registry) -> None:
        registry.register("loader", "pdf", lambda: PdfLoader())

    return register



