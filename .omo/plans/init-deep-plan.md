# Init-Deep Plan (Updated 2026-10-13 — clarification completed)

Scope: Initialize/update `.omo/plans/init-deep-plan.md`, `.omo/specs/init-spec.md`, `.omo/plans/init-deep-run-card.md` referencing `.omo/plans/init-deep.md` and `repo-init` skill.
Source reference: `.omo/plans/init-deep.md` (generated 2026-10-13).
Cross-reference: `.omo/plans/hooks-plan.md`.

Clarification results (contract applied — 5 questions answered):
- Task: repo-init skill (`scripts/repo-init.py --init` / agent inventory scaffolding) selected over init-deep artifacts, BUT artifacts to create/update = `.omo/plans/init-deep-plan.md`, `.omo/specs/init-spec.md`, `.omo/plans/init-deep-run-card.md`.
- Validation: init-deep checklist (`ruff check .`, identity sync `.hermes.md` vs `AGENTS.md`, `python manage.py test`, artifact presence + references).
- Execution: deferred (PLAN MODE). Safe assumption: this plan file specifies artifacts/references; actual mutation deferred to implementer/subagent.
- Contradiction record: `/tmp/contradiction-record-repo-init.md` (user instruction implies execution workflow; safe deferred assumption adopted; no new contradiction — user's deferred choice aligns with safe assumption).

Artifacts specified by this plan:
- `.omo/plans/init-deep-plan.md` (this file — updated with clarification, skills/references, deferred note)
- `.omo/specs/init-spec.md` (verify/update — must reference `.omo/plans/init-deep.md` and include requirements/acceptance/non-goals/constraints)
- `.omo/plans/init-deep-run-card.md` (verify/update — status rows for detect, inspect, plan, implement, test, verify, sync, document; must reference previous steps)

Plan steps (from `.omo/plans/hooks-plan.md` sequence; updated 2027-01-01 with session reference):
1. Detect: read `.omo/plans/init-deep.md`, `.omo/plans/hooks-plan.md`, `docs/scope/scope.md`.
2. Inspect: verify agent identity (`.hermes.md` vs `AGENTS.md`); confirm profile `default` active (`hermes profile list`).
3. Plan: `.omo/plans/init-deep-plan.md` (updated with clarification results + session reference) + `.omo/plans/session-plan.md` (new session artifact) created.
4. Implement (Artifacts + Skills): create/update `.omo/specs/init-spec.md` (`.omo/specs/session-spec.md` created); apply `engineer-args-kwargs` verification; audit skills; apply `skill-judge`; run `/session-audit`.
5. Implement (Execution deferred to implementer): actual Django code changes deferred (plan mode); artifacts and audit reports produced now.
6. Test: verify artifacts exist (`ruff check .` if Python changed; `python manage.py test` if Django env active and code modified; `hermes skills --help` for skills audit).
7. Verify logs: `.omo/plans/session-run-card.md` (new) contains status rows; `.omo/specs/session-spec.md` verifies.
8. Systematic debug: apply `/systematic-debugging` unconditionally (mandatory per user-selected option in clarification; no contradiction — safe path adopted).
9. Sync: reconcile workspace state; update `docs/scope/scope.md` (no destructive edit — keep existing feature table).
10. Document changelog: update `.omo/plans/init-deep-plan.md` final verification notes; `session-audit-report.md` generated.

Validation checklist (derived from `.omo/plans/init-deep.md`):
- [ ] `ruff check .` passes (or only non-blocking warnings)
- [ ] Agent identity synchronization verified (`.hermes.md` aligns with `AGENTS.md`; profile linkage `default` confirmed via `hermes profile list`)
- [ ] `python manage.py test` passes in Django env (`DJANGO_SETTINGS_MODULE=rhixecompany.settings` if needed)
- [ ] `.omo/plans/init-deep-plan.md` exists, references `.omo/plans/init-deep.md`, and includes clarification/skills/references/deferred note
- [ ] `.omo/specs/init-spec.md` exists, references `.omo/plans/init-deep.md`, includes requirements/acceptance/non-goals/constraints
- [ ] `.omo/plans/init-deep-run-card.md` exists, references previous steps, contains status rows for detect/inspect/plan/implement/test/verify/sync/document
- [ ] No secrets (`.env`, tokens) committed; no npm dependencies added (`package.json` unchanged); no settings overwritten without override check (`rhixecompany/setting.py` verified)

Skills / References Used:
- `repo-planning-quick-commands` (development skill): inventory/audit pattern applied to `.omo/` artifacts.
- `repo-init` (devops skill): agent inventory / scaffolding reference (`scripts/repo-init.py` workflow: `--list-agents`, `--init`, `--verify`).
- `readme-blueprint-generator` (development skill): included per user instruction (`execute and implement include /readme-blueprint-generator`).
- `.omo/plans/init-deep.md`: source reference for Django sub-project identity and conventions.
- `.omo/plans/hooks-plan.md`: cross-reference for verification sequence (systematic-debugging mandatory; deferred execution assumption documented).
- `clarify-requirements`: clarification contract applied; 5 select questions answered; safe deferred assumption adopted; contradiction record saved at `/tmp/contradiction-record-repo-init.md`.

Notes / Assumptions:
- PLAN MODE applies: actual mutation deferred. Implementer/subagent must confirm plan approval before creating/updating `.omo/specs/init-spec.md` and `.omo/plans/init-deep-run-card.md`, running validation checklist, and applying `/systematic-debugging`.
- If implementer selects an option conflicting with deferred assumption (e.g., forcing execution without approval), record contradiction per `/tmp/contradiction-record-[project].md` format before applying.
