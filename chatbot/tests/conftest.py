"""Test configuration for the isolated chatbot package."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHATBOT_TMP = ROOT / "chatbot" / ".pytest-tmp"
CHATBOT_TMP.mkdir(exist_ok=True)

os.environ["TMP"] = str(CHATBOT_TMP)
os.environ["TEMP"] = str(CHATBOT_TMP)
os.environ["TMPDIR"] = str(CHATBOT_TMP)
tempfile.tempdir = str(CHATBOT_TMP)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))