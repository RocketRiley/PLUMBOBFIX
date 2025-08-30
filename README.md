# simdoc

`simdoc` is a local command-line helper for The Sims 4 mods and custom content.
It scans, diagnoses, and safely applies fixes after game updates. All
operations are deterministic, idempotent, and perform backups before
changing any files.

## Features

- Detect game version changes and inventory mods.
- Parse `lastException.txt` to highlight failing mods.
- Clear native caches like `localthumbcache.package`.
- Remove incompatible `.pyc` files to ensure Python compatibility.
- Stubbed tuning conflict detection for future expansion.
- Always dry-runs by default; use `--apply` to modify files.
- Generates Markdown reports and timestamped backups.

## Quickstart

```bash
simdoc init --sims-folder "C:/Users/<you>/Documents/Electronic Arts/The Sims 4"
simdoc scan
simdoc fix --py-compat --native           # dry run
simdoc fix --apply --py-compat --native   # actually apply
simdoc doctor --apply                     # shortcut for common fixes
```

## Limitations

- Tuning conflict detection is a placeholder.
- Better Exceptions integration is planned but not implemented.

## License

MIT
