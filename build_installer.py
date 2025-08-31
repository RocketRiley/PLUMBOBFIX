#!/usr/bin/env python3
"""Build a Windows installer executable using PyInstaller.

Running this script on Windows will produce ``simdoc_installer.exe`` in the
``dist`` directory. The resulting executable wraps ``installer.py`` so users can
simply double-click it to set up and launch ``simdoc``.
"""
from __future__ import annotations

import argparse
from pathlib import Path

def build(name: str) -> None:
    try:
        from PyInstaller.__main__ import run
    except Exception as exc:  # pragma: no cover - import-time failure
        raise SystemExit("PyInstaller is required to build the executable") from exc

    script = Path(__file__).with_name("installer.py")
    run([str(script), "--onefile", "--name", name])

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build simdoc installer executable")
    parser.add_argument("--name", default="simdoc_installer", help="Output executable name")
    args = parser.parse_args(argv)
    build(args.name)

if __name__ == "__main__":  # pragma: no cover
    main()
