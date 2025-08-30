import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from simdoc.core.state import SimDocState


def test_state_roundtrip(tmp_path):
    state = SimDocState(sims_docs_root="/path/to/docs", last_seen_game_version="1.0")
    file = tmp_path / "state.json"
    state.save(file)
    loaded = SimDocState.load(file)
    assert loaded == state
