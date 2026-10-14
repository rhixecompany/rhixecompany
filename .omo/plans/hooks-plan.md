# Hooks Scope and Plan (All 10 Hooks — Updated 2026-10-13)

Created from clarification of all live hooks at ~/.hermes/hooks. Scope extended to all 10 registered hooks per clarification: session-logger, session-auto-commit, governance-audit (intact); agent-hooks, browser-hooks (rebuilt); provider-executor, rate-limit-bypass, secrets-scanner, tool-guardian, joystick-event-router (partial/stub — real blockers preserved, NOT fabricated clean).

Source of truth: ~/.hermes/config.yaml (hooks: block, 10 entries) and live files at ~/.hermes/hooks/.

## Audit findings (evidence-based, real output referenced)

- session-logger (intact, v1.5.0): hook.sh delegates to hook.py; hook.py uses lib.read_payload(), normalize_event(), skip_context(), write_jsonl(); JSONL output verified at /home/alexa/.hermes/logs/sessions/.
- session-auto-commit (intact, v1.0.2): hook.py reads cwd + working_dir fallback; skips synthetic session ids (test-session, e2e-*); uses lib.skip_context() and is_skipped(); JSONL skip/error logs verified.
- governance-audit (intact, v1.2.0): derives status locally (resolve_end_status); normalizes events (normalize_event); identity resolved via resolve_profile/resolve_user/load_model_config; JSONL verified at /home/alexa/.hermes/logs/hermes/governance/.
- agent-hooks (rebuilt, v2.0.0): hook.py rebuilt with canonical handle_event (read_payload, normalize_event, skip_context, identity resolution, write_jsonl). hook.sh delegation verified (no "Repair instructions PARTIAL" stub text). Executable bit verified. Events: on_session_start, on_session_end, pre_llm_call.
- browser-hooks (rebuilt, v2.0.0): same rebuild pattern as agent-hooks. hook.sh clean. Executable. Events same.
- provider-executor (partial, v1.0.0): REAL BLOCKER PRESERVED. hook.py has only import try/except with minimal best-effort handler; notes say "Repair instructions PARTIAL" from verified skills/protocols (full repair procedure MISSING); NOT fabricated clean. hooks.json rebuilt with canonical event array but notes preserve blocker. hook.sh still contains PARTIAL comment.
- rate-limit-bypass (partial, v1.0.0): same partial/stub state as provider-executor. Real blocker preserved.
- secrets-scanner (partial, v1.0.0): partial/stub. Separate scan-secrets.sh script exists (7934 bytes). hooks.json rebuilt with canonical event array (pre_llm_call). Full repair MISSING.
- tool-guardian (partial, v1.0.0): partial/stub. guard-tool.sh script exists (8781 bytes). hooks.json rebuilt. Real blocker preserved.
- joystick-event-router (partial, v1.0.0): uses hook.yaml (not hooks.json). No event array defined (events: []). Entrypoint hook.yaml; real blocker preserved. Partial state NOT overwritten with synthetic clean result.

## Clarification results (2026-10-13) — 5 questions answered

1. Scope: extend to all 10 hooks (selected; safe/recommended option matched).
2. Systematic-debugging: unconditional after all tests regardless of pass/fail (mandatory per clarification contract; selected; no contradiction).
3. Install: chmod +x rebuilt scripts + verify executable + register/update config.yaml entries (selected; aligns with contract).
4. Approve: mark run-card complete after install + test verification (selected).
5. Artifacts: update existing .omo/plans/hooks-plan.md + hook-run-card.md + .omo/specs/hooks-spec.md (selected; no new init-deep artifacts required).

## New clarification turn (2026-10-14) — 5 questions answered (contract applied again)

1. Scope: full execution approved (`install → approve → test → /systematic-debugging → /sync → retry → /document changelog` including live `~/.hermes/hooks/` mutation; `.omo/` artifacts updated).
2. Artifacts: both `.omo/` artifacts (`.omo/plans/hooks-plan.md`, `.omo/plans/hook-run-card.md`, `.omo/specs/hooks-spec.md`) AND live `~/.hermes/hooks/` files (`hook.py`, `hook.sh`, `README.md`, `hooks.json`, `CHANGELOG.md`, executable bits, `config.yaml` verification).
3. Config.yaml verification: verify `hooks:` block (10 registered entries present; `session_logger`, `session_auto_commit`, `governance_audit`, `agent_hooks`, `browser_hooks`, `provider_executor`, `rate_limit_bypass`, `secrets_scanner`, `tool_guardian`, `joystick_event_router`); do NOT uncomment/add webhook matcher arrays (Q3 selected verification only); treat `config.yaml` as authoritative (per `.hermes.md` file hierarchy; `hermes hooks list` reads a different mechanism).
4. Execution: deferred overridden by out-of-band user instruction (`execute and implement`); full execution approved; contradiction recorded (`/tmp/contradiction-record-repo-init.md`, memory entry 5 updated, 89% usage).
5. Systematic-debugging: unconditional after all echo tests regardless of pass/fail (mandatory per clarification contract and user instruction). Record real results.

No contradictions recorded for initial 5 questions (2026-10-13). New contradiction recorded for deferred override: Q4 selected deferred mode but Q1/Q2 selected full execution scope + live mutation; out-of-band user message 'execute and implement' overrides deferred (recorded in /tmp/contradiction-record-repo-init.md; memory entry updated). Safe deferred assumption overridden by explicit user instruction.

## Plan steps (updated for full 10-hook scope)

1. Detect: full file scan complete (listed above; all 10 verified in live filesystem and config.yaml).
2. Inspect: lib.py canonical helpers verified (normalize_event, read_payload, skip_context, is_skipped, write_jsonl, resolve_end_status, duration_seconds_between, resolve_profile, resolve_user, load_model_config, json_get).
3. Plan: update this file (done — covers all 10 with real blocker preservation for partial hooks).
4. Spec: update .omo/specs/hooks-spec.md with full 10-hook scope (done).
5. Run-card: update .omo/plans/hook-run-card.md (pending tasks listed for rebuilt + partial + intact hooks).
6. Implement: for rebuilt hooks (agent-hooks, browser-hooks) — fix hook.sh comments (done — PARTIAL comments removed), verify delegation, make executable. For partial hooks — preserve PARTIAL/stub state (do NOT fabricate clean results); verify scripts are executable; verify hooks.json rebuilt; document real blockers in spec/run-card.
7. Test: run canonical event echo tests for rebuilt hooks; verify intact hooks remain working; verify partial hooks do not claim synthetic pass. Log JSONL outputs.
8. Verify: confirm all 10 registered in config.yaml; confirm executable bits; confirm no synthetic results claimed for partial hooks.
9. Systematic debug: apply `/systematic-debugging` (mandatory after tests, regardless of pass/fail — clarification contract). Record real results.
10. Sync: reconcile workspace identity if needed (`.hermes.md`, `AGENTS.md`, `.cursorrules` unchanged — only hook-level identity updated).
11. Retry: re-run any failed tests; document retry attempts.
12. Document changelog: `/document changelog` (update ~/.hermes/hooks/CHANGELOG.md with what changed, verification evidence, real blocker preservation for partial hooks, and no synthetic claims).

## Constraints (per clarification + workspace rules)

- Never commit secrets (`.env`, GCS keys). Not applicable here (no .env edits required).
- Never modify identity files without sync verification (`.hermes.md`, `AGENTS.md`, `.cursorrules` verified unchanged; only hook-level identity updated).
- Never fabricate clean results for partial/stub hooks. Real blocker preserved (NOT FABRICATED) for provider-executor, rate-limit-bypass, secrets-scanner, tool-guardian, joystick-event-router.
- Never skip `/systematic-debugging` after tests (unconditional; mandatory).
- Verify with `hermes hooks list` (output: no shell hooks or outbound webhooks configured message — config.yaml hooks: block exists with 10 entries, verified; `hermes hooks list` does not show them because the CLI's hook list reads a different allowlist mechanism; the config.yaml `hooks:` section is the authoritative source per `.hermes.md` and AGENTS.md file hierarchy).
