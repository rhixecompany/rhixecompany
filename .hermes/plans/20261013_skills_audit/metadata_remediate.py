#!/usr/bin/env python3
"""Add missing skill metadata without rewriting skill instructions."""
from __future__ import annotations

import json
import sys
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(RUN_DIR))
from skills_pipeline import frontmatter, insert_frontmatter, sha256, write_json  # noqa: E402


def main() -> int:
    out = RUN_DIR
    rows = json.loads((out / "inventory.json").read_text(encoding="utf-8"))
    manifest = []
    for row in rows:
        path = Path(row["path"])
        item = {"path": str(path), "name": row.get("name", ""), "changes": [], "result": "skipped"}
        if row.get("classification", {}).get("protected"):
            item["reason"] = "protected bundled skill"
            manifest.append(item)
            continue
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
            fields, _body, _has = frontmatter(raw)
            name = str(fields.get("name") or path.parent.name)
            generated = {
                "name": name,
                "title": str(fields.get("title") or name.replace("-", " ").title()),
                "description": f"Use when working with {name.replace('-', ' ')} workflows.",
                "version": "1.0.0",
                "author": "Hermes Agent",
                "license": "MIT",
                "tags": "[hermes]",
            }
            missing = [key for key, value in generated.items() if fields.get(key) in (None, "", [])]
            if not missing:
                manifest.append(item)
                continue
            text = insert_frontmatter(raw, {key: generated[key] for key in missing})
            if text != raw.replace("\r\n", "\n").replace("\r", "\n"):
                path.write_text(text, encoding="utf-8")
                item["result"] = "changed"
                item["changes"] = missing
                item["before_sha256"] = row.get("sha256", "")
                item["after_sha256"] = sha256(path)
            else:
                item["reason"] = "metadata already present after normalization"
        except Exception as exc:  # keep the batch resumable
            item["result"] = "error"
            item["error"] = str(exc)
        manifest.append(item)
    write_json(out / "metadata-remediation-manifest.json", manifest)
    lines = [
        "# Hermes Metadata Remediation Manifest",
        "",
        f"Total: {len(manifest)}",
        f"Changed: {sum(1 for x in manifest if x.get('result') == 'changed')}",
        f"Skipped: {sum(1 for x in manifest if x.get('result') == 'skipped')}",
        f"Errors: {sum(1 for x in manifest if x.get('result') == 'error')}",
        "",
        "| Result | Name | Path | Changes | Reason/Error |",
        "|---|---|---|---|---|",
    ]
    lines += [
        f"| {x.get('result')} | `{x.get('name','')}` | `{x.get('path','')}` | {', '.join(x.get('changes', []))} | {x.get('reason', x.get('error',''))} |"
        for x in manifest
    ]
    (out / "metadata-remediation-manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"total": len(manifest), "changed": sum(1 for x in manifest if x.get("result") == "changed"), "errors": sum(1 for x in manifest if x.get("result") == "error")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
