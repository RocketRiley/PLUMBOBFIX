"""Python compatibility fixer for .pyc files."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from simdoc.core.paths import SimsPaths
from simdoc.core.util import backup_file

MAGIC_TO_VERSION: Dict[bytes, str] = {
    b"\x42\x0d\x0d\x0a": "3.7",
    b"\x50\x0d\x0d\x0a": "3.8",
    b"\x60\x0d\x0d\x0a": "3.9",
    b"\x61\x0d\x0d\x0a": "3.10",
}

ALLOWED_VERSIONS = {"3.7", "3.8"}


def fix_py_compat(paths: SimsPaths, dry_run: bool, backup_dir: Path) -> List[str]:
    """Delete .pyc files with incompatible magic numbers."""
    actions: List[str] = []
    for pyc in paths.mods.rglob("*.pyc"):
        try:
            with pyc.open("rb") as fh:
                magic = fh.read(4)
        except OSError as exc:
            actions.append(f"WARN could not read {pyc}: {exc}")
            continue
        version = MAGIC_TO_VERSION.get(magic, "unknown")
        if version in ALLOWED_VERSIONS:
            continue
        if dry_run:
            actions.append(f"Would remove incompatible {pyc} (py{version})")
        else:
            backup_file(pyc, backup_dir)
            try:
                pyc.unlink()
                actions.append(f"Removed incompatible {pyc} (py{version})")
            except Exception as exc:
                actions.append(f"WARN failed to delete {pyc}: {exc}")
    return actions
