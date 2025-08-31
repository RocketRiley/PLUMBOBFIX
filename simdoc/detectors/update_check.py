"""Read and parse GameVersion.txt."""
from __future__ import annotations

import re
from pathlib import Path

from simdoc.core.paths import SimsPaths

VERSION_RE = re.compile(r"(\d+\.\d+\.\d+\.\d+)")


def read_game_version(paths: SimsPaths) -> str:
    """Return the game version string or empty if not found."""
    try:
        text = paths.game_version_txt.read_text()
    except FileNotFoundError:
        return ""
    m = VERSION_RE.search(text)
    return m.group(1) if m else ""
