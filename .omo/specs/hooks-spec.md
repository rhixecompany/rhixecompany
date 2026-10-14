# Hooks Implementation Spec (All 10 Hooks — Updated 2026-10-13)

## Goal

Cover all 10 registered hooks in `~/.hermes/config.yaml` (hooks: block). Rebuilt hooks (agent-hooks, browser-hooks) must use canonical `lib.py` patterns. Intact hooks (session-logger, session-auto-commit, governance-audit) must remain verified. Partial/stub hooks (provider-executor, rate-limit-bypass, secrets-scanner, tool-guardian, joystick-event-router) must have their real blocker state preserved (NOT fabricated clean) — full repair procedure MISSING from verified skills/protocols; notes and `hook.sh` comments retain "PARTIAL" / real blocker language.

Verify executable bits, config.yaml registration, canonical event arrays, and that no synthetic clean results are produced for partial hooks.

## Scope

All scripts and markdown files under `~/.hermes/hooks/`. All 10 hooks:

1. session-logger (intact)
2. session-auto-commit (intact)
3. governance-audit (intact)
4. agent-hooks (rebuilt)
5. browser-hooks (rebuilt)
6. provider-executor (partial — real blocker)
7. rate-limit-bypass (partial — real blocker)
8. secrets-scanner (partial — real blocker; scan-secrets.sh present)
9. tool-guardian (partial — real blocker; guard-tool.sh present)
10. joystick-event-router (partial — hook.yaml entrypoint, no event array; real blocker)

## Inputs (evidence-based)

- `.omo/plans/hooks-plan.md` — full audit findings for all 10 hooks (updated with clarification results and real blocker preservation).
- `.omo/plans/hook-run-card.md` — pending/completed tasks (updated below).
- `~/.hermes/hooks/lib.py` — canonical helpers (`normalize_event`, `read_payload`, `skip_context`, `is_skipped`, `write_jsonl`, `resolve_end_status`, `duration_seconds_between`, `resolve_profile`, `resolve_user`, `load_model_config`, `json_get`, `now_iso`, `log_info`, `log_debug`).
- `~/.hermes/config.yaml` — hooks: block with 10 entries (verified with yaml.safe_load).
- `~/.hermes/hooks/CHANGELOG.md` — previous audit/repair notes (updated at end of this spec execution).

## Clarification results (2026-10-13 — 5 questions, no contradictions)

- Scope: all 10 hooks (safe/recommended selected; matches full config.yaml inventory).
- Systematic-debugging: unconditional after all tests regardless of pass/fail (mandatory; selected; aligns with contract; no contradiction to record).
- Install: `chmod +x` rebuilt scripts + verify executable bits + register/update `config.yaml` entries (selected).
- Approve: mark run-card complete after install + test verification (selected).
- Artifacts: update existing `.omo/plans/hooks-plan.md` + `.omo/plans/hook-run-card.md` + `.omo/specs/hooks-spec.md` (selected; no new init-deep artifacts required).

No contradiction file needed (`/tmp/contradiction-record-[project].md` not created — user selected safe/recommended options consistently; no conflict with safer conditional alternatives).

## Implementation steps (in order — full 10-hook scope)

1. Update `.omo/plans/hooks-plan.md` (completed — covers all 10 with real blocker preservation for partial hooks).
2. Update `.omo/specs/hooks-spec.md` (this file — completed — full 10-hook scope).
3. Update `.omo/plans/hook-run-card.md` (pending/completed tasks for rebuilt + intact + partial hooks — done below).
4. Verify rebuilt hooks:
   - agent-hooks `hook.py` uses `lib.py` (`normalize_event`, `read_payload`, `skip_context`, `resolve_profile`, `resolve_user`, `load_model_config`, `write_jsonl`).
   - browser-hooks `hook.py` uses same `lib.py` helpers.
   - Both `hook.sh` have no "Repair instructions PARTIAL" stub text (verified — cleaned 2026-10-13).
5. Verify rebuilt hooks executable (`chmod +x`) and config.yaml entries present.
6. For partial hooks — verify real blocker state preserved (DO NOT fabricate clean results):
   - `hook.py` retains PARTIAL/stub import structure (only minimal best-effort handler, not synthetic full handler).
   - `hooks.json` notes retain "Repair instructions PARTIAL" and "NOT FABRICATED clean result" language.
   - `hook.sh` comments retain "Repair instructions PARTIAL" and real blocker language.
   - Scripts executable (verified with `ls -l`).
7. Verify intact hooks remain intact:
   - session-logger: `hook.py` uses `read_payload()`, `normalize_event()`, `skip_context()`, `write_jsonl()`.
   - session-auto-commit: `hook.py` uses `skip_context()` and `is_skipped()`; skips synthetic session ids.
   - governance-audit: `hook.py` uses `normalize_event()`, `resolve_end_status()`, identity resolution; `JSONL` output verified.
8. Verify partial hooks executable and config.yaml registered:
   - provider-executor: entrypoint hook.py; events array rebuilt.
   - rate-limit-bypass: same.
   - secrets-scanner: entrypoint hook.py; events array rebuilt (pre_llm_call); `scan-secrets.sh` present.
   - tool-guardian: entrypoint hook.py; events array rebuilt; `guard-tool.sh` present.
   - joystick-event-router: entrypoint hook.yaml; `events: []`; real blocker preserved (no synthetic event array fabricated).
9. Test rebuilt hooks with canonical event echo pipes (`echo '{"event":"on_session_start","session_id":"test-001"}' | bash hook.sh`). Verify exit 0 and JSONL output.
10. Verify intact hooks with echo pipes; confirm existing JSONL logs not broken.
11. Verify partial hooks: do NOT claim synthetic test pass. Confirm executable bits, hooks.json rebuilt, and real blocker language preserved.
12. Verify JSONL outputs for rebuilt hooks exist (`agent-hooks.jsonl`, `browser-hooks.jsonl`); confirm no synthetic clean claims in log notes for partial hooks.
13. Apply `/systematic-debugging` (mandatory after all tests — unconditional; regardless of pass/fail). Record real results (not synthetic).
14. Apply `/sync`. Confirm workspace identity (`.hermes.md`, `AGENTS.md`, `.cursorrules`, `base/AGENTS.md`) unchanged (only hook-level identity updated); no identity file modifications needed.
15. Retry any failed tests with real retry attempts; document retries in changelog.
16. `/document changelog`: update `~/.hermes/hooks/CHANGELOG.md` with scope (all 10 hooks), what changed (rebuilt hook.py/hook.sh cleaned; partial hooks preserved with real blockers; executable bits verified; config.yaml verified; spec/plan/run-card updated), verification evidence (real command outputs), and no synthetic claims.

## Data model (per hook record for verification — real, not synthetic)

```json
{
  "hook_name": "agent-hooks|browser-hooks|session-logger|session-auto-commit|governance-audit|provider-executor|rate-limit-bypass|secrets-scanner|tool-guardian|joystick-event-router",
  "scope_verified": true,
  "stub_fixed_or_preserved": "rebuilt|intact|partial_real_blocker_preserved",
  "hook_py_uses_lib": true,
  "hook_sh_delegates_or_has_stub_notes": true,
  "executable": true,
  "tests_run": true,
  "test_result_claim": "exit_0_for_rebuilt|verified_for_intact|not_claimed_synthetic_for_partial",
  "log_jsonl_exists_or_not_claimed": true,
  "config_registered": true,
  "real_blocker_preserved": true
}
```

## Verification criteria (all evidence-based; no synthetic results)

- All 10 hooks listed in `.omo/plans/hooks-plan.md` with real audit evidence.
- `.omo/plans/hook-run-card.md` reflects rebuilt (agent-hooks, browser-hooks) as completed or in-progress; partial hooks (provider-executor, rate-limit-bypass, secrets-scanner, tool-guardian, joystick-event-router) have tasks open with real blocker preserved (not fabricated clean).
- All rebuilt hook scripts executable (`ls -l` shows `-rwx` or equivalent).
- Partial hook scripts executable; `hook.py` retains minimal best-effort import/stub (NOT synthetic full handler); `hooks.json` notes retain PARTIAL/blocker language; `hook.sh` comments retain PARTIAL/blocker language.
- `config.yaml` `hooks:` block verified (10 entries; yaml.safe_load confirmed).
- `agent-hooks` and `browser-hooks` `hook.py` import from `lib.py` (verified by reading file contents — real import statements present).
- `agent-hooks` and `browser-hooks` `hook.sh` delegate to `hook.py` with clean comments (no "Repair instructions PARTIAL" stub text — verified by cat output).
- Canonical event tests pass (`echo` pipes return exit 0) for rebuilt hooks.
- Partial hooks do NOT claim synthetic pass; executable bits verified; hooks.json rebuilt; blocker language preserved.
- JSONL log files produced for rebuilt hooks; no synthetic claims for partial hooks' log outputs.
- `.omo/specs/hooks-spec.md` covers full 10-hook scope with clarification results and no synthetic claims.
- `CHANGELOG.md` updated (`/document changelog`) with real evidence (command outputs, file states) — no fabricated clean results.
- `/systematic-debugging` applied unconditionally after all tests (mandatory; real results recorded).
- `/sync` applied; workspace identity verified unchanged.
- No contradiction file needed (user selected safe/recommended options consistently; no conflict with safer conditional alternatives recorded).
