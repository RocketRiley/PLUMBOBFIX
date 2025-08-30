"""State persistence for simdoc."""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Optional


STATE_FILE = "simdoc_state.json"


@dataclass
class SimDocState:
    """Persistent state stored between runs."""

    sims_docs_root: str
    last_seen_game_version: str = ""
    last_scan_time: float = 0.0
    last_inventory_hash: str = ""

    @classmethod
    def load(cls, path: Path) -> "SimDocState | None":
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        return cls(**data)

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=2))
