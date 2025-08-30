"""Command line interface for simdoc."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Dict, Iterable

from .core.paths import SimsPaths
from .core.state import SimDocState, STATE_FILE
from .core.reporting import write_report
from .core.util import timestamp, ensure_dir
from .detectors.update_check import read_game_version
from .detectors.scan_mods import scan_mods
from .parsers.last_exception import parse_last_exception
from .fixers.native import clear_caches
from .fixers.py_compat import fix_py_compat
from .fixers.tuning_conflicts import detect_conflicts


def load_state(state_path: Path) -> SimDocState:
    state = SimDocState.load(state_path)
    if state is None:
        print("State file not found. Run 'simdoc init' first.")
        sys.exit(1)
    return state


def cmd_init(args: argparse.Namespace) -> None:
    paths = SimsPaths.from_docs_root(Path(args.sims_folder))
    ok, errors = paths.validate()
    if not ok:
        for e in errors:
            print(e)
        sys.exit(1)
    version = read_game_version(paths)
    state = SimDocState(sims_docs_root=str(paths.docs_root), last_seen_game_version=version)
    state.save(Path(args.state_file))
    print(f"Initialized simdoc at {paths.docs_root}")


def cmd_scan(args: argparse.Namespace) -> None:
    state = load_state(Path(args.state_file))
    paths = SimsPaths.from_docs_root(state.sims_docs_root)
    current_version = read_game_version(paths)
    inventory, inv_hash = scan_mods(paths)
    le_info = parse_last_exception(paths)

    sections: Dict[str, Iterable[str]] = {
        "Game Version": [
            f"Previous: {state.last_seen_game_version}",
            f"Current: {current_version}",
        ],
        "Inventory": [
            f"Files: {len(inventory)}",
            f"Inventory hash: {inv_hash}",
        ],
    }
    if le_info["present"]:
        sections["Last Exception"] = [le_info["traceback_snippet"]] + le_info["mod_hits"]

    report = write_report("Scan Summary", sections)
    print(f"Scan complete. Report written to {report}")

    state.last_seen_game_version = current_version
    state.last_inventory_hash = inv_hash
    state.last_scan_time = time.time()
    state.save(Path(args.state_file))


def cmd_fix(args: argparse.Namespace) -> None:
    state = load_state(Path(args.state_file))
    paths = SimsPaths.from_docs_root(state.sims_docs_root)
    dry_run = not args.apply
    backup_dir = Path("backups") / timestamp()
    sections: Dict[str, Iterable[str]] = {}
    ensure_dir(backup_dir)

    if args.native:
        sections["Native"] = clear_caches(paths, dry_run, backup_dir)
    if args.py_compat:
        sections["Python compatibility"] = fix_py_compat(paths, dry_run, backup_dir)
    if args.conflicts:
        sections["Tuning conflicts"] = detect_conflicts(paths, dry_run, backup_dir)

    report = write_report("Fix Run", sections)
    print(f"Fix complete. Report written to {report}")
    if dry_run:
        print("Dry run complete; no files modified.")
    else:
        print(f"Backups saved in {backup_dir}")


def cmd_doctor(args: argparse.Namespace) -> None:
    args.native = True
    args.py_compat = True
    cmd_fix(args)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="simdoc", description="The Sims 4 mod doctor")
    parser.add_argument("--state-file", default=STATE_FILE, help="Path to state file")
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="Initialize with Sims 4 documents folder")
    p_init.add_argument("--sims-folder", required=True, help="Path to 'The Sims 4' documents folder")
    p_init.set_defaults(func=cmd_init)

    p_scan = sub.add_parser("scan", help="Scan mods and produce report")
    p_scan.set_defaults(func=cmd_scan)

    p_fix = sub.add_parser("fix", help="Run fixers")
    p_fix.add_argument("--apply", action="store_true", help="Apply changes")
    p_fix.add_argument("--native", action="store_true", help="Run native fixer")
    p_fix.add_argument("--py-compat", action="store_true", help="Check Python .pyc compatibility")
    p_fix.add_argument("--conflicts", action="store_true", help="Detect tuning conflicts (stub)")
    p_fix.set_defaults(func=cmd_fix)

    p_doc = sub.add_parser("doctor", help="Run common fixes")
    p_doc.add_argument("--apply", action="store_true", help="Apply changes")
    p_doc.set_defaults(func=cmd_doctor)

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main()
