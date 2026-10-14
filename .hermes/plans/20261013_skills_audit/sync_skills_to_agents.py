#!/usr/bin/env python3
"""Merge audited Hermes skills into installed agent skill roots."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

SKIP_SUFFIXES = (":Zone.Identifier",)
SKIP_NAMES = {".DS_Store", "__pycache__"}
DEFAULT_TARGETS = {
    "opencode": Path.home() / ".config/opencode/skills",
    "grok": Path.home() / ".grok/skills",
    "codex": Path.home() / ".codex/skills",
    "cursor-agent": Path.home() / ".cursor/skills",
    "copilot": Path.home() / ".copilot/skills",
    "shared-agents-alias": Path.home() / ".agents/skills",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def active_roots(source: Path) -> list[Path]:
    return sorted(
        path
        for path in source.iterdir()
        if path.is_dir() and any(path.rglob("SKILL.md"))
    )


def source_files(source: Path) -> tuple[list[Path], int]:
    files: list[Path] = []
    excluded = 0
    for root in active_roots(source):
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.name in SKIP_NAMES or path.name.endswith(SKIP_SUFFIXES):
                excluded += 1
                continue
            files.append(path)
    return sorted(files), excluded


def sync_target(
    source: Path,
    target: Path,
    backup_root: Path,
    files: list[Path],
    dry_run: bool,
) -> dict[str, int | str]:
    stats = {"new": 0, "replaced": 0, "unchanged": 0, "backups": 0}
    for source_file in files:
        relative = source_file.relative_to(source)
        target_file = target / relative
        if target_file.exists() and target_file.is_file():
            if digest(source_file) == digest(target_file):
                stats["unchanged"] += 1
                continue
            stats["replaced"] += 1
            if not dry_run:
                backup = backup_root / relative
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target_file, backup)
                stats["backups"] += 1
        else:
            stats["new"] += 1
        if not dry_run:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            temporary = target_file.with_name(f".{target_file.name}.hermes-sync.tmp")
            shutil.copy2(source_file, temporary)
            temporary.replace(target_file)
    stats["target"] = str(target)
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path.home() / ".hermes/skills")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not source.is_dir():
        raise SystemExit(f"source skills directory not found: {source}")
    files, excluded = source_files(source)
    skill_count = sum(path.name == "SKILL.md" for path in files)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    backup_root = output / "backups" / timestamp
    results = {
        "source": str(source),
        "source_skill_count": skill_count,
        "source_file_count": len(files),
        "excluded_metadata_files": excluded,
        "dry_run": args.dry_run,
        "targets": {},
    }
    for name, target in DEFAULT_TARGETS.items():
        results["targets"][name] = sync_target(
            source, target.expanduser().resolve(), backup_root / name, files, args.dry_run
        )
    output.mkdir(parents=True, exist_ok=True)
    (output / "sync-manifest.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
