# Copilot Instructions — profile workspace (Updated 2026-10-13)

**Workspace identity:** `profile` (Hermes agent profile / identity management repo)  
**Agent profile:** `default` (workspace-linked)  
**Workspace identity file hierarchy:**
1. `.hermes.md` (highest precedence — Hermes-specific workspace agent identity; created/enhanced 2026-10-13).
2. `AGENTS.md` (workspace agent rules — enhanced 2026-10-13; broader agent identity context).
3. `.cursorrules` (Cursor IDE rules — enhanced 2026-10-13; derived from `.hermes.md` + `AGENTS.md`).
4. `CLAUDE.md` (planned — Claude-specific agent identity; not yet created in this workspace).
5. Sub-app identity: `base/AGENTS.md` (Django domain identity — verified; aligns with workspace identity).
6. Initialization plans: `.omo/plans/init-deep.md`, `.omo/plans/base-agents.md`, `.omo/plans/rhixecompany-agents.md` (verified; reference workspace identity rules).
7. Agent inventory: `docs/ai-agents-inventory.md` (verified — reflects workspace agent identity files).

---

## Workspace Agent Identity (Quick Reference)

This workspace (`profile`) manages agent identity for Hermes Agent (`hermes`). Key identity files:

- `.hermes.md` — Workspace agent identity (Hermes-specific). Confirm profile linkage (`default`) with `hermes profile list`. Verify identity rules align with `AGENTS.md`. Must exist before identity/config updates.
- `AGENTS.md` — Workspace agent rules (broader identity context). Confirm identity rules, conventions (`ruff` line length 120, EditorConfig 4 spaces, CBVs, `snake_case` fields), anti-patterns (secrets, README misuse, npm, identity sync, settings override, vendor files, verification skip), profile definitions (`default`, `alexa`, `code-architect`, `creative-director`, `exec-assistant`, `patient-tutor`, `research-analyst`), provider configurations (`nous`, `opencode-zen`, `openrouter`), session startup sequence, file hierarchy, and verification checklist.
- `.cursorrules` — Cursor IDE rules (derived from `.hermes.md` + `AGENTS.md`). Confirm references `.hermes.md` + `AGENTS.md` correctly. Confirm code style rules match workspace conventions (4-space Python, 120-char ruff, no `any`, no backup files, no `.env` writes).

---

## Copilot Workspace Quick Start

```bash
# Verify agent identity / profile linkage (always do this first for agent identity/config tasks)
hermes profile list              # Confirm `default` profile is active (workspace-linked to `profile` repo)
hermes config show               # Confirm agent config aligns with workspace identity (`.hermes.md` + `AGENTS.md`)

# Load agent skills (before identity/config updates)
# Load `hermes-agent` skill: references/project-context-files.md (agent framework rules, identity file hierarchy)
# Load `development` skill: structural placeholder (verified); applies to workspace identity updates
# Load `audit` and `verify` skills: identity verification and audit workflows

# Verify workspace identity synchronization (before making identity/config changes)
# Confirm `.hermes.md` exists and aligns with `AGENTS.md`
# Confirm `.cursorrules` references `.hermes.md` + `AGENTS.md`
# Confirm `copilot-instructions.md` (this file) references `.hermes.md` + `AGENTS.md` + planned `CLAUDE.md`
# Confirm `docs/ai-agents-inventory.md` is current
# Confirm `base/AGENTS.md` aligns with workspace identity
# Confirm `.omo/plans/*.md` aligns with identity rules
# Confirm `.github/workflows/ci.yml` verifies identity changes indirectly (lint + tests)
# Confirm `SOUL.md` (global: `~/.hermes/SOUL.md`) aligns with workspace identity (global identity should not conflict with workspace identity; `.hermes.md` provides workspace-specific overrides only)

# Django sub-project commands (if working with Django domain / config)
python manage.py runserver       # Dev server (requires active Django environment; see `myvenv/` or `pip install -r requirements.txt`)
python manage.py migrate         # Database migrations
python manage.py test            # Django tests (requires Django env active)
python manage.py collectstatic --noinput  # Production static collection

# Lint / format / verification (always verify after identity/config updates)
ruff check .                     # Lint (verified: `.ruff.toml` line length 120; `ruff` installed globally or in venv; `.github/workflows/ci.yml` verifies lint + tests)
ruff format .                    # Format
python -m mypy .                 # Type check (optional; `.vscode/tasks.json` includes `mypy .` task)
```

---

## Workspace Rules (Agent Identity / Project)

All conventions, workflows, agent identity rules, file hierarchy rules (`.hermes.md` > `AGENTS.md` > `.cursorrules` > `copilot-instructions.md` > sub-app identity), profile linkage rules (`default`), session startup sequence rules, anti-patterns (secrets, README misuse, npm dependencies, identity sync skip, settings override without override check, vendor file overwrite, verification skip after identity/config updates), and identity verification checklist rules are in:

- `.hermes.md` (highest precedence workspace agent identity file — created/enhanced 2026-10-13; must reference profile linkage `default`, agent framework `hermes-agent`, agent skills `development`/`audit`/`verify`, file hierarchy, session startup sequence, anti-patterns, identity synchronization rules, and verification checklist).
- `AGENTS.md` (enhanced 2026-10-13; must reference `.hermes.md`, profile linkage `default`, agent framework `hermes-agent`, agent skills `development`/`audit`/`verify`, file hierarchy, session startup sequence, anti-patterns, identity synchronization rules, verification checklist, profile definitions, provider configurations, conventions, and verification status).
- `.cursorrules` (enhanced 2026-10-13; must reference `.hermes.md` + `AGENTS.md`, confirm profile linkage rules, confirm identity synchronization rules, confirm code style rules match workspace conventions).

Additionally:
- `base/AGENTS.md` — Sub-app agent identity (Django domain; verified 2026-10-13; aligns with workspace identity).
- `.omo/plans/init-deep.md` — Deep initialization plan (agent + project identity; verified; references workspace identity rules; should be updated if identity rules change significantly).
- `.omo/plans/base-agents.md` — Sub-app agent identity plan (`base/` Django domain; verified).
- `.omo/plans/rhixecompany-agents.md` — Sub-app agent identity plan (`rhixecompany/` Django config; verified).
- `docs/ai-agents-inventory.md` — Agent inventory (verified; reflects workspace agent identity file count and platform mapping; should be re-verified if identity files change).
- `.vscode/settings.json` — VS Code agent-related settings (ruff, Python, Django file associations; verified; should remain consistent with workspace identity conventions).
- `.vscode/tasks.json` — VS Code tasks (lint, test, format, type check, docs lint, spell check; verified).
- `.github/workflows/ci.yml` — CI pipeline (lint + Django tests; verified; identity verification is manual/skill-assisted, not automated in CI).

---

## Agent Identity / Config Change Protocol

For any agent identity/config update in this workspace:

1. Confirm workspace identity file (`.hermes.md`) exists and aligns with `AGENTS.md`.
2. Confirm profile linkage (`default`) matches workspace identity (`hermes profile list`).
3. Confirm identity synchronization rules are followed (`.hermes.md` updated first; `AGENTS.md` updated second; `.cursorrules` updated third; `copilot-instructions.md` updated fourth; sub-app identity and init plans updated; inventory verified).
4. Confirm agent skills (`hermes-agent`, `development`, `audit`, `verify`) are loaded/referenced.
5. Confirm verification is performed (`ruff check .` for lint; identity sync verification; `python manage.py test` for Django domain when Django env active; profile linkage verification; `.vscode/settings.json` consistency check; `.omo/plans/init-deep.md` or dedicated verification report updated).
6. Confirm anti-patterns are not violated (no secrets committed; README not used as identity truth; npm dependencies not added; `.env` not edited/committed; Django settings override checked; vendor files not overwritten; identity verification not skipped).

---

*These Copilot workspace instructions (`copilot-instructions.md`) are derived from the workspace agent identity file (`.hermes.md` — enhanced 2026-10-13) and workspace agent rules (`AGENTS.md` — enhanced 2026-10-13). They are verified against workspace identity conventions: profile linkage (`default`), agent framework (`hermes-agent`), agent skills (`development` verified structural placeholder; `audit` / `verify` for identity verification), file hierarchy (`.hermes.md` > `AGENTS.md` > `.cursorrules` > `copilot-instructions.md` > sub-app identity > init plans > inventory), anti-patterns (secrets, README misuse, npm dependencies, identity sync skip, settings override without check, vendor file overwrite, verification skip), and identity synchronization rules. Any discrepancy between `copilot-instructions.md` and workspace identity files (`.hermes.md`, `AGENTS.md`, `.cursorrules`) should be reported as an identity synchronization failure and resolved before making agent identity/config changes.*
