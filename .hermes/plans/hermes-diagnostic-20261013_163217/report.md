# Hermes Diagnostic Report — 20261013_163217

- Workspace: `/mnt/c/Users/Alexa/playgrounds/profile`
- Mode: read-only diagnostic; repair actions gated
- Result: 10/12 commands passed; 2 failed; 0 timed out.

## Runner deviation

- The skill-referenced `scripts/hermes_diagnostic.py` was absent. The documented command set ran through an equivalent bounded runner.

## Command results

| Command | Exit | Seconds | Result |
|---|---:|---:|---|
| `hermes doctor` | 1 | 23.305 | FAIL |
| `hermes security audit` | 1 | 7.851 | FAIL |
| `hermes status --deep` | 0 | 6.664 | PASS |
| `hermes insights --days 30 --source cli` | 0 | 2.953 | PASS |
| `hermes logs list` | 0 | 2.562 | PASS |
| `hermes logs errors -n 100` | 0 | 2.523 | PASS |
| `hermes logs desktop -n 100` | 0 | 2.858 | PASS |
| `hermes logs gateway -n 100` | 0 | 2.700 | PASS |
| `hermes logs gui -n 100` | 0 | 2.586 | PASS |
| `hermes logs agent -n 100` | 0 | 2.845 | PASS |
| `bun run check` | 0 | 0.447 | PASS |
| `npm run check` | 0 | 0.558 | PASS |

## Findings

- `hermes doctor`: exit 1; reports three upstream workspace vulnerability groups, missing optional API keys, and stale channel metadata.
- `hermes security audit`: 55 findings across 130 components — 1 critical, 13 high, 16 moderate, and 25 unknown.
- Affected components include `PyJWT==2.13.0`, `@playwright/mcp==latest`, `httpx2==2.7.0`, `tornado==6.5.8`, and `urllib3==2.7.0`.
- `hermes status --deep`: core gateway is running and OpenRouter is reachable; Nous managed tools are unavailable because the Portal account has no usable paid credits.
- Error logs show repeated Honcho sync failures caused by insufficient credits; historical Telegram, MCP, WebSocket, and desktop backend timeouts are also present.

## Repair gate

- `hermes doctor --fix`, dependency remediation, provider setup, and Hermes updates were not run.
- These actions require review because they can modify configuration, lockfiles, credentials, or runtime behavior.

## Next action

- Review failed command tails in `report.json`, approve only the repairs within scope, then rerun the diagnostic sweep.
