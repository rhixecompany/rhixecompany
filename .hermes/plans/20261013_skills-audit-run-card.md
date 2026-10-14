# Hermes Skills Audit Run Card

Run id: 20261013_skills_audit
Session deliverable: hermes-skills-audit-report

## Command contract

- Active root: `/home/alexa/.hermes/skills`
- Audit every recursive `SKILL.md`.
- Use the `skill-judge` rubric for each skill.
- Use the audit report as the only remediation input.
- Validate and re-judge after every remediation batch.
- Preserve protected, bundled, hub-installed, duplicate, and backup files unless separately approved.
- Do not run Hermes update, dependency upgrades, destructive deletion, publication, or production actions.

## Composer Modes gate

Before and after the pipeline, verify this exact live registration line:

`[composer-modes] register ver=v2.0.1 default=agent modes=ask,agent,plan,debug enforce=True`

If absent or different: stop the mutation phase, record the evidence, and report the blocker.

## Artifacts

- `inventory.json` / `inventory.md`
- `baseline-judge.json` / `baseline-judge.md` / `baseline-results.tsv`
- `triage.json` / `triage.md`
- `remediation-manifest.json` / `remediation-manifest.md`
- `final-judge.json` / `final-judge.md` / `final-results.tsv`
- `validation-report.json` / `validation-report.md`
- `audit-report.md` — final human-readable report

## Exit gates

- Inventory count equals baseline judge count and final judge count.
- Every skill has a disposition: remediated, unchanged, protected/skipped, duplicate-classified, or error.
- Every changed file has on-disk validation and a post-change judge result.
- No score regressions are hidden.
- `bun run check` and `npm run check` pass after project-file changes.
- Final report states remaining blockers and next action.
