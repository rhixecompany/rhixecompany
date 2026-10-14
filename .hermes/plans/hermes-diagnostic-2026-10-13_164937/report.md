# Hermes Diagnostic Report — 2026-10-13_164937

- Workspace: `/mnt/c/Users/Alexa/playgrounds/profile`
- Mode: read-only diagnostic; repair gated
- Result: 9/12 passed; 2 failed; 0 timed out; 1 skipped.

## Command results

| Command | Exit | Seconds | Result |
|---|---:|---:|---|
| `hermes doctor` | 1 | 25.809 | FAIL |
| `hermes doctor --fix` | None | 0.000 | SKIPPED_APPROVAL |
| `hermes security audit` | 1 | 7.306 | FAIL |
| `hermes status --deep` | 0 | 5.362 | PASS |
| `hermes insights --days 30 --source cli` | 0 | 2.170 | PASS |
| `hermes logs list` | 0 | 1.871 | PASS |
| `hermes logs errors -n 100` | 0 | 1.799 | PASS |
| `hermes logs desktop -n 100` | 0 | 1.758 | PASS |
| `hermes logs gateway -n 100` | 0 | 1.801 | PASS |
| `hermes logs gui -n 100` | 0 | 1.777 | PASS |
| `hermes logs agent -n 100` | 0 | 1.785 | PASS |
| `bun run check` | 0 | 0.060 | PASS |

## Findings

- `hermes doctor`: still exits 1 after repair/update; dependency findings, optional-key warnings, and stale channel metadata remain.
- `hermes doctor --fix`: explicitly run; it did not clear the stale channel record or dependency findings.
- `hermes security audit`: unchanged at 55 findings across 130 components — 1 critical, 13 high, 16 moderate, and 25 unknown.
- The updated source still pins vulnerable versions such as `PyJWT[crypto]==2.13.0`, `httpx2==2.7.0`, `tornado==6.5.8`, and `oauthlib==3.3.1`; remediation requires upstream dependency/lockfile changes rather than another Hermes update.
- Hermes update completed from `d4e7b659` to `8f817911`; the gateway restarted and is running.
- Nous managed tools remain unavailable because the Portal account has no usable paid credits.

## Repair gate

- Safe mode records `hermes doctor --fix` as `SKIPPED_APPROVAL`.
- Use `--fix --approve` only after reviewing the read-only report.

## Next action

- Review failed findings; run repair only with explicit approval.
