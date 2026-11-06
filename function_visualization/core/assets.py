"""Loading of static template assets (HTML / CSS / JS) bundled with the package."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


@lru_cache(maxsize=None)
def read_template(relative_path: str) -> str:
    """Read a UTF-8 text file located under ``core/templates``.

    Raises ``FileNotFoundError`` with a clear message when it is missing.
    """
    path = TEMPLATES_DIR / relative_path
    if not path.is_file():
        raise FileNotFoundError(f"Missing template asset: {path}")
    return path.read_text(encoding="utf-8")
