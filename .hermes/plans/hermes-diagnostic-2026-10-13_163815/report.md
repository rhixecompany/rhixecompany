# Hermes Diagnostic Report — 2026-10-13_163815

- Workspace: `/mnt/c/Users/Alexa/playgrounds/profile`
- Mode: read-only diagnostic; repair gated
- Result: 9/12 passed; 2 failed; 0 timed out; 1 skipped.

## Command results

| Command | Exit | Seconds | Result |
|---|---:|---:|---|
| `hermes doctor` | 1 | 26.506 | FAIL |
| `hermes doctor --fix` | None | 0.000 | SKIPPED_APPROVAL |
| `hermes security audit` | 1 | 7.301 | FAIL |
| `hermes status --deep` | 0 | 5.605 | PASS |
| `hermes insights --days 30 --source cli` | 0 | 2.022 | PASS |
| `hermes logs list` | 0 | 1.841 | PASS |
| `hermes logs errors -n 100` | 0 | 1.895 | PASS |
| `hermes logs desktop -n 100` | 0 | 1.786 | PASS |
| `hermes logs gateway -n 100` | 0 | 1.844 | PASS |
| `hermes logs gui -n 100` | 0 | 1.769 | PASS |
| `hermes logs agent -n 100` | 0 | 1.829 | PASS |
| `bun run check` | 0 | 0.029 | PASS |

## Repair gate

- Safe mode records `hermes doctor --fix` as `SKIPPED_APPROVAL`.
- Use `--fix --approve` only after reviewing the read-only report.

## Next action

- Review failed findings; run repair only with explicit approval.
