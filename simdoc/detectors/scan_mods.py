"""Inventory mods and compute a stable hash."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

from simdoc.core.paths import SimsPaths
from simdoc.core.util import compute_inventory_hash

EXTS = {".package", ".ts4script", ".zip", ".py", ".pyc"}


def scan_mods(paths: SimsPaths) -> Tuple[List[Dict[str, object]], str]:
    """Return (inventory, inventory_hash)."""
    inventory: List[Dict[str, object]] = []
    for file in paths.mods.rglob("*"):
        if not file.is_file():
            continue
        ext = file.suffix.lower()
        if ext not in EXTS:
            continue
        stat = file.stat()
        rel = str(file.relative_to(paths.mods))
        item = {
            "path": rel,
            "size": stat.st_size,
            "mtime": int(stat.st_mtime),
            "ext": ext,
        }
        inventory.append(item)
    items_for_hash = [f"{i['path']}|{i['size']}|{i['mtime']}" for i in inventory]
    inv_hash = compute_inventory_hash(items_for_hash)
    return inventory, inv_hash
