"""Native cache clearing and other basic fixes."""
from __future__ import annotations

from pathlib import Path
from typing import List

from simdoc.core.paths import SimsPaths
from simdoc.core.util import backup_file


def clear_caches(paths: SimsPaths, dry_run: bool, backup_dir: Path) -> List[str]:
    """Clear common caches, returning a list of actions."""
    actions: List[str] = []
    cache = paths.localthumbcache
    if cache.exists():
        if dry_run:
            actions.append(f"Would delete {cache}")
        else:
            backup_file(cache, backup_dir)
            try:
                cache.unlink()
                actions.append(f"Deleted {cache}")
            except Exception as exc:
                actions.append(f"WARN failed to delete {cache}: {exc}")
    else:
        actions.append("localthumbcache.package not found")
    # TODO: handle Options.ini sanity checks and other caches.
    return actions
