"""Reporting helpers for simdoc."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List

from .util import timestamp, slugify, ensure_dir

REPORTS_DIR = Path("reports")


def write_report(title: str, sections: Dict[str, Iterable[str]]) -> Path:
    """Write a Markdown report with *title* and section bullet lists."""
    ensure_dir(REPORTS_DIR)
    ts = timestamp()
    filename = REPORTS_DIR / f"{ts}_{slugify(title)}.md"
    lines: List[str] = [f"# {title}\n"]
    for section, items in sections.items():
        lines.append(f"## {section}\n")
        for item in items:
            lines.append(f"- {item}\n")
        lines.append("\n")
    filename.write_text("".join(lines))
    return filename
