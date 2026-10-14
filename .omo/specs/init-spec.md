# Init Specification (Updated 2026-10-13 — execution approved, deferred overridden)

Project: profile workspace Django sub-project (`base/` + `rhixecompany/`).
Source reference: `.omo/plans/init-deep.md` (generated 2026-10-13).
Cross-reference: `.omo/plans/hooks-plan.md`.

Clarification results (5 questions answered, contract applied):
- Task target: repo-init skill (`scripts/repo-init.py` workflow) referenced; artifacts = `.omo/plans/init-deep-plan.md`, `.omo/specs/init-spec.md`, `.omo/plans/init-deep-run-card.md`.
- Execution: deferred (PLAN MODE) overridden by user out-of-band instruction (`execute and implement include /readme-blueprint-generator`). Contradiction recorded at `/tmp/contradiction-record-repo-init.md`.
- Skills/references used: `repo-planning-quick-commands`, `repo-init`, `readme-blueprint-generator`, `.omo/plans/init-deep.md`, `.omo/plans/hooks-plan.md`, `clarify-requirements`.

Requirements:
1. Verify agent identity synchronization (`.hermes.md` aligns with `AGENTS.md`). Confirm profile linkage (`default`) via `hermes profile list`.
2. Confirm Django environment (`myvenv/` or equivalent) is active; run `python manage.py test` with `DJANGO_SETTINGS_MODULE=rhixecompany.settings` when needed.
3. Confirm lint (`ruff check .`) passes per `.ruff.toml` (120 chars line length, 4-space indentation from `.editorconfig`).
4. Confirm `.omo/plans/init-deep-plan.md`, `.omo/specs/init-spec.md`, and `.omo/plans/init-deep-run-card.md` exist, reference `.omo/plans/init-deep.md`, and include clarification/references/deferred override.
5. Confirm `.omo/plans/init-deep-plan.md` includes `readme-blueprint-generator` reference (per user instruction) and `repo-init` skill reference.
6. Confirm no secrets (`.env`, tokens) committed; no npm dependencies added (`package.json` unchanged); no settings overwritten without override check (`rhixecompany/setting.py` verified).

Acceptance Criteria:
- `.omo/plans/init-deep-plan.md` created/updated and contains validation checklist from `.omo/plans/init-deep.md`, clarification results, deferred override note, and skills/references (`repo-planning-quick-commands`, `repo-init`, `readme-blueprint-generator`).
- `.omo/specs/init-spec.md` (this file) updated, references source, includes clarification, override note, and `readme-blueprint-generator` reference.
- `.omo/plans/init-deep-run-card.md` updated with status rows for detect/inspect/plan/implement/test/verify/sync/document; references previous steps and contradiction record.
- All three artifacts contain `.omo/plans/init-deep.md` reference string.
- Contradiction assumption (`/tmp/contradiction-record-repo-init.md`) saved, referenced, and new contradiction (deferred overridden) appended before mutation.
- Validation executed: `ruff check .`, identity sync, `python manage.py test`, artifacts verified.
- Systematic-debugging (`/systematic-debugging`) applied regardless of validation result.

Non-Goals:
- Do NOT modify `.env`, `base/` source files, `rhixecompany/settings.py` (without override check), or move original JS vendor objects.
- Do NOT add npm dependencies (`package.json` unchanged).
- Do NOT commit secrets.
- Do NOT use README as source of truth (`.hermes.md` and `.omo/plans/init-deep.md` are canonical).

Constraints:
- Deferred mode overridden; execution proceeds per user instruction.
- Any destructive or identity/config change must include verification (`ruff check .`, identity sync, Django test) and explanation.
- Systematic-debugging (`/systematic-debugging`) must be applied after tests regardless of pass/fail (mandatory per user-selected option).
- `readme-blueprint-generator` skill must be included/referenced in plan artifacts.
