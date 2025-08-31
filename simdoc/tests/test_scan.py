import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from simdoc.core.paths import SimsPaths
from simdoc.detectors.scan_mods import scan_mods


def test_scan_inventory_hash(tmp_path):
    docs = tmp_path / "The Sims 4"
    mods = docs / "Mods"
    mods.mkdir(parents=True)
    (mods / "a.package").write_text("data")
    (mods / "b.pyc").write_bytes(b"\x42\x0d\x0d\x0a1234")
    paths = SimsPaths.from_docs_root(docs)

    inv1, h1 = scan_mods(paths)
    inv2, h2 = scan_mods(paths)
    assert h1 == h2
    exts = {i["ext"] for i in inv1}
    assert ".package" in exts
    assert ".pyc" in exts
