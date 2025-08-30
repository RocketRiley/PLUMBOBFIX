"""Parse lastException.txt to identify failing mods."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

from simdoc.core.paths import SimsPaths

MOD_RE = re.compile(r"Mods[\\/].+?\.py")


def parse_last_exception(paths: SimsPaths) -> Dict[str, object]:
    try:
        text = paths.last_exception.read_text(errors="ignore")
    except FileNotFoundError:
        return {"present": False, "traceback_snippet": "", "mod_hits": []}
    lines = text.splitlines()
    snippet_lines: List[str] = []
    for idx in range(len(lines) - 1, -1, -1):
        if lines[idx].startswith("Traceback (most recent call last)"):
            snippet_lines = lines[idx: idx + 10]
            break
    snippet = "\n".join(snippet_lines)
    mod_hits = sorted(set(MOD_RE.findall(text)))
    return {
        "present": True,
        "traceback_snippet": snippet,
        "mod_hits": mod_hits,
    }
