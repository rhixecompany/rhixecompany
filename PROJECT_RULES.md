# PROJECT_RULES.md — Workspace Agent Rules Layer (Updated 2026-10-13)

**Workspace identity:** `profile` (Hermes agent profile management repo)  
**Agent profile:** `default` (workspace-linked)  
**File hierarchy precedence:** `.hermes.md` (highest) > `AGENTS.md` (broader) > `PROJECT_RULES.md` (rules) > `MASTER_RULES.md` (universal) > `.cursorrules` (IDE) > `copilot-instructions.md` (Copilot) > sub-app identity (`base/AGENTS.md`) > init plans (`.omo/plans/`) > inventory (`docs/ai-agents-inventory.md`).

---

## Workspace Agent Rules (Project-Level)

These rules apply specifically to agent identity/config updates, Django sub-project work (`base/` + `rhixecompany/`), documentation updates (`docs/`), initialization plan updates (`.omo/plans/`), and CI pipeline updates (`.github/workflows/`) within the `profile` workspace.

### Agent Identity / Config Rules (Project Level)
- Agent identity updates must reference `.hermes.md` (workspace agent identity) and `AGENTS.md` (broader agent rules) before making changes.
- Profile linkage (`default`) must be confirmed (`hermes profile list`) before identity/config updates in this workspace.
- Agent identity file synchronization is mandatory across `.hermes.md`, `AGENTS.md`, `.cursorrules`, `copilot-instructions.md`, `base/AGENTS.md`, `.omo/plans/*.md`, and `docs/ai-agents-inventory.md`.
- Agent skills (`hermes-agent` framework reference; `development` structural placeholder — verified; `audit` / `verify` for identity verification) must be loaded/referenced before identity/config updates.
- Verification must be performed after identity/config updates (`ruff check .` for lint; identity sync verification; `python manage.py test` for Django domain when Django env active; profile linkage verification; `.vscode/settings.json` consistency check; `.omo/plans/init-deep.md` or dedicated verification report updated).

### Django Sub-Project Rules (Project Level)
- All Django domain logic lives in `base/` (models, views, forms, signals, filters) — verified (`base/AGENTS.md` confirms this; `base/models.py`, `base/views.py`, `base/forms.py`, `base/decorators.py`, `base/filters.py` exist and are part of Django app).
- All Django configuration lives in `rhixecompany/` (settings, URLs, wsgi, asgi) — verified (`rhixecompany/settings.py` is canonical; `rhixecompany/setting.py` is override; `rhixecompany/urls.py` handles root routing).
- Settings override (`rhixecompany/setting.py`) must be checked before editing `rhixecompany/settings.py` — verified (`.hermes.md` references this anti-pattern; `.cursorrules` confirms it; `AGENTS.md` includes it).
- Original CKEditor vendor objects in `base/static/admin/` and `base/static/ckeditor/` must not be overwritten (clone instead) — verified (`.gitignore` protects original vendor files; `.cursorrules` confirms clone-only rule).
- `manage.py` is the Django entry point — verified (`manage.py` exists; `.vscode/launch.json` includes `Python: Current File` using `manage.py` or `.venv`; `.vscode/tasks.json` includes `Python: Test All` using `python -m pytest` and `Python: Lint (ruff)` using `ruff check .`).

### Agent Identity / Config Anti-Patterns (Project Level — Enhanced from AGENTS.md)
- Never commit secrets (`.env`, tokens, GCS keys, API credentials) — verified (`.gitignore` includes `.env`; `.hermes.md` and `.cursorrules` confirm anti-pattern).
- Never use README as source of truth for agent architecture or identity rules — `.hermes.md` and `AGENTS.md` are canonical (`README.md` describes profiles but is not identity truth).
- Never use README as source of truth for Django architecture (`TECHNOLOGY_STACK.md`, `SPEC.md`, `.omo/plans/init-deep.md` are architecture truth).
- Never add npm dependencies (`package.json` has no JS tooling — no scripts, dependencies, or build tools) — verified (`package.json` content confirmed; `.vscode/settings.json` references TypeScript/JavaScript settings but these are not actively used for Django project).
- Never edit `.env` or commit it — `.env` is `.gitignore`-protected; workspace `.env` must not be edited without verification (`.hermes.md` confirms).
- Never modify agent identity files without synchronization verification (`.hermes.md` updated first; `AGENTS.md` second; `.cursorrules` third; `copilot-instructions.md` fourth; sub-app identity and init plans updated; inventory verified; memory updated; verification report written/updated).
- Never skip identity verification after agent identity/config changes (`ruff check .`; identity sync check; `python manage.py test` when Django env active; profile linkage verification with `hermes profile list`; `.vscode/settings.json` consistency check).

---

*These project-level rules (`PROJECT_RULES.md`) are derived from workspace agent identity (`.hermes.md` — created/enhanced 2026-10-13) and workspace agent rules (`AGENTS.md` — enhanced 2026-10-13). They apply specifically to agent identity/config updates, Django sub-project work (`base/` + `rhixecompany/`), documentation updates (`docs/`), initialization plan updates (`.omo/plans/`), CI pipeline updates (`.github/workflows/`), and workspace identity verification within the `profile` workspace. They must remain synchronized with `.hermes.md` and `AGENTS.md`; any discrepancy should be reported as an identity synchronization failure and resolved before making agent identity/config changes in this workspace.*
