"""Standalone retrieval evaluation harness.

This measures retrieval quality against a fixed corpus and fixed eval cases.
It compares reranker=none against reranker=cross-encoder using the real
sentence-transformers embedding provider and a real Ollama LLM provider
selected through the app's normal environment-based wiring.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _ensure_import_paths() -> None:
    root = _repo_root()
    for relative in (
        "apps/api/src",
        "packages/core/src",
        "packages/providers/src",
        "packages/plugins/src",
        "packages/shared/src",
        ".",
    ):
        resolved = str(root / relative)
        if resolved not in sys.path:
            sys.path.insert(0, resolved)


_ensure_import_paths()

# Keep module import safe and deterministic even before the real eval runs.
os.environ.setdefault("RAG_FRAMEWORK_LLM__PROVIDER", "fake")
os.environ.setdefault("RAG_FRAMEWORK_EMBEDDINGS__PROVIDER", "fake")
os.environ.setdefault("RAG_FRAMEWORK_VECTORSTORE__PROVIDER", "in-memory")
os.environ.setdefault("RAG_FRAMEWORK_RERANKER__PROVIDER", "none")

from apps.api.src.server import create_app
from rag_framework.core.contracts import Document


@dataclass(frozen=True, slots=True)
class EvalCase:
    question: str
    expected_source: str
    expected_content_contains: str | None = None


@dataclass(frozen=True, slots=True)
class EvalResult:
    case: EvalCase
    passed: bool
    retrieved_source: str
    retrieved_content: str


@contextmanager
def _temporary_env(updates: dict[str, str | None]) -> Iterator[None]:
    previous = {key: os.environ.get(key) for key in updates}
    try:
        for key, value in updates.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _load_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON list")
    return payload


def _load_corpus(path: Path) -> list[Document]:
    documents: list[Document] = []
    for index, item in enumerate(_load_json(path)):
        if not isinstance(item, dict):
            raise ValueError(f"corpus item {index} in {path} must be an object")
        try:
            content = str(item["content"]).strip()
            source = str(item["source"]).strip()
        except KeyError as exc:
            raise ValueError(f"corpus item {index} in {path} is missing {exc.args[0]!r}") from exc
        if not content:
            raise ValueError(f"corpus item {index} in {path} has empty content")
        if not source:
            raise ValueError(f"corpus item {index} in {path} has empty source")
        metadata = {key: value for key, value in item.items() if key != "content"}
        documents.append(Document(content=content, metadata=metadata))
    return documents


def _load_cases(path: Path) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for index, item in enumerate(_load_json(path)):
        if not isinstance(item, dict):
            raise ValueError(f"case item {index} in {path} must be an object")
        try:
            question = str(item["question"]).strip()
            expected_source = str(item["expected_source"]).strip()
        except KeyError as exc:
            raise ValueError(f"case item {index} in {path} is missing {exc.args[0]!r}") from exc
        if not question:
            raise ValueError(f"case item {index} in {path} has empty question")
        if not expected_source:
            raise ValueError(f"case item {index} in {path} has empty expected_source")
        expected_content_contains = item.get("expected_content_contains")
        cases.append(
            EvalCase(
                question=question,
                expected_source=expected_source,
                expected_content_contains=str(expected_content_contains).strip() if expected_content_contains else None,
            )
        )
    return cases


def _build_app(*, vector_store: str, reranker: str, chroma_path: str | None = None):
    env_updates: dict[str, str | None] = {
        "RAG_FRAMEWORK_LLM__PROVIDER": "ollama",
        "RAG_FRAMEWORK_EMBEDDINGS__PROVIDER": "sentence-transformers",
        "RAG_FRAMEWORK_VECTORSTORE__PROVIDER": vector_store,
        "RAG_FRAMEWORK_RERANKER__PROVIDER": reranker,
    }
    if chroma_path is not None:
        env_updates["RAG_FRAMEWORK_CHROMA__PATH"] = chroma_path
    with _temporary_env(env_updates):
        return create_app()


def _search_documents(app, question: str, top_k: int = 1) -> list[Document]:
    backend = app.state.backend
    return backend.knowledge_base.search(question, top_k=top_k)


def _run_eval(corpus: list[Document], cases: list[EvalCase], *, vector_store: str, reranker: str) -> list[EvalResult]:
    if vector_store == "chroma":
        with tempfile.TemporaryDirectory(prefix=f"rag-eval-{reranker}-") as chroma_dir:
            app = _build_app(vector_store=vector_store, reranker=reranker, chroma_path=chroma_dir)
            backend = app.state.backend
            backend.knowledge_base.add_documents(corpus)
            return [_evaluate_case(app, case) for case in cases]

    app = _build_app(vector_store=vector_store, reranker=reranker)
    backend = app.state.backend
    backend.knowledge_base.add_documents(corpus)
    return [_evaluate_case(app, case) for case in cases]


def _evaluate_case(app, case: EvalCase) -> EvalResult:
    retrieved_documents = _search_documents(app, case.question, top_k=1)
    if retrieved_documents:
        top_document = retrieved_documents[0]
        retrieved_source = str(top_document.metadata.get("source", ""))
        retrieved_content = top_document.content
    else:
        retrieved_source = ""
        retrieved_content = ""
    passed = bool(retrieved_documents) and retrieved_source == case.expected_source
    if passed and case.expected_content_contains:
        passed = case.expected_content_contains.lower() in retrieved_content.lower()
    return EvalResult(
        case=case,
        passed=passed,
        retrieved_source=retrieved_source,
        retrieved_content=retrieved_content,
    )


def _truncate(text: str, limit: int = 110) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _print_fixture_preview(corpus: list[Document], cases: list[EvalCase]) -> None:
    print("Eval corpus")
    for document in corpus:
        print(f"- {document.metadata.get('source')}: {_truncate(document.content)}")
    print()
    print("Eval cases")
    for case in cases:
        suffix = f" [needs: {case.expected_content_contains}]" if case.expected_content_contains else ""
        print(f"- {case.question} -> {case.expected_source}{suffix}")
    print()


def _print_run_summary(label: str, results: list[EvalResult]) -> tuple[int, int]:
    total = len(results)
    passed = sum(1 for result in results if result.passed)
    pass_rate = (passed / total * 100.0) if total else 0.0

    print(f"{label}: {passed}/{total} passed ({pass_rate:.1f}%)")
    failures = [result for result in results if not result.passed]
    if failures:
        print("  Failures:")
        for result in failures:
            expected = result.case.expected_source
            retrieved = result.retrieved_source or "<no documents>"
            details = f" expected={expected} retrieved={retrieved}"
            if result.case.expected_content_contains:
                details += f" required_content={result.case.expected_content_contains!r}"
            if result.retrieved_content:
                details += f" top_content={_truncate(result.retrieved_content)}"
            print(f"  - {result.case.question}{details}")
    else:
        print("  Failures: none")
    print()
    return passed, total


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate retrieval quality on a fixed corpus.")
    parser.add_argument(
        "--vector-store",
        choices=("in-memory", "chroma"),
        default=os.getenv("RAG_FRAMEWORK_EVAL_VECTORSTORE", "in-memory"),
        help="Vector store provider to use for the eval runs.",
    )
    args = parser.parse_args()

    root = _repo_root()
    corpus_path = root / "tests" / "fixtures" / "eval" / "corpus.json"
    cases_path = root / "tests" / "fixtures" / "eval" / "retrieval_cases.json"

    corpus = _load_corpus(corpus_path)
    cases = _load_cases(cases_path)

    _print_fixture_preview(corpus, cases)

    try:
        from sentence_transformers import CrossEncoder  # noqa: F401
        from sentence_transformers import SentenceTransformer  # noqa: F401
    except ImportError as exc:
        print("sentence-transformers is required for this eval.")
        print(str(exc))
        return 1

    print(f"Vector store: {args.vector_store}")
    print("Embedding provider: sentence-transformers")
    print("LLM provider: ollama")
    print()

    results_none = _run_eval(corpus, cases, vector_store=args.vector_store, reranker="none")
    results_cross = _run_eval(corpus, cases, vector_store=args.vector_store, reranker="cross-encoder")

    print("Results")
    print("--------")
    none_passed, none_total = _print_run_summary("reranker=none", results_none)
    cross_passed, cross_total = _print_run_summary("reranker=cross-encoder", results_cross)

    none_rate = none_passed / none_total * 100.0 if none_total else 0.0
    cross_rate = cross_passed / cross_total * 100.0 if cross_total else 0.0

    print("Side by side")
    print("------------")
    print(f"reranker=none           {none_passed:>2}/{none_total:<2}  {none_rate:5.1f}%")
    print(f"reranker=cross-encoder  {cross_passed:>2}/{cross_total:<2}  {cross_rate:5.1f}%")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
