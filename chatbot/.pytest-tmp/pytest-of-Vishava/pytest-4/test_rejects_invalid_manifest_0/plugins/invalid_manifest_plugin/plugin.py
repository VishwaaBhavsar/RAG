"""Broken fixture plugin.

This file should never be imported because the manifest fails validation first.
"""

def load() -> dict[str, object]:
    return {"plugin": "broken-plugin"}

