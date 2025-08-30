"""Path utilities and validation for The Sims 4 documents folder."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, List


@dataclass
class SimsPaths:
    """Collection of important paths within The Sims 4 documents folder."""

    docs_root: Path
    mods: Path
    localthumbcache: Path
    last_exception: Path
    game_version_txt: Path

    @classmethod
    def from_docs_root(cls, docs_root: Path) -> "SimsPaths":
        docs_root = Path(docs_root).expanduser().resolve()
        return cls(
            docs_root=docs_root,
            mods=docs_root / "Mods",
            localthumbcache=docs_root / "localthumbcache.package",
            last_exception=docs_root / "lastException.txt",
            game_version_txt=docs_root / "GameVersion.txt",
        )

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate the expected folder structure.

        Returns a tuple of (is_valid, errors).
        """
        errors: List[str] = []
        if not self.docs_root.exists():
            errors.append(f"Docs root not found: {self.docs_root}")
        if not self.mods.exists():
            errors.append(f"Mods folder not found: {self.mods}")
        return (not errors, errors)
