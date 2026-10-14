# Session Plan: Full Implementation + Skills Audit + Session Audit (2027-01-01)

**Status:** Running  
**Created:** 2027-01-01  
**Assignee:** Default agent (code-architect / adminbot as needed)  
**Profile:** default  
**Plan reference:** `.omo/plans/init-deep-plan.md` (updated)  

## Clarification (completed — 4 questions answered)

1. All phases sequential? → Yes (plan → skills audit → session audit)
2. Create/update artifacts? → Yes, in docs/ and .omo/
3. Skills audit scope? → Categories mentioned (development, agentic-coder, planning, architecture) plus related inventory
4. Session audit? → Yes, generate session-audit-report.md

## Objectives

1. Update `.omo/plans/init-deep-plan.md` and `.omo/plans/init-deep-run-card.md`
2. Create/update `.omo/specs/init-spec.md` (reference `.omo/plans/init-deep.md` and include requirements/acceptance/non-goals/constraints)
3. Update `docs/scope/scope.md` (if needed; keep existing feature table intact, add session reference)
4. Apply `engineer-args-kwargs` skill: inspect args/config, verify `scripts/normalize_args_kwargs.py`, run checklist
5. Search/triage/audit skills in mentioned categories; create audit reports per category
6. Apply `hermes skills --help` + `/skill-judge` to updated skills in batches
7. Run `/session-audit` and generate `.omo/plans/session-audit-report.md` or `docs/scope/session-audit-report.md`

## Execution sequence

| Step | Action | Artifact / Evidence | Status |
|---|---|---|---|
| 1 | Read existing `.omo/` artifacts and `docs/scope/scope.md` | Read outputs saved | Done |
| 2 | Update `.omo/plans/init-deep-plan.md` | Updated file | In progress |
| 3 | Create `.omo/plans/session-plan.md` (this file) | This file | Done |
| 4 | Create/update `.omo/plans/session-run-card.md` | Run card file | In progress |
| 5 | Create/update `.omo/specs/session-spec.md` | Spec file | Planned |
| 6 | Apply `engineer-args-kwargs` verification | `scripts/normalize_args_kwargs.py` + checklist | Planned |
| 7 | Skills audit (search, list, audit reports) | `docs/inventory/` audit reports | Planned |
| 8 | Skill validation (`hermes skills --help`, `skill-judge`) | Batch reports | Planned |
| 9 | Session audit (`/session-audit`) + `session-audit-report.md` | Audit report | Planned |

## References
- `.hermes.md` (workspace identity)
- `AGENTS.md` (agent rules)
- `.omo/plans/init-deep.md` (source reference)
- `.omo/plans/hooks-plan.md` (cross-reference for verification sequence)
- `docs/scope/scope.md` (existing scope)
- Skills: `engineer-args-kwargs`, `using-superpowers`, `brainstorming`, `user-communication-preferences`, `scope`, `architect`, `clarify-requirements`
- MCP: `mcp-sequential-thinking`, `mcp-filesystem`, `mcp-ast-grep`, `mcp-memory`
