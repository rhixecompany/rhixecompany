# Hermes Skills Audit and Remediation Plan

Run id: 20261013_skills_audit
Active profile: default

## Phase 0 — Preconditions

- Confirm active profile and current repository state.
- Confirm `/home/alexa/.hermes/skills` is the active skill root.
- Confirm composer-modes registration exactness from live logs.
- Inspect batch judge, audit, validator, and remediation scripts before execution.
- Do not run `hermes skills update` or modify Hermes configuration.

## Phase 1 — Inventory and triage

- Enumerate every `SKILL.md` recursively.
- Parse frontmatter and classify: canonical, duplicate-name, backup/archive, bundled/protected, hub-installed, malformed, placeholder, or editable local.
- Record file hash, line count, references/templates/scripts, and safety flags.
- Store the inventory before any edit.

## Phase 2 — Baseline audit

- Run the installed `skill-judge` rubric once per discovered skill, in resumable batches.
- Produce per-skill results plus aggregate Markdown/JSON/TSV reports.
- Reconcile enumerated count against result count programmatically.
- Triage findings into high/medium/low remediation queues.

## Phase 3 — Evidence-backed remediation

- Apply only deterministic structural fixes supported by the audit: valid frontmatter, missing workflow sections, explicit prerequisites/error handling, verification checklist, and real references where content is available.
- Never mass-inject empty templates or duplicate prose.
- Never edit protected/bundled/hub-installed skills unless the source marks them user-modified and the edit is safe; otherwise record the skip.
- Write a patch/remediation manifest for every attempted file.

## Phase 4 — Validation and re-judge

- Validate all skills from disk, including unchanged skills for final coverage.
- Re-run `/skill-judge` for every discovered skill, not only changed files.
- Compare baseline and final scores/dimensions; flag regressions.
- Verify exact composer registration again.

## Phase 5 — Repository verification and close

- Run `bun run check` and `npm run check` if present.
- Verify generated artifacts, counts, and git status.
- Write final report with scope, evidence, skipped work, risks, and next action.
- Do not commit, publish, delete, or update Hermes.

## Batch controls

- Batch size: 7 skills, matching the installed judge guidance.
- Resume marker: one result file per batch and a manifest of completed paths.
- Fail-open per skill: record parse/judge errors and continue; never drop a target.
- Final gate: no aggregate total is accepted unless it equals the inventory total.
