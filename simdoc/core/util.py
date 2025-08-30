"""Utility functions for simdoc.

This module provides helpers for timestamps, hashing inventories,
file backups, and slugifying titles for report filenames.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import time
import re
from typing import Iterable


def timestamp() -> str:
    """Return a timestamp string suitable for file names."""
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


def slugify(title: str) -> str:
    """Create a filesystem-friendly slug from *title*."""
    slug = re.sub(r"[^a-zA-Z0-9-_]+", "_", title.strip().lower())
    return slug.strip("_")


def compute_inventory_hash(items: Iterable[str]) -> str:
    """Compute a stable hash for a sequence of inventory item strings."""
    sha = hashlib.sha256()
    for item in sorted(items):
        sha.update(item.encode("utf-8"))
    return sha.hexdigest()


def ensure_dir(path: Path) -> None:
    """Ensure *path* exists as a directory."""
    path.mkdir(parents=True, exist_ok=True)


def backup_file(src: Path, backup_dir: Path) -> Path:
    """Copy *src* into *backup_dir*, preserving relative name.

    Returns the path to the backed up file.
    """
    ensure_dir(backup_dir)
    dst = backup_dir / src.name
    shutil.copy2(src, dst)
    return dst
