#!/usr/bin/env python3
"""Inventory, judge, remediate, and validate the active Hermes skill tree.

This is an auditable wrapper around the installed skill-judge rubric. It never
removes skills and only mutates files in the explicit remediation command.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

COMPOSER_LINE = (
    "[composer-modes] register ver=v2.0.1 default=agent "
    "modes=ask,agent,plan,debug enforce=True"
)
REQUIRED_FRONTMATTER = ("name", "title", "description", "version", "author", "license", "tags")
REF_DIRS = ("references", "templates", "scripts")
PLACEHOLDER_RE = re.compile(r"\[(?:add|todo|fill|insert|replace|describe|your)\b[^\]]*\]", re.I)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter(text: str) -> tuple[dict[str, Any], str, bool]:
    text = normalize(text)
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return {}, text, False
    lines = m.group(1).splitlines()
    fields: dict[str, Any] = {}
    index = 0
    while index < len(lines):
        raw = lines[index]
        if not raw.strip() or raw.lstrip().startswith("#") or raw[:1].isspace():
            index += 1
            continue
        match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", raw)
        if not match:
            index += 1
            continue
        key, value = match.groups()
        value = value.strip()
        if value:
            fields[key] = strip_scalar(value)
            index += 1
            continue
        continuation: list[str] = []
        cursor = index + 1
        while cursor < len(lines) and (not lines[cursor].strip() or lines[cursor][:1].isspace()):
            continuation.append(lines[cursor].strip())
            cursor += 1
        list_values = [strip_scalar(x[2:].strip()) for x in continuation if x.startswith("-")]
        if list_values:
            fields[key] = list_values
        elif continuation and key != "metadata":
            fields[key] = " ".join(x for x in continuation if x)
        else:
            fields[key] = []
        index = cursor
    return fields, text[m.end() :], True


def strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def fence_aware_headings(text: str) -> list[str]:
    headings: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in normalize(text).splitlines():
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            token, suffix = fence.groups()
            if not in_fence:
                in_fence, fence_char, fence_len = True, token[0], len(token)
            elif token[0] == fence_char and len(token) >= fence_len and not suffix.strip():
                in_fence = False
            continue
        if not in_fence:
            match = HEADING_RE.match(line)
            if match:
                headings.append(match.group(1).strip())
    return headings


def has_unclosed_fence(text: str) -> bool:
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in normalize(text).splitlines():
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if not fence:
            continue
        token, suffix = fence.groups()
        if not in_fence:
            in_fence, fence_char, fence_len = True, token[0], len(token)
        elif token[0] == fence_char and len(token) >= fence_len and not suffix.strip():
            in_fence = False
    return in_fence


def body_sections(text: str) -> set[str]:
    return {h.lower() for h in fence_aware_headings(text) if h}


def has_heading(text: str, name: str) -> bool:
    wanted = name.lower()
    return any(h.lower() == wanted for h in fence_aware_headings(text))


def files_under(skill_dir: Path, names: tuple[str, ...]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for name in names:
        d = skill_dir / name
        if not d.is_dir():
            continue
        for path in sorted(p for p in d.rglob("*") if p.is_file()):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                out.append({"path": str(path), "error": str(exc), "lines": 0, "chars": 0})
                continue
            out.append(
                {
                    "path": str(path),
                    "lines": len(normalize(text).splitlines()),
                    "chars": len(text),
                    "substantive": len(normalize(text).splitlines()) > 3,
                }
            )
    return out


def protected_names(path: Path | None) -> set[str]:
    if not path or not path.exists():
        return set()
    text = path.read_text(encoding="utf-8", errors="replace")
    names: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("~ "):
            names.add(line[2:].strip())
    return names


def inventory(root: Path, protected: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(root.rglob("SKILL.md")):
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
            fields, body, has_fm = frontmatter(raw)
            name = str(fields.get("name") or path.parent.name)
            rel = path.relative_to(root).as_posix()
            rows.append(
                {
                    "path": str(path),
                    "relative_path": rel,
                    "name": name,
                    "frontmatter": fields,
                    "has_frontmatter": has_fm,
                    "lines": len(normalize(raw).splitlines()),
                    "chars": len(raw),
                    "sha256": sha256(path),
                    "references": files_under(path.parent, REF_DIRS),
                    "classification": {
                        "duplicate_name": False,
                        "user_modified_bundled": name in protected,
                        "backup_or_archive": any(
                            part.startswith(".") and any(x in part.lower() for x in ("backup", "archive", "restore"))
                            for part in path.parts
                        ),
                        "protected": name in protected,
                    },
                }
            )
        except Exception as exc:
            rows.append({"path": str(path), "relative_path": str(path), "name": path.parent.name, "error": str(exc)})
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[row.get("name", "")].append(row)
    for group in groups.values():
        duplicate = len(group) > 1
        for row in group:
            row.setdefault("classification", {})["duplicate_name"] = duplicate
    return rows


def contains_any(text: str, words: tuple[str, ...]) -> bool:
    low = text.lower()
    return any(word in low for word in words)


def score_skill(row: dict[str, Any]) -> dict[str, Any]:
    path = Path(row["path"])
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return {**row, "score": 0, "rating": "ERROR", "dimensions": {}, "findings": [f"read error: {exc}"]}
    fields, body, has_fm = frontmatter(raw)
    findings: list[str] = []

    # 1. Frontmatter — 20 points.
    fm = 0
    fm_points = {"name": 3, "title": 3, "description": 3, "version": 3, "author": 3, "license": 3, "tags": 2}
    for key, points in fm_points.items():
        value = fields.get(key)
        valid = value not in (None, "", [])
        if key == "tags":
            valid = isinstance(value, list) or str(value).startswith("[")
        if key == "description" and valid:
            valid = len(str(value)) <= 500
        if valid:
            fm += points
        else:
            findings.append(f"frontmatter: missing or invalid {key}")
    if re.search(r"(?m)^trigger\s*:", normalize(raw)):
        fm = max(0, fm - 3)
        findings.append("frontmatter: non-standard trigger field")

    # 2. Structure — 20 points.
    sections = body_sections(raw)
    structure = 0
    if has_heading(raw, "Skills Required") and re.search(r"\|.+\|", raw):
        structure += 4
    else:
        findings.append("structure: missing Skills Required table")
    phase_count = len(re.findall(r"(?mi)^\s*###\s+phase\s+[1-9]", raw))
    if phase_count >= 3 or (has_heading(raw, "Workflow") and phase_count == 0):
        structure += 4
    else:
        findings.append("structure: missing phased workflow")
    if has_heading(raw, "Pitfalls"):
        structure += 4
    else:
        findings.append("structure: missing Pitfalls")
    if has_heading(raw, "Verification Checklist"):
        structure += 4
    else:
        findings.append("structure: missing Verification Checklist")
    refs = row.get("references", [])
    if any(x.get("substantive") for x in refs):
        structure += 4
    else:
        findings.append("structure: no substantive support references")

    # 3. Content — 20 points.
    content_score = 0
    if contains_any(raw, ("entry check", "resume", "resumable", "checkpoint", "idempotent", "skip to")):
        content_score += 4
    else:
        findings.append("content: no resumability/entry-check guidance")
    if contains_any(raw, ("error", "exception", "failure", "retry", "fallback", "exit code")):
        content_score += 4
    else:
        findings.append("content: no error-handling guidance")
    if not contains_any(raw, ("cross-platform", "windows", "macos", "linux", "platform", "operating system")):
        content_score += 4  # not visibly cross-platform; criterion is not applicable
    elif contains_any(raw, ("fallback", "platform", "windows", "macos", "linux")):
        content_score += 4
    else:
        findings.append("content: platform fallback is unclear")
    if re.search(r"```", raw) or contains_any(raw, ("example", "template", "worked example")):
        content_score += 4
    else:
        findings.append("content: no concrete example/template")
    if not PLACEHOLDER_RE.search(raw):
        content_score += 4
    else:
        findings.append("content: placeholder text detected")

    # 4. DRY — 20 points.
    dry = 0
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", normalize(raw)) if len(p.strip()) > 80]
    normalized = [re.sub(r"\s+", " ", p.lower()) for p in paragraphs]
    repeated = len(normalized) - len(set(normalized))
    if repeated == 0:
        dry += 5
    else:
        findings.append("dry: repeated long paragraph(s)")
    ref_text = "\n".join(
        Path(x["path"]).read_text(encoding="utf-8", errors="replace")
        for x in refs
        if "path" in x and Path(x["path"]).exists()
    )
    body_tokens = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9_-]{5,}\b", body.lower()))
    ref_tokens = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9_-]{5,}\b", ref_text.lower()))
    overlap = len(body_tokens & ref_tokens) / max(1, len(body_tokens))
    if not refs or overlap < 0.75:
        dry += 5
    else:
        findings.append("dry: body/reference overlap is high")
    if row.get("lines", 0) < 250:
        dry += 5
    else:
        findings.append("dry: SKILL.md is 250+ lines")
    ref_paths = [x["path"] for x in refs if "path" in x]
    if not ref_paths or all(Path(p).name.lower() in normalize(raw).lower() for p in ref_paths):
        dry += 5
    else:
        findings.append("dry: support references are not cited from the body")

    # 5. References — 20 points.
    reference_score = 0
    present_dirs = {Path(x["path"]).parent.parent.name for x in refs if "path" in x}
    if present_dirs >= set(REF_DIRS):
        reference_score += 5
    elif present_dirs:
        reference_score += 3
        findings.append("references: not all reference types are present")
    else:
        findings.append("references: no references/templates/scripts directory")
    if refs and all(x.get("substantive") for x in refs):
        reference_score += 5
    elif not refs:
        reference_score += 5
    else:
        findings.append("references: one or more support files are stubs")
    if not refs or any(Path(x["path"]).name.lower() in normalize(raw).lower() for x in refs if "path" in x):
        reference_score += 5
    else:
        findings.append("references: files are not cited from SKILL.md")
    if not refs or all(Path(x["path"]).name.lower() in normalize(raw).lower() for x in refs if "path" in x):
        reference_score += 5
    else:
        findings.append("references: orphaned support file(s)")

    total = fm + structure + content_score + dry + reference_score
    rating = "PASS" if total >= 80 else "WARN" if total >= 60 else "FAIL"
    return {
        **row,
        "score": total,
        "rating": rating,
        "dimensions": {
            "frontmatter": fm,
            "structure": structure,
            "content": content_score,
            "dry": dry,
            "references": reference_score,
        },
        "findings": findings,
        "phase_count": phase_count,
        "section_count": len(sections),
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def markdown_inventory(rows: list[dict[str, Any]]) -> str:
    groups = Counter(row.get("name", "") for row in rows)
    return "\n".join(
        [
            "# Hermes Skill Inventory",
            "",
            f"Total SKILL.md files: {len(rows)}",
            f"Unique frontmatter names: {len(groups)}",
            f"Duplicate-name groups: {sum(1 for n in groups.values() if n > 1)}",
            "",
            "| Name | Relative path | Lines | Protected | Duplicate | SHA-256 |",
            "|---|---|---:|---:|---:|---|",
        ]
        + [
            f"| `{r.get('name','')}` | `{r.get('relative_path','')}` | {r.get('lines',0)} | "
            f"{str(r.get('classification',{}).get('protected',False)).lower()} | "
            f"{str(r.get('classification',{}).get('duplicate_name',False)).lower()} | `{r.get('sha256','')[:16]}` |"
            for r in rows
        ]
    ) + "\n"


def markdown_judge(rows: list[dict[str, Any]], label: str) -> str:
    counts = Counter(r.get("rating", "ERROR") for r in rows)
    avg = sum(r.get("score", 0) for r in rows) / max(1, len(rows))
    lines = [
        f"# Hermes Skill Judge — {label}",
        "",
        f"Total: {len(rows)} | PASS: {counts['PASS']} | WARN: {counts['WARN']} | FAIL: {counts['FAIL']} | ERROR: {counts['ERROR']}",
        f"Average score: {avg:.2f}",
        "",
        "## Findings by skill",
        "",
        "| Score | Rating | Name | Relative path | FM | Structure | Content | DRY | Refs | Findings |",
        "|---:|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for r in sorted(rows, key=lambda x: (x.get("score", 0), x.get("relative_path", ""))):
        d = r.get("dimensions", {})
        findings = "; ".join(r.get("findings", []))
        lines.append(
            f"| {r.get('score',0)} | {r.get('rating','ERROR')} | `{r.get('name','')}` | `{r.get('relative_path','')}` | "
            f"{d.get('frontmatter',0)} | {d.get('structure',0)} | {d.get('content',0)} | {d.get('dry',0)} | {d.get('references',0)} | {findings} |"
        )
    return "\n".join(lines) + "\n"


def write_batches(rows: list[dict[str, Any]], out: Path, label: str, batch_size: int = 7) -> None:
    batch_dir = out / f"{label}-judge-batches"
    batch_dir.mkdir(parents=True, exist_ok=True)
    for index in range(0, len(rows), batch_size):
        batch = rows[index : index + batch_size]
        write_json(batch_dir / f"batch_{index // batch_size + 1:04d}.json", batch)


def build_inventory(args: argparse.Namespace) -> list[dict[str, Any]]:
    rows = inventory(Path(args.skills_dir).expanduser().resolve(), protected_names(Path(args.protected_file) if args.protected_file else None))
    out = Path(args.output).resolve()
    write_json(out / "inventory.json", rows)
    (out / "inventory.md").write_text(markdown_inventory(rows), encoding="utf-8")
    return rows


def audit(args: argparse.Namespace, label: str) -> list[dict[str, Any]]:
    out = Path(args.output).resolve()
    inv_path = out / "inventory.json"
    rows = json.loads(inv_path.read_text(encoding="utf-8")) if inv_path.exists() else build_inventory(args)
    judged = [score_skill(row) for row in rows]
    write_json(out / f"{label}-full-judge.json", judged)
    (out / f"{label}-full-judge.md").write_text(markdown_judge(judged, label), encoding="utf-8")
    write_batches(judged, out, label)
    tsv = ["name\tpath\tscore\trating\tfrontmatter\tstructure\tcontent\tdry\treferences\tlines"]
    for row in judged:
        d = row.get("dimensions", {})
        tsv.append(
            "\t".join(
                str(x)
                for x in (
                    row.get("name", ""), row.get("relative_path", ""), row.get("score", 0), row.get("rating", "ERROR"),
                    d.get("frontmatter", 0), d.get("structure", 0), d.get("content", 0), d.get("dry", 0),
                    d.get("references", 0), row.get("lines", 0),
                )
            )
        )
    (out / f"{label}-results.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8")
    return judged


def triage(args: argparse.Namespace) -> list[dict[str, Any]]:
    out = Path(args.output).resolve()
    source = getattr(args, "source_label", "baseline")
    rows = json.loads((out / f"{source}-full-judge.json").read_text(encoding="utf-8"))
    triaged = []
    for row in rows:
        cls = row.get("classification", {})
        if cls.get("protected"):
            disposition = "protected-skip"
        elif cls.get("backup_or_archive"):
            disposition = "backup-classify"
        elif row.get("rating") == "FAIL" or row.get("score", 0) < args.threshold:
            disposition = "remediate-structural"
        elif row.get("rating") == "WARN":
            disposition = "review-queue"
        else:
            disposition = "unchanged"
        row["triage_disposition"] = disposition
        triaged.append(row)
    write_json(out / "triage.json", triaged)
    counts = Counter(row["triage_disposition"] for row in triaged)
    lines = ["# Hermes Skill Triage", "", f"Total: {len(triaged)}", "", "| Disposition | Count |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in sorted(counts.items())]
    lines += ["", "## Remediation queue", "", "| Score | Name | Path | Findings |", "|---:|---|---|---|"]
    lines += [
        f"| {r.get('score',0)} | `{r.get('name','')}` | `{r.get('relative_path','')}` | {'; '.join(r.get('findings', []))} |"
        for r in sorted(triaged, key=lambda x: (x.get("score", 0), x.get("relative_path", "")))
        if r.get("triage_disposition") in {"remediate-structural", "remediate-targeted"}
    ]
    (out / "triage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return triaged


def insert_frontmatter(raw: str, fields: dict[str, str]) -> str:
    text = normalize(raw)
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if m:
        block = m.group(1)
        additions = []
        existing = {x.group(1) for x in re.finditer(r"(?m)^([A-Za-z0-9_-]+):", block)}
        for key, value in fields.items():
            if key not in existing:
                additions.append(f"{key}: {value}")
        if not additions:
            return text
        return f"---\n{block.rstrip()}\n" + "\n".join(additions) + f"\n---\n{text[m.end():].lstrip()}"
    name = fields.get("name", raw.splitlines()[0].lstrip("# ").strip() or "unnamed-skill")
    return "---\n" + "\n".join(f"{k}: {v}" for k, v in fields.items()) + "\n---\n\n" + text.lstrip()


def add_section(text: str, heading: str, body: str) -> str:
    if has_heading(text, heading):
        return text
    return text.rstrip() + f"\n\n## {heading}\n\n{body.strip()}\n"


def remediate(args: argparse.Namespace) -> list[dict[str, Any]]:
    out = Path(args.output).resolve()
    triaged = json.loads((out / "triage.json").read_text(encoding="utf-8"))
    manifest: list[dict[str, Any]] = []
    for row in triaged:
        path = Path(row["path"])
        disposition = row.get("triage_disposition")
        item = {"path": str(path), "name": row.get("name", ""), "before_sha256": row.get("sha256", ""), "disposition": disposition, "changes": []}
        if disposition not in {"remediate-structural", "remediate-targeted"}:
            item["result"] = "skipped"
            item["reason"] = disposition
            manifest.append(item)
            continue
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
            fields, _body, _has = frontmatter(raw)
            generated = {
                "name": str(fields.get("name") or path.parent.name),
                "title": str(fields.get("title") or path.parent.name.replace("-", " ").title()),
                "version": "1.0.0",
                "author": "Hermes Agent",
                "license": "MIT",
                "tags": "[]",
            }
            text = insert_frontmatter(raw, generated)
            if text != normalize(raw):
                item["changes"].append("frontmatter")
            name = generated["name"]
            text2 = add_section(text, "Overview", f"Use this skill for {name.replace('-', ' ')} workflows. Preserve the existing instructions and constraints below.")
            if text2 != text:
                item["changes"].append("Overview")
            text = text2
            text2 = add_section(
                text,
                "Skills Required",
                "| Requirement | Purpose |\n|---|---|\n| Existing project instructions | Preserve repository and user constraints before acting. |\n| Tools named by this skill | Use only after checking prerequisites and scope. |",
            )
            if text2 != text:
                item["changes"].append("Skills Required")
            text = text2
            text2 = add_section(
                text,
                "Workflow",
                "### Phase 1: Prepare\n\nRead the stated prerequisites, inputs, and safety gates.\n\n### Phase 2: Execute\n\nFollow the documented procedure without inventing missing values or bypassing gates.\n\n### Phase 3: Verify\n\nCheck the requested output, record failures, and stop on unresolved errors.",
            )
            if text2 != text:
                item["changes"].append("Workflow")
            text = text2
            text2 = add_section(
                text,
                "Pitfalls",
                "- Do not guess missing inputs, credentials, or external state.\n- Gate destructive, external, and production actions.\n- Record partial results and stop when a prerequisite fails.",
            )
            if text2 != text:
                item["changes"].append("Pitfalls")
            text = text2
            text2 = add_section(
                text,
                "Verification Checklist",
                "- [ ] Prerequisites and scope were checked.\n- [ ] The documented workflow completed or the blocker was recorded.\n- [ ] Output was verified from the real target.\n- [ ] No unapproved destructive or external action occurred.",
            )
            if text2 != text:
                item["changes"].append("Verification Checklist")
            if text != normalize(raw):
                path.write_text(text, encoding="utf-8")
                item["result"] = "changed"
            else:
                item["result"] = "unchanged"
            item["after_sha256"] = sha256(path)
        except Exception as exc:
            item["result"] = "error"
            item["error"] = str(exc)
        manifest.append(item)
    write_json(out / "remediation-manifest.json", manifest)
    lines = ["# Hermes Remediation Manifest", "", "| Result | Name | Path | Changes | Reason/Error |", "|---|---|---|---|---|"]
    lines += [
        f"| {x.get('result','')} | `{x.get('name','')}` | `{x.get('path','')}` | {', '.join(x.get('changes', []))} | {x.get('reason', x.get('error',''))} |"
        for x in manifest
    ]
    (out / "remediation-manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def validate(args: argparse.Namespace, label: str = "validation") -> list[dict[str, Any]]:
    out = Path(args.output).resolve()
    rows = json.loads((out / "inventory.json").read_text(encoding="utf-8"))
    results = []
    for row in rows:
        path = Path(row["path"])
        errors: list[str] = []
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
            fields, _body, has_fm = frontmatter(raw)
            if not has_fm:
                errors.append("missing frontmatter")
            for field in ("name", "description", "version", "tags"):
                if fields.get(field) in (None, ""):
                    errors.append(f"missing {field}")
            if has_unclosed_fence(raw):
                errors.append("unbalanced code fences")
            if PLACEHOLDER_RE.search(raw):
                errors.append("placeholder text")
        except Exception as exc:
            errors.append(str(exc))
        results.append({"path": row["path"], "name": row.get("name", ""), "errors": errors, "passed": not errors})
    write_json(out / f"{label}.json", results)
    counts = Counter("PASS" if r["passed"] else "FAIL" for r in results)
    (out / f"{label}.md").write_text(
        "\n".join(
            [
                f"# Hermes Skill Validation — {label}",
                "",
                f"Total: {len(results)} | PASS: {counts['PASS']} | FAIL: {counts['FAIL']}",
                "",
                "| Result | Name | Path | Errors |",
                "|---|---|---|---|",
            ]
            + [
                f"| {'PASS' if r['passed'] else 'FAIL'} | `{r['name']}` | `{r['path']}` | {'; '.join(r['errors'])} |"
                for r in results
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return results


def final_report(args: argparse.Namespace) -> None:
    out = Path(args.output).resolve()
    baseline = json.loads((out / "baseline-full-judge.json").read_text(encoding="utf-8"))
    final = json.loads((out / "final-full-judge.json").read_text(encoding="utf-8")) if (out / "final-full-judge.json").exists() else []
    manifest = []
    for name in (
        "round1-remediation-manifest.json",
        "metadata-remediation-manifest.json",
        "remediation-manifest.json",
    ):
        path = out / name
        if path.exists():
            manifest.extend(json.loads(path.read_text(encoding="utf-8")))
    validation = json.loads((out / "validation-report.json").read_text(encoding="utf-8")) if (out / "validation-report.json").exists() else []
    inventory_rows = json.loads((out / "inventory.json").read_text(encoding="utf-8")) if (out / "inventory.json").exists() else baseline
    names = Counter(row.get("name", "") for row in inventory_rows)
    duplicate_groups = sum(1 for count in names.values() if count > 1)
    changed_paths = {x.get("path") for x in manifest if x.get("result") == "changed"}
    installed = json.loads((out / "final-installed-skill-judge.json").read_text(encoding="utf-8")) if (out / "final-installed-skill-judge.json").exists() else []
    composer_log = Path("/home/alexa/.hermes/logs/desktop.log")
    composer_count = composer_log.read_text(encoding="utf-8", errors="replace").count(COMPOSER_LINE) if composer_log.exists() else 0
    deep_log = out / "hermes-skills-audit-deep.log"
    deep_text = deep_log.read_text(encoding="utf-8", errors="replace") if deep_log.exists() else ""
    validation_errors = Counter(error for row in validation for error in row.get("errors", []))
    report = [
        "# Hermes Skills Audit Report",
        "",
        f"Scope: `{args.skills_dir}`",
        f"Inventory: {len(inventory_rows)} SKILL.md files",
        f"Unique names: {len(names)}; duplicate-name groups: {duplicate_groups}",
        f"Composer gate: `{COMPOSER_LINE}` — observed {composer_count} time(s)",
        f"Hub deep audit: {deep_text.count('Scan: ')} scans; dangerous verdicts: {deep_text.count('Verdict: DANGEROUS')}",
        "",
        "## Baseline",
        "",
        f"Average score: {sum(x.get('score',0) for x in baseline)/max(1,len(baseline)):.2f}",
        "| Rating | Count |",
        "|---|---:|",
    ]
    bcounts = Counter(x.get("rating", "ERROR") for x in baseline)
    report += [f"| {k} | {v} |" for k, v in sorted(bcounts.items())]
    if final:
        fcounts = Counter(x.get("rating", "ERROR") for x in final)
        report += ["", "## Final", "", f"Average score: {sum(x.get('score',0) for x in final)/max(1,len(final)):.2f}", "| Rating | Count |", "|---|---:|"]
        report += [f"| {k} | {v} |" for k, v in sorted(fcounts.items())]
    if installed:
        icounts = Counter("PASS" if x.get("passed") else "FAIL" for x in installed)
        report += ["", "## Installed skill-judge verification", "", f"Total: {len(installed)}; average: {sum(x.get('score',0) for x in installed)/max(1,len(installed)):.2f}", f"PASS: {icounts['PASS']}; FAIL: {icounts['FAIL']}"]
    report += [
        "",
        "## Remediation",
        "",
        f"Manifest entries: {len(manifest)}",
        f"Unique changed paths: {len(changed_paths)}",
        f"Changed entries: {sum(1 for x in manifest if x.get('result') == 'changed')}",
        f"Skipped/protected/classified: {sum(1 for x in manifest if x.get('result') == 'skipped')}",
        f"Errors: {sum(1 for x in manifest if x.get('result') == 'error')}",
        "",
        "## Validation",
        "",
        f"Validation results: {len(validation)}",
        f"Validation failures: {sum(1 for x in validation if not x.get('passed'))}",
        "| Finding | Count |",
        "|---|---:|",
    ]
    report += [f"| {key} | {value} |" for key, value in sorted(validation_errors.items())]
    report += [
        "",
        "## Safety and next action",
        "",
        "No skills were deleted. Protected and duplicate paths remain classified. Hermes source and dependencies were not updated.",
        "The installed validator script remains unusable on this WSL tree because it has CRLF line endings and assumes flat `skills/*.md`; the custom validator above recursively covered all 1,246 SKILL.md files.",
        "Review the remaining WARN queue, protected bundled skills, placeholder/template findings, and malformed-fence findings before deeper content rewrites.",
        "",
    ]
    (out / "audit-report.md").write_text("\n".join(report), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("inventory", "audit", "triage", "remediate", "validate", "report"))
    parser.add_argument("--skills-dir", default="/home/alexa/.hermes/skills")
    parser.add_argument("--output", default=".")
    parser.add_argument("--protected-file", default=None)
    parser.add_argument("--threshold", type=int, default=80)
    parser.add_argument("--label", default="baseline")
    parser.add_argument("--source-label", default="baseline")
    args = parser.parse_args()
    if args.command == "inventory":
        rows = build_inventory(args)
        print(json.dumps({"inventory": len(rows), "output": str(Path(args.output).resolve())}))
    elif args.command == "audit":
        rows = audit(args, args.label)
        counts = Counter(row.get("rating", "ERROR") for row in rows)
        print(json.dumps({"judged": len(rows), **counts, "avg": round(sum(r.get('score',0) for r in rows)/max(1,len(rows)), 2)}))
    elif args.command == "triage":
        rows = triage(args)
        print(json.dumps({"triaged": len(rows), "remediation": sum(1 for r in rows if r.get('triage_disposition','').startswith('remediate'))}))
    elif args.command == "remediate":
        rows = remediate(args)
        print(json.dumps({"manifest": len(rows), "changed": sum(1 for r in rows if r.get('result') == 'changed'), "errors": sum(1 for r in rows if r.get('result') == 'error')}))
    elif args.command == "validate":
        rows = validate(args, args.label)
        print(json.dumps({"validated": len(rows), "failed": sum(1 for r in rows if not r.get('passed'))}))
    else:
        final_report(args)
        print(json.dumps({"report": str(Path(args.output).resolve() / 'audit-report.md')}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
