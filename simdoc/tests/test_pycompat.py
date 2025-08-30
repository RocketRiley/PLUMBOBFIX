import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from simdoc.core.paths import SimsPaths
from simdoc.fixers.py_compat import fix_py_compat


def make_pyc(path: Path, magic: bytes) -> None:
    path.write_bytes(magic + b"\x00\x00\x00\x00")


def test_pycompat_dry_run_and_apply(tmp_path):
    docs = tmp_path / "The Sims 4"
    mods = docs / "Mods"
    mods.mkdir(parents=True)
    good = mods / "good.pyc"
    bad = mods / "bad.pyc"
    make_pyc(good, b"\x42\x0d\x0d\x0a")  # 3.7
    make_pyc(bad, b"\x60\x0d\x0d\x0a")   # 3.9
    paths = SimsPaths.from_docs_root(docs)
    backup = tmp_path / "backup"

    actions = fix_py_compat(paths, True, backup)
    assert bad.exists()
    assert any("Would remove" in a for a in actions)

    actions = fix_py_compat(paths, False, backup)
    assert not bad.exists()
    assert (backup / "bad.pyc").exists()
    assert all("Would" not in a for a in actions)
