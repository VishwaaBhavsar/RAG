"""Repository bootstrap package for the rag_framework namespace.

This package keeps editable installs simple by extending the import path to the
actual source trees that live under packages/core/src, packages/plugins/src,
and packages/providers/src.
"""

from __future__ import annotations

from pathlib import Path
from pkgutil import extend_path
import sys

_repo_root = Path(__file__).resolve().parent.parent
for relative in ("packages/core/src", "packages/plugins/src", "packages/providers/src"):
    source_path = str((_repo_root / relative).resolve())
    if source_path not in sys.path:
        sys.path.insert(0, source_path)

__path__ = extend_path(__path__, __name__)