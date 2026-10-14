# Hermes Skills Audit Report

Scope: `/home/alexa/.hermes/skills`
Inventory: 1246 SKILL.md files
Unique names: 1222; duplicate-name groups: 21
Composer gate: `[composer-modes] register ver=v2.0.1 default=agent modes=ask,agent,plan,debug enforce=True` — observed 3 time(s)
Hub deep audit: command announced 51 skills; 45 scan records parsed; 3 dangerous verdicts; 8 blocked decisions.

## Baseline

Average score: 73.00
| Rating | Count |
|---|---:|
| FAIL | 96 |
| PASS | 325 |
| WARN | 825 |

## Final

Average score: 76.98
| Rating | Count |
|---|---:|
| FAIL | 2 |
| PASS | 488 |
| WARN | 756 |

## Installed skill-judge verification

Total: 1246; average: 98.91
PASS: 1246; FAIL: 0

## Remediation

Manifest entries: 3738
Unique changed paths: 277
Changed entries: 300
Skipped/protected/classified: 3438
Errors: 0

## Validation

Validation results: 1246
Validation failures: 57
| Finding | Count |
|---|---:|
| missing tags | 26 |
| placeholder text | 17 |
| unbalanced code fences | 17 |

## Safety and next action

No skills were deleted. Protected and duplicate paths remain classified. Hermes source and dependencies were not updated.
The installed validator script remains unusable on this WSL tree because it has CRLF line endings and assumes flat `skills/*.md`; the custom validator above recursively covered all 1,246 SKILL.md files.
Review the remaining WARN queue, protected bundled skills, placeholder/template findings, and malformed-fence findings before deeper content rewrites.

## Repository verification

- `bun run check`: PASS
- `npm run check`: PASS
- `npm run lint`: BLOCKED — `ruff` is not installed on PATH
- `npm run typecheck`: BLOCKED — `pyright` is not installed on PATH
- `ruff check .`: BLOCKED — `ruff` is not installed on PATH

No Hermes update, dependency installation, skill deletion, or external publication was performed.
