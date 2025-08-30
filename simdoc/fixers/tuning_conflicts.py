"""Stub for tuning conflict detection."""
from __future__ import annotations

from pathlib import Path
from typing import List

from simdoc.core.paths import SimsPaths


def detect_conflicts(paths: SimsPaths, dry_run: bool, backup_dir: Path) -> List[str]:
    """Enumerate .package files and report placeholder analysis."""
    packages = list(paths.mods.rglob("*.package"))
    return [
        f"Found {len(packages)} package files. TODO: analyze tuning IDs for conflicts.",
        "Planned approach: parse DBPF headers and identify duplicate instance IDs.",
    ]
