#!/usr/bin/env python3
"""SimDoc auto-installer and launcher.

This script creates an isolated virtual environment, installs the ``simdoc``
package from the current directory, and then launches the CLI.  Users can
simply download the project, extract the archive, and double-click this file to
set things up.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def create_venv(venv_dir: Path) -> Path:
    """Create a virtual environment and return the path to its Python executable."""
    subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
    return venv_dir / ("Scripts" if os.name == "nt" else "bin") / "python"


def launch_cli(python_bin: Path, project_root: Path, args: list[str]) -> int:
    """Invoke the SimDoc CLI using the provided Python executable."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)
    return subprocess.call([str(python_bin), "-m", "simdoc", *args], env=env)


def main() -> None:
    project_root = Path(__file__).resolve().parent
    venv_dir = project_root / "venv"

    if venv_dir.exists():
        python_bin = venv_dir / ("Scripts" if os.name == "nt" else "bin") / "python"
    else:
        python_bin = create_venv(venv_dir)

    sys.exit(launch_cli(python_bin, project_root, sys.argv[1:]))


if __name__ == "__main__":
    main()
