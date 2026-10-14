# profile — AGENTS.md (Updated 2026-10-13)

**Canonical reference:** Workspace identity files (`.hermes.md`, `.cursorrules`, `copilot-instructions.md`) and global profile skills library (`~/.hermes/skills/`). See also workspace-wide rules in workspace root documentation.

## OVERVIEW
Agent profile / identity configuration repository (`profile`). This workspace manages Hermes Agent identity, session startup sequences, provider configurations, context-file hierarchy precedence, and workspace-level agent rules. It also contains a Django blog/CMS sub-project (`base/` + `rhixecompany/`) that uses Google Cloud Storage (GCS) for media.

**Repo identity:** `profile` (Hermes agent profile workspace)  
**Workspace root:** `/mnt/c/Users/Alexa/playgrounds/profile`  
**Agent profile:** `default` (workspace-linked; verify with `hermes profile list`)  
**Stack (project):** Python 3.11+, Django 4.x, PostgreSQL, Gunicorn, WhiteNoise, CKEditor 5, GCS media storage.

## STRUCTURE (Agent Context + Project)
```
{root}/
├── AGENTS.md              # Workspace agent rules (this file)
├── .hermes.md             # Workspace agent identity (Hermes-specific; highest precedence)
├── .cursorrules           # Cursor IDE rules (derived from AGENTS.md + .hermes.md)
├── copilot-instructions.md  # Copilot / GitHub Copilot workspace instructions
├── docs/
│   └── ai-agents-inventory.md  # Agent platform inventory (repo-init output)
├── .omo/
│   ├── plans/
│   │   ├── base-agents.md            # Sub-app agent identity (base/ Django domain)
│   │   ├── init-deep.md              # Deep init plan (agent + project)
│   │   └── rhixecompany-agents.md   # Sub-app agent identity (rhixecompany/ config)
│   └── run-continuation/            # Continuation tracking
├── base/                  # Django domain (views, models, forms, signals)
│   └── AGENTS.md          # Sub-app agent identity
├── rhixecompany/          # Django config (settings, URLs, wsgi/asgi)
├── static/                # Static assets + CKEditor vendor files
├── templates/             # Django templates
├── .github/workflows/
│   └── ci.yml             # CI: ruff lint + Django tests
├── requirements.txt       # Python dependencies
├── package.json           # Bun package manager (`bun@1.3.14`); scripts: `lint` (ruff), `typecheck` (pyright), `check` (echo). No npm build.
└── manage.py              # Django entry point
```

## AGENT PROFILE CONFIGURATION (Per README.md)
Profiles managed by this workspace (verify with `hermes profile list` / `hermes config show`):
- `default` — workspace-linked (this repo is linked to `default` profile)
- `alexa` — personal assistant / user-aligned profile
- `code-architect` — architecture-focused agent
- `creative-director` — creative/content agent
- `exec-assistant` — executive/task management agent
- `patient-tutor` — tutoring/educational agent
- `research-analyst` — research/data analysis agent

Provider configurations (from README.md):
- `nous` — OAuth (device_code), default model `meituan/longcat-2.0:free`, vision/reasoning enabled, context 2000.
- `opencode-zen` — API Key + OAuth, default `nemotron-3-ultra-free`, context 2000.
- `openrouter` — API Key, default `nvidia/nemotron-3-ultra-550b-a55b:free`, context 2000.

## FILE HIERARCHY PRECEDENCE (Agent Identity — Per README.md + Workspace)
|| # | File | Purpose | Authority |
||---|------|---------|-----------|
|| 1 | `.hermes.md` | Workspace agent identity (Hermes-specific; highest precedence) | Highest — overrides all below |
|| 2 | `AGENTS.md` (this file) | Workspace agent rules + identity | This workspace |
|| 3 | `.cursorrules` | Cursor IDE rules | Cursor IDE only |
|| 4 | `copilot-instructions.md` | Copilot workspace instructions | Copilot workspace |
|| 5 | `base/AGENTS.md` | Sub-app agent identity (Django domain) | Sub-app identity |
|| 6 | `.omo/plans/*.md` | Agent init plans | Planning layer |

Note: `.hermes.md` and `AGENTS.md` should remain synchronized; `.hermes.md` takes precedence for Hermes-specific behavior, while `AGENTS.md` provides the broader workspace agent rules.

## KEY DOCUMENTATION (Agent + Project)
- **AGENTS.md** (this file): Workspace agent identity + rules.
- **.hermes.md**: Workspace agent identity (exists and verified 2026-10-13; includes profile linkage `default`, identity rules, session startup sequence, anti-patterns).
- **.cursorrules**: Cursor IDE rules (derived from AGENTS.md + .hermes.md).
- **copilot-instructions.md**: Copilot / GitHub Copilot workspace instructions.
- **README.md**: Profile definitions, provider config, session startup sequence, file hierarchy.
- **docs/ai-agents-inventory.md**: Agent platform inventory (`repo-init.py` output; verified 2026-10-13).
- **PLAN.md / SPEC.md / TECHNOLOGY_STACK.md / THE_STORY_OF_THIS_REPO.md**: Project architecture and history.
- **base/AGENTS.md**: Sub-app agent identity (Django domain logic).
- **.omo/plans/init-deep.md** / **base-agents.md** / **rhixecompany-agents.md**: Agent initialization plans.

## CONVENTIONS (Agent + Project — Verified)
- **Linting/Formatting:** `ruff` (line-length: 120, configured in `.ruff.toml`).
- **Style:** EditorConfig (`.editorconfig`) — 4 spaces `.py`, 2 spaces default (`[*]`), 2 spaces `.md`, `crlf` line endings (`.editorconfig`). Note: `.ruff.toml` enforces `lf` line endings for Python (`line-ending = "lf"`); run `ruff format .` to normalize.
- **Agent identity:** Never modify `.hermes.md` without confirming profile linkage (`hermes profile list`).
- **Sub-app identity:** Update `base/AGENTS.md` and `.omo/plans/*.md` when agent rules change.
- **Views:** Class-Based Views (CBVs) preferred (`base/views.py`, `rhixecompany/urls.py`).
- **Models:** `snake_case` fields, `PascalCase` classes (`base/models.py`).
- **Testing:** Django `TestCase` or `pytest` (see `.vscode/tasks.json` — configured tasks include Python tests, ruff check/format, mypy, markdownlint, cspell).
- **CI/CD:** `.github/workflows/ci.yml` — runs `ruff check .` and `python manage.py test`.
- **Agent skills:** Load `hermes-agent` (reference), `development` (verified structural placeholder), and workspace-relevant skills before making identity/config changes.

## COMMANDS (Agent + Development — Verified)
```bash
# Agent identity / profile
hermes profile list              # Verify workspace profile linkage
hermes profile switch default    # Confirm default profile active
hermes config show               # Verify agent configuration / identity
hermes --help                    # CLI reference

# Django development (sub-project)
python manage.py runserver       # Dev server
python manage.py migrate         # Database
python manage.py test            # Tests (requires Django env; see `myvenv/` or install via `pip install -r requirements.txt`)
python manage.py collectstatic --noinput  # Production static

# Lint / format / type check / docs
ruff check .                     # Lint (Python)
ruff format .                    # Format (Python)
bun run lint                     # `ruff check .` (package script)
bun run typecheck                # `pyright .` (package script — verified from package.json)
bun run check                    # Echo only (no JS build)
python -m mypy .                 # Type check (optional; requires `mypy` install)
python -m pytest                 # Tests (`.vscode/tasks.json` uses `python -m pytest`; `base/AGENTS.md` recommends `base/test_*.py` / `base/tests.py`)
markdownlint-cli2 --config .markdownlint-cli2.jsonc "**/*.md"  # Docs lint
python manage.py test            # Django tests (`.github/workflows/ci.yml`)
```

## ANTI-PATTERNS (Agent + Project — Enhanced)
- DO NOT commit secrets (`.env`, tokens, GCS credentials, API keys, `auth.json`).
- DO NOT use the README as a source of truth for agent architecture; agent identity lives in `.hermes.md`, `AGENTS.md`, `.cursorrules`, and `copilot-instructions.md`. The README describes profile configurations but is not canonical for agent identity rules.
- DO NOT use the README as a source of truth for Django architecture; see `base/AGENTS.md`, `TECHNOLOGY_STACK.md`, `SPEC.md`, and `.omo/plans/init-deep.md`.
- DO NOT add new JS dependencies; `package.json` uses `bun` (package manager `bun@1.3.14`) with minimal scripts (`lint`: `ruff check .`, `typecheck`: `pyright .`, `check`: echo). No npm build system exists; do not invent one.
- DO NOT edit `.env` directly or commit it; workspace `.env` is covered by `.gitignore`.
- DO NOT overwrite agent identity files (`AGENTS.md`, `.hermes.md`, `.cursorrules`) without verifying synchronization with profile settings (`hermes profile list`, `hermes config show`).
- DO NOT overwrite settings (`rhixecompany/settings.py`) without checking `rhixecompany/setting.py` (override file) first.
- DO NOT move original CKEditor vendor objects (`base/static/admin/`); clone them instead.
- DO NOT commit `.bak` files or untracked artifacts; `.gitignore` covers `.worktrees/`, `.env`, and build artifacts.
- DO NOT create agent identity/config changes without running verification (`ruff check .`, `python manage.py test` when Django environment is active, and identity sync check between `AGENTS.md` and `.hermes.md`).

## SESSION STARTUP SEQUENCE (Agent Identity — Enhanced Per README.md)
1. Read workspace session context: `AGENTS.md` (always), `.hermes.md` (if exists), `SESSION_REPORT.md` (if present).
2. Load mandatory agent identity skills:
   - `hermes-agent` (agent framework reference) — read `references/project-context-files.md` first for context-file rules.
   - `development` (verified structural placeholder in `~/.hermes/skills/development/`)
   - Workspace-relevant agent skills: `agent-analytics`, `agent-development`, `architect`, `audit`, `verify`, `development/check`.
3. Verify profile linkage: `hermes profile list` → confirm `default` (or target profile) matches workspace identity file (`.hermes.md`).
4. Confirm agent identity/file synchronization:
   - `.hermes.md` exists and is consistent with `AGENTS.md`.
   - `.cursorrules` references `.hermes.md` and `AGENTS.md` correctly.
   - `copilot-instructions.md` references workspace identity files.
   - `docs/ai-agents-inventory.md` is current (verify with `repo-init.py` or manual audit).
5. If any mandatory identity/config check fails → ABORT and report discrepancy with evidence (file paths, profile output, diff summary).

## ACTIVE AGENT CONTEXT FILE INVENTORY (Verified — Updated 2026-10-13)
The workspace agent identity is managed across multiple file formats. The inventory below reflects verified files (updated/confirmed this session) and planned files (to be created/enhanced).

### Hermes (Agent Framework — Primary)
| File / Source | Purpose | Status | Verification |
|---------------|---------|--------|--------------|
|| `.hermes.md` | Workspace agent identity (highest precedence) | **Verified 2026-10-13** | Exists; includes profile linkage `default`, identity rules, anti-patterns, session startup sequence, file hierarchy reference, references `.cursorrules` / `copilot-instructions.md` |
| `AGENTS.md` | Workspace agent rules (this file) | **Updated 2026-10-13** | Enhanced; verified against README.md |
| `.cursorrules` | Cursor IDE rules (derived) | **Updated** | Enhanced; references `.hermes.md` + `AGENTS.md` |
| `SOUL.md` (global: `~/.hermes/SOUL.md`) | Global system prompt / identity | **Verified** | Exists; aligns with Hermes Agent framework |
| Memory (`~/.hermes/memories/`) | Persistent memory (workspace-relevant) | **Empty** | Needs workspace memory entry |
| Skills (`~/.hermes/skills/`) | Installed agent capabilities | **Verified** | 50+ skills installed; `development` verified |

### Cursor (IDE)
| File / Source | Purpose | Status | Verification |
|---------------|---------|--------|--------------|
| `.cursorrules` | Cursor rules | **Updated** | Enhanced; references workspace identity files |

### Copilot / GitHub Copilot
| File / Source | Purpose | Status | Verification |
|---------------|---------|--------|--------------|
| `copilot-instructions.md` | Copilot workspace instructions | **Updated** | Enhanced; references `.hermes.md` + `AGENTS.md` |
| `.vscode/settings.json` | VS Code settings (includes agent-related extensions) | **Verified** | Contains `python-envs.alwaysUseUv`, ruff settings |

### Claude / Claude Code
| File / Source | Purpose | Status | Verification |
|---------------|---------|--------|--------------|
| `CLAUDE.md` | Claude-specific behavior | **Not present (planned)** | Should be created per file hierarchy |
| `base/AGENTS.md` | Sub-app Claude-aligned identity | **Verified** | Exists; aligns with workspace identity |

### OpenCode / Codex / GitHub CLI
Not applicable to this workspace profile repo (no specific agent identity files required). If needed in the future, create `opencode.md`, `codex.md`, or `.github/workflows/` extensions per README hierarchy.

### Agent Platform Inventory (docs/ai-agents-inventory.md)
Verified content reflects the workspace agent identity file count and platform mapping. The inventory table should remain synchronized with any new agent identity file creation (`.hermes.md`, `CLAUDE.md`, `MASTER_RULES.md`, etc.).

### Context File Counts (Workspace — Updated)
- Hermes: 7+ (`AGENTS.md`, `.hermes.md` [verified 2026-10-13], `.cursorrules`, `copilot-instructions.md`, `docs/ai-agents-inventory.md`, `base/AGENTS.md`, `.omo/plans/init-deep.md`) + installed skills + memory
- Cursor (`.cursorrules`): 2 files (AGENTS.md reference + .cursorrules rules)
- Copilot (`copilot-instructions.md`): 3 files (AGENTS.md, .hermes.md, .cursorrules references)
- Claude: 1 file planned (`CLAUDE.md`) + `base/AGENTS.md` reference
- OpenCode: 0
- Codex: 0
- GitHub CLI (`gh`): 0

## AGENT SKILLS (Workspace-Relevant — Verified 2026-10-13)
Installed skills in `~/.hermes/skills/` that apply directly to agent identity / profile work:
- `autonomous-ai-agents/hermes-agent` — Agent framework (reference only; load `references/project-context-files.md` before making identity changes).
- `development` — Development skill (verified structural placeholder; `SKILL.md` exists, status: `verified-structure`, audit session: `vscode-skill-audit-20260920`).
- `agent-analytics` — Agent analytics / session tracking.
- `agent-development` — Agent development skill set.
- `agentic-coder` — Coding agent skill (Turkish description; verified installed; applies to agent identity updates).
- `code-review` — Code review workflows (`code-rabbit-cli-mcp`).
- `architecture` / `architect` — Architecture documentation.
- `audit` / `verify` — Audit and verification skills (used for identity/file verification).
- `development/check` — Change verification before merge.

Verification method for skills: `skill_view(name='development')` confirmed structural placeholder; `ls ~/.hermes/skills/` confirms 50+ installed skills; `hermes-agent` skill references verified against workspace identity files.

## SESSION STARTUP SEQUENCE (Agent Identity — Detailed)
This sequence is derived from README.md session startup rules and enhanced for agent identity/config verification:

1. **Identity verification:**
   - Confirm workspace profile (`hermes profile list` → verify `default` or target profile).
   - Confirm `.hermes.md` exists and aligns with workspace identity (if missing → create/enhance before proceeding).

2. **Mandatory skill loading:**
   - Load `hermes-agent` (reference for agent framework rules, identity file hierarchy, context-file conventions).
   - Load `development` (verified structural placeholder — confirms repo-level identity files are structured correctly).
   - Load workspace-specific agent skills: `agent-analytics`, `agent-development`, `audit`, `verify`.

3. **File synchronization check:**
   - Verify `.hermes.md` content is consistent with `AGENTS.md` identity rules.
   - Verify `.cursorrules` references `.hermes.md` and `AGENTS.md`.
   - Verify `copilot-instructions.md` references workspace identity files.
   - Verify `docs/ai-agents-inventory.md` is current (re-run `repo-init.py` or manual audit if identity files change).

4. **Profile linkage confirmation:**
   - Confirm agent profile (`default`) matches workspace identity file (`.hermes.md`).
   - Confirm `.vscode/settings.json` agent-related settings align with workspace identity rules.

5. **Abort condition:**
   - If `.hermes.md` is missing and workspace identity is required for agent tasks → ABORT and create/enhance `.hermes.md` first.
   - If `.hermes.md` and `AGENTS.md` are out of sync → ABORT and report discrepancy with file paths, profile output, and diff summary.
   - If agent skills (`development`, `audit`, `verify`) are missing or fail to load → ABORT and report.

## AGENT IDENTITY / SYSTEM PROMPT SYNCHRONIZATION (Updated 2026-10-13)
The system prompt for this workspace is composed of three layers (per workspace file hierarchy):

1. **Global system prompt:** `~/.hermes/SOUL.md` (verified — Hermes Agent identity: "Be direct: match the length of your reply to the weight of the ask...").
2. **Workspace agent identity (highest precedence for workspace):** `.hermes.md` (exists and verified 2026-10-13 — includes profile linkage `default`, identity rules, session startup sequence, anti-patterns, file hierarchy reference, and references `.cursorrules` / `copilot-instructions.md`).
3. **Workspace agent rules:** `AGENTS.md` (this file — updated; serves as the broader agent identity reference, including file hierarchy, session startup sequence, anti-patterns, profile definitions, and verification status).

Synchronization rules:
- `.hermes.md` should reference `AGENTS.md` (not replace it; `.hermes.md` provides Hermes-specific identity rules, `AGENTS.md` provides workspace agent rules).
- `AGENTS.md` should reference `.hermes.md` (not replace it; confirms `.hermes.md` is the highest precedence workspace identity file).
- Both files should confirm profile linkage (`default`) and reference session startup sequence rules.
- `.cursorrules` and `copilot-instructions.md` should reference both `.hermes.md` and `AGENTS.md` (verified: `.cursorrules` references `../../AGENTS.md` and workspace identity; `copilot-instructions.md` references `../../AGENTS.md`, `.hermes.md`, `CLAUDE.md`).

Status: `.hermes.md` exists (verified 2026-10-13) and is synchronized with `AGENTS.md`. Identity synchronization is complete across `.hermes.md`, `AGENTS.md`, `.cursorrules`, `copilot-instructions.md`, `base/AGENTS.md`, `.omo/plans/*.md`, `docs/ai-agents-inventory.md`, and `SOUL.md` (global).

## VERIFICATION STATUS (Updated — 2026-10-13)
- [x] AGENTS.md — enhanced; verified against workspace identity rules, README.md file hierarchy, agent profile config, session startup sequence, anti-patterns, and documentation references.
- [x] `.cursorrules` — enhanced; verified references to `.hermes.md`, `AGENTS.md`, workspace identity, and Cursor IDE conventions.
- [x] `copilot-instructions.md` — enhanced; verified references to `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, workspace identity, and Copilot workspace instructions.
- [x] `docs/ai-agents-inventory.md` — verified; inventory reflects workspace agent identity files and platform mapping.
- [x] `base/AGENTS.md` — verified; aligns with workspace agent identity (`base/` Django domain sub-app).
- [x] `.omo/plans/*.md` — verified; plans reference workspace identity (`init-deep.md`, `base-agents.md`, `rhixecompany-agents.md`).
- [x] `.github/workflows/ci.yml` — verified; pipeline runs `ruff check .` and Django tests (requires active Django environment; see `myvenv/` or `pip install -r requirements.txt`).
- [x] `.vscode/settings.json` / `.vscode/tasks.json` — verified; includes agent-related settings (ruff, Python, Django file associations) and task configurations.
- [x] Global `SOUL.md` (`~/.hermes/SOUL.md`) — verified; aligns with Hermes Agent framework identity.
- [x] Global agent skills (`~/.hermes/skills/`) — verified; 50+ installed; `development` verified (structural placeholder); `hermes-agent` verified (framework reference).
- [x] `.hermes.md` (workspace agent identity) — exists and verified (2026-10-13); includes profile linkage `default`, identity rules, anti-patterns, session startup sequence, file hierarchy reference, and references `.cursorrules` / `copilot-instructions.md`.
- [ ] `PROJECT_RULES.md` — to be created (workspace rules layer).
- [ ] `MASTER_RULES.md` — to be created (universal agent rules layer).
- [ ] `CLAUDE.md` — to be created (Claude-specific agent identity layer).
- [ ] Memory (`~/.hermes/memories/`) — empty; needs workspace memory entry (agent identity / profile context).
- [ ] `.omo/run-continuation/` — verified; continuation tracking directory exists; content may need update based on agent identity verification results.
- [x] `.omo/plans/init-deep.md` — verified; references workspace identity rules; synchronized with `.hermes.md` (verified 2026-10-13).

## NEXT STEPS (Agent Identity Verification Pipeline)
1. Confirm `.hermes.md` remains synchronized with `AGENTS.md` (done — verified 2026-10-13).
2. Create/update `PROJECT_RULES.md`, `MASTER_RULES.md`, `CLAUDE.md` (optional but recommended per README file hierarchy).
3. Initialize/update workspace memory (`~/.hermes/memories/`) with agent identity / profile context entry.
4. Re-verify all identity files (`ruff check .` for code; identity sync check for agent files; `python manage.py test` when Django env is active).
5. Write/update verification report (`.omo/plans/init-deep.md` or new `VERIFICATION_REPORT.md`).
