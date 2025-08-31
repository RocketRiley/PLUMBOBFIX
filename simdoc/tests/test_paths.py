import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from simdoc.core.paths import SimsPaths


def test_validate_paths(tmp_path):
    docs = tmp_path / "The Sims 4"
    mods = docs / "Mods"
    mods.mkdir(parents=True)
    paths = SimsPaths.from_docs_root(docs)
    ok, errors = paths.validate()
    assert ok
    assert errors == []


def test_validate_missing_mods(tmp_path):
    docs = tmp_path / "The Sims 4"
    docs.mkdir()
    paths = SimsPaths.from_docs_root(docs)
    ok, errors = paths.validate()
    assert not ok
    assert errors
