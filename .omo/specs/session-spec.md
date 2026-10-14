# Session Spec (2027-01-01) — Implementation + Skills Audit + Session Audit

**Status:** Proposed (linked to session; no scope feature row links it, so standalone decision spec)  
**Author:** Default agent  
**References:** `.omo/plans/init-deep.md`, `docs/scope/scope.md`, `.hermes.md`, `AGENTS.md`  
**Mode:** FEATURE / CROSS-CUTTING (session-level work spanning implementation artifacts, skills audit, and session audit)

## Summary

This spec defines the work for the current session: (1) create/update plan, spec, run-card artifacts per clarification; (2) apply `engineer-args-kwargs` skill verification; (3) audit available Hermes skills across mentioned categories; (4) validate skills with `hermes skills --help` and `/skill-judge`; (5) run `/session-audit` and generate `session-audit-report.md`. The spec is standalone (no scope feature links it) and uses the documentation context from `.omo/plans/init-deep.md`.

## Requirements (derived from clarification + `.omo/plans/init-deep.md`)

Requirements (seeded from user request and clarification contract):
- R1: Update `.omo/plans/init-deep-plan.md` to include clarification results, deferred note, skills/references, and session reference.
- R2: Create/update `.omo/plans/init-deep-run-card.md` with status rows for detect/inspect/plan/implement/test/verify/sync/document.
- R3: Create/update `.omo/specs/init-spec.md` referencing `.omo/plans/init-deep.md` and including requirements/acceptance/non-goals/constraints.
- R4: Apply `engineer-args-kwargs` verification (`scripts/normalize_args_kwargs.py` inspection + checklist).
- R5: Create audit reports per mentioned skills category (development, agentic-coder, planning, architecture, etc.).
- R6: Apply `hermes skills --help` and `/skill-judge` to updated skills in batches, covering categories subfolder.
- R7: Run `/session-audit` (via `session-audit` skill or native command) and generate `session-audit-report.md`.
- R8: Ensure identity sync verified (`.hermes.md` aligns with `AGENTS.md`), profile `default` active.
- R9: Preserve integrity: no secrets committed; `package.json` unchanged; Django settings override (`rhixecompany/setting.py`) verified; `.env` untouched.

## Acceptance criteria (Done when)

- `.omo/plans/init-deep-plan.md` exists, references `init-deep.md`, and passes the checklist.
- `.omo/plans/init-deep-run-card.md` exists and references previous steps.
- `.omo/specs/init-spec.md` exists, references `.omo/plans/init-deep.md`, and includes requirements/acceptance/non-goals/constraints.
- `.omo/plans/session-plan.md` and `.omo/plans/session-run-card.md` created.
- `engineer-args-kwargs` verification completed (script read, checklist executed, no invocation of target callable, JSON-safe diagnostics produced).
- Skills audit reports exist for mentioned categories (at minimum: one per category audited).
- Skill validation (`hermes skills --help` + `/skill-judge`) executed in batches; evidence saved (batch results documented).
- Session audit (`/session-audit`) completed; `session-audit-report.md` (or equivalent) exists in `.omo/plans/` or `docs/scope/`.
- `ruff check .` passes (if any Python changed); `python manage.py test` passes (if Django env active and tests affected).
- No synthetic results; real evidence (file sizes, exit codes, audit outputs) preserved.

## Non-goals (out of scope for this session, per clarification)

- Not auditing all 38 categories (limited to mentioned categories: development, agentic-coder, planning, architecture, etc.).
- Not modifying agent identity files (`.hermes.md`, `AGENTS.md`) unless identity sync verification fails.
- Not creating new Django features or modifying `base/` code (implementation deferred to subagent/implementer per plan mode).
- Not committing to git (no push or history rewrite unless explicitly requested).
- Not installing new npm dependencies (package.json unchanged per anti-patterns).

## Constraints

- Use POSIX syntax for terminal tool calls; provide PowerShell variants only when ambiguity risk exists.
- Prefer MCP-first tool precedence (`mcp-filesystem`, `mcp-ast-grep`, etc.) over native tools.
- Enforce DRY principle (no duplication across files/responses); reference rather than repeat.
- Apply `user-communication-preferences`: concise, action-first, blunt + technical tone, no filler.
- Apply `scope` output style (plain words, no dashes/hyphens in prose; code/file paths keep hyphens).
- Verify identity sync before any identity/config change (`.hermes.md` vs `AGENTS.md`).
- Record contradictions per `/tmp/contradiction-record-[project].md` format if any conflicting option arises.

## Design / Build plan (aligned with approach from scope)

Approach: Tracer Bullet (thin end-to-end thread through every layer — artifacts → skills → audit → validation → session audit), then thicken. Not a facade or journey split; each phase touches the full pipeline briefly.

Build order:
1. Artifacts update (plan, spec, run-card, session artifacts).
2. `engineer-args-kwargs` verification (inspection + checklist).
3. Skills search and inventory (discover categories, list skills, read reference docs).
4. Audit reports per category (search, triage, consolidate, deduplicate, enhance notes).
5. Skill validation (`hermes skills --help` + `/skill-judge`) in batches.
6. Session audit run (`/session-audit`) and report generation.
7. Final sync: verify identity, document outcomes, clean up temporary files.

## Consequences / Follow-up

- This session produces durable artifacts (`.omo/plans/`, `.omo/specs/`, audit reports, session-audit-report.md) that future sessions can reference.
- If identity sync discrepancy is found, it must be resolved before any identity/config change is finalized (per `.hermes.md` rules).
- Skills audit findings should feed into `.omo/plans/init-deep-plan.md` or a dedicated skills maintenance plan (`.omo/plans/skills-maintenance-plan.md`) if needed.

## References

- `.omo/plans/init-deep.md`: source reference for Django sub-project identity and conventions.
- `.omo/plans/hooks-plan.md`: cross-reference for verification sequence (`systematic-debugging` mandatory; deferred execution assumption documented).
- `docs/scope/scope.md`: existing scope; no destructive edit.
- Skills used: `engineer-args-kwargs`, `using-superpowers`, `brainstorming`, `user-communication-preferences`, `scope`, `architect`, `clarify-requirements`, `repo-planning-quick-commands`, `repo-init`, `readme-blueprint-generator`.
- MCP servers: `mcp-sequential-thinking`, `mcp-filesystem`, `mcp-ast-grep`, `mcp-memory`.
