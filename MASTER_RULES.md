# MASTER_RULES.md — Universal Agent Rules (Updated 2026-10-13)

**Workspace identity:** `profile` (Hermes agent profile management repo)  
**Agent profile:** `default` (workspace-linked)  
**Universal scope:** These rules apply across all agent identity/config work in this workspace (`profile`) and can be referenced by any agent profile (`default`, `alexa`, `code-architect`, `creative-director`, `exec-assistant`, `patient-tutor`, `research-analyst`) or any workspace/project that uses the Hermes Agent framework (`~/hermes-agent/nousresearch/docs/project-context-files.md` or load `hermes-agent` skill).

---

## Universal Agent Identity / Config Rules (Cross-Project / Cross-Profile)

These rules are derived from the workspace agent identity file (`.hermes.md`) and workspace agent rules (`AGENTS.md`) but apply universally to any agent identity/config work in this workspace or any workspace/project that uses Hermes Agent identity conventions.

### Agent Framework Rules (Universal)
- Agent framework: Hermes Agent (built by Nous Research; global identity: `~/.hermes/SOUL.md`).
- Agent identity file hierarchy (universal): Workspace identity file (`.hermes.md` or equivalent workspace identity file) > workspace agent rules (`AGENTS.md` or equivalent) > workspace IDE rules (`.cursorrules` or equivalent) > workspace Copilot instructions (`copilot-instructions.md` or equivalent) > sub-app identity files (`base/AGENTS.md` or equivalent sub-app identity) > initialization plans (`.omo/plans/*.md` or equivalent init plans) > agent inventory (`docs/ai-agents-inventory.md` or equivalent inventory).
- Agent profile linkage: Confirm profile linkage (`hermes profile list`) matches workspace identity before making identity/config changes. If profile linkage does not match workspace identity (`default` profile not linked to `profile` workspace, or target profile does not match identity file reference), report discrepancy and resolve before proceeding.
- Agent identity file synchronization: Update workspace identity file first; confirm synchronization with broader agent rules; confirm synchronization with IDE rules; confirm synchronization with Copilot instructions; confirm sub-app identity synchronization; confirm init plan synchronization; confirm inventory synchronization; confirm memory synchronization; confirm CI pipeline consistency; confirm `.vscode/settings.json` consistency; confirm verification report is updated.
- Agent identity verification: Confirm agent identity file exists (`.hermes.md`); confirm identity rules align (`.hermes.md` content matches identity rules in `.hermes.md` — self-consistency — and aligns with `AGENTS.md`); confirm profile linkage; confirm agent skills (`hermes-agent`, `development`, `audit`, `verify`) are loaded/referenced; confirm anti-patterns are not violated (secrets, README misuse, npm dependencies, identity sync skip, settings override without check, vendor file overwrite, verification skip); confirm verification is performed (`ruff check .`; identity sync verification; `python manage.py test` for Django domain when Django env active; profile linkage verification; `.vscode/settings.json` consistency check; verification report updated).
- Agent skills (universal): Load `hermes-agent` skill (agent framework reference; `references/project-context-files.md` for identity file rules); load `development` skill (verified structural placeholder — applies to workspace identity updates); load `audit` / `verify` skills (identity verification and audit workflows).
- Agent anti-patterns (universal): Never commit secrets (`.env`, tokens, API keys, GCS credentials, `auth.json`); never use README as identity truth (`.hermes.md` + `AGENTS.md` are canonical); never add npm dependencies (if `package.json` has no JS tooling — verified in this workspace); never edit `.env` or commit it; never modify identity files without synchronization verification; never skip identity verification after identity/config updates; never overwrite original vendor files (clone only); never use identity rules that conflict with workspace identity (`.hermes.md` and `AGENTS.md` must remain synchronized).

### Agent Profile Definitions (Universal — From Workspace `AGENTS.md`)
Profiles managed by this workspace (`profile` workspace) — verified (`README.md` defines profiles; `AGENTS.md` references them; `.hermes.md` references `default`; profile identity rules apply to all profiles):
- `default` — workspace-linked profile (primary identity profile for `profile` workspace).
- `alexa` — personal assistant / user-aligned profile.
- `code-architect` — architecture-focused agent profile.
- `creative-director` — creative/content agent profile.
- `exec-assistant` — executive/task management agent profile.
- `patient-tutor` — tutoring/educational agent profile.
- `research-analyst` — research/data analysis agent profile.

Profile linkage verification (universal): Before identity/config updates, confirm `hermes profile list` shows the target profile (`default` for workspace identity work; target profile for profile-specific identity work). Confirm `.hermes.md` references the correct profile. Confirm `AGENTS.md` references the correct profile. Confirm `.cursorrules` references profile linkage rules. Confirm `copilot-instructions.md` references profile linkage rules.

### Agent Provider Configurations (Universal — From Workspace `README.md` + `AGENTS.md`)
Provider configurations verified in workspace identity (`.hermes.md` + `AGENTS.md` + `README.md`):
- `nous` — OAuth (device_code); default model `meituan/longcat-2.0:free`; vision/reasoning enabled; context 2000.
- `opencode-zen` — API Key + OAuth; default `nemotron-3-ultra-free`; context 2000.
- `openrouter` — API Key; default `nvidia/nemotron-3-ultra-550b-a55b:free`; context 2000.

Provider identity rules: Provider configurations are part of agent profile identity (`README.md` defines them; `.hermes.md` and `AGENTS.md` reference them; profile linkage rules apply to provider selection — confirm profile (`default`) matches provider configuration before making identity/config updates that affect provider settings).

---

## Universal Verification Checklist (Cross-Project / Cross-Profile)

Before completing any agent identity/config update (in this workspace `profile` or any workspace/project using Hermes Agent identity conventions):

- [ ] Workspace identity file (`.hermes.md` or equivalent) exists and aligns with workspace identity rules.
- [ ] Broader agent rules (`AGENTS.md` or equivalent) exist and align with workspace identity file.
- [ ] Profile linkage (`default` or target profile) matches workspace identity and is verified (`hermes profile list`).
- [ ] Agent skills (`hermes-agent`, `development`, `audit`, `verify`) are loaded/referenced.
- [ ] Identity synchronization rules are followed (`.hermes.md` updated first; broader rules second; IDE rules third; Copilot instructions fourth; sub-app identity fifth; init plans sixth; inventory seventh; memory eighth; CI pipeline ninth; `.vscode/settings.json` tenth; verification report eleventh).
- [ ] Anti-patterns are not violated (no secrets committed; README not used as identity truth; npm dependencies not added; `.env` not edited/committed; identity files not overwritten without sync verification; verification not skipped; vendor files not overwritten; identity rules synchronized).
- [ ] Verification is performed (`ruff check .` for lint; identity sync verification; `python manage.py test` for Django domain when Django env active; profile linkage verification; `.vscode/settings.json` consistency check; verification report updated; `.omo/plans/init-deep.md` or dedicated verification file updated).
- [ ] Memory (`~/.hermes/memories/` or equivalent workspace memory) is initialized/updated with agent identity / profile context (if memory is part of identity/config work).
- [ ] Agent identity/config changes include verification note (either in `.omo/plans/init-deep.md` or dedicated verification file) describing what changed, what's verified, what's missing, profile linkage status, identity synchronization status, anti-pattern compliance status, and remaining tasks.

---

*These universal agent rules (`MASTER_RULES.md`) are derived from the workspace agent identity file (`.hermes.md` — created/enhanced 2026-10-13) and workspace agent rules (`AGENTS.md` — enhanced 2026-10-13). They apply across all agent profiles (`default`, `alexa`, `code-architect`, `creative-director`, `exec-assistant`, `patient-tutor`, `research-analyst`) and any workspace/project that uses Hermes Agent identity conventions. They must remain synchronized with workspace identity (`.hermes.md`) and workspace agent rules (`AGENTS.md`); any discrepancy should be reported as an identity synchronization failure and resolved before making agent identity/config changes in this workspace or any workspace/project using Hermes Agent identity conventions.*
