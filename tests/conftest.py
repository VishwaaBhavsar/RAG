"""Test configuration.

Purpose:
    Make the source trees importable during test runs without packaging the project yet.

Responsibilities:
    - Put each package `src/` directory on `sys.path`.
    - Keep the test imports consistent across local runs and CI.

Usage example:
    The pytest session imports `rag_framework.plugins` directly from the source tree.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for relative in (
    "packages/plugins/src",
    "packages/core/src",
    "packages/providers/src",
    "packages/shared/src",
):
    source_path = str(ROOT / relative)
    if source_path not in sys.path:
        sys.path.insert(0, source_path)

