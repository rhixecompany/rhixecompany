# profile — Project README

A Hermes profile configuration project managing agent identities, permissions, and session state across multiple environments.

## Overview

This project centralizes Hermes Agent profile settings including:

- **Profile definitions**: default, alexa, code-architect, creative-director, exec-assistant, patient-tutor, research-analyst
- **Provider configurations**: nous, opencode-zen, openrouter with auth models and context limits
- **Session startup sequences**: mandatory skill loading and verification
- **File hierarchy precedence**: `$HERMES_HOME.md` > `AGENTS.md` > `PROJECT_RULES.md` > `MASTER_RULES.md`

## Profile Configuration

| Profile | Model / Guidance |
|---------|-----------------|
| **default** | Verify with `hermes profile list` / `hermes config show` |
| alexa | Verify with `hermes profile list` / `hermes config show` |
| code-architect | Verify with `hermes profile list` / `hermes config show` |
| creative-director | Verify with `hermes profile list` / `hermes config show` |
| exec-assistant | Verify with `hermes profile list` / `hermes config show` |
| patient-tutor | Verify with `hermes profile list` / `hermes config show` |
| research-analyst | Verify with `hermes profile list` / `hermes config show` |

## Provider Configuration

| Provider | Auth Method | Default Model | Vision | Reasoning | Context |
|----------|-------------|---------------|--------|-----------|---------|
| **nous** | OAuth (device_code) | meituan/longcat-2.0:free | yes | yes | 2000 |
| **opencode-zen** | API Key + OAuth | nemotron-3-ultra-free | yes | yes | 2000 |
| **openrouter** | API Key | nvidia/nemotron-3-ultra-550b-a55b:free | yes | yes | 2000 |

## Session Startup Sequence

```bash
1. Read SESSION_REPORT.md (workspace root) — last session summary

2. Load mandatory skills:
  - using-superpowers (foundational workflow)
  - user-communication-preferences (safety constraints)
  - session-audit-report (session analysis)
  - hermes-profiles (profile management)
  - validate-memories (memory verification)

3. Review ./SESSION_REPORT.md for session context

4. If any mandatory skill fails → ABORT and report
```

## File Hierarchy (Precedence Order)

| # | File | Purpose | Authority |
|---|------|---------|-----------|
| 1 | `$HERMES_HOME.md` | Hermes-specific overrides | Highest — overrides all below |
| 2 | `AGENTS.md` | General agent guidance | This file |
| 3 | `PROJECT_RULES.md` | Workspace-level rules | Rules |
| 4 | `MASTER_RULES.md` | Universal agent rules | Cross-project rules |
| 5 | `CLAUDE.md` | Claude-specific behavior | Copilot/Claude only |
| 6 | `.cursorrules` | Cursor IDE rules | Cursor IDE only |

## Available Hermes Toolsets (16)

`web`, `browser`, `terminal`, `file`, `code_execution`, `vision`, `image_gen`, `tts`, `skills`, `todo`, `memory`, `context_engine`, `session_search`, `clarify`, `delegation`, `cronjob`

## Active Hooks (3)

`session-logger` | `session-auto-commit` | `governance-audit`

## Safety Rules

1. **Never commit secrets** — `.env`, tokens, credentials
2. **No destructive ops without approval** — explain risks first
3. **Verify before claim** — test, check, confirm before reporting
4. **MCP-first** — use MCP servers over native tools where available
5. **Profile per task** — switch profile before execution
6. **Strict sequential** — "only then" is a hard constraint

## Quick Start

```bash
# From workspace root
cd C:/Users/Alexa/Desktop/SandBox

# List available profiles
hermes profile list

# Set active profile
hermes profile switch default

# Verify configuration
hermes config show
```
