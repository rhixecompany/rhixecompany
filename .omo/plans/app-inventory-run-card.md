# App Inventory Run Card

Status: COMPLETE (all phases done 2026-10-13)

Validation results (real evidence):
- registry probe rc=0, real apps found (NVM for Windows 1.2.2, Git 2.55.0.5, Intel Graphics)
- winget list rc=0, table output only; --output json NOT supported on winget v1.29.380 (rc=1) → parse table
- choco list --local-only rc=0 but ZERO packages installed (choco 2.5.0 present, empty package list) → record empty as real finding
- dpkg-query rc=0, 3205 lines well formatted

Scope: Windows registry, winget, choco, Kali apt

Phase 1 Enumerate:
- [x] Windows registry uninstall keys via powershell.exe (HKLM + WOW6432Node + HKCU paths) — 86 apps
- [x] winget list via powershell.exe — 105 packages
- [x] choco list --local-only --limit-output via powershell.exe — 0 packages (real finding)
- [x] Kali apt via dpkg-query -W — 3205 packages
- [x] Save raw JSON per source to docs/inventory/

Phase 2 Triage:
- [x] Categorize all apps with keyword heuristics — 17 categories, counts in triage-report.md
- [x] Flag library packages (not user facing) — 2391 libraries
- [x] Flag duplicates across winget/registry — 46 duplicates
- [x] Flag stale (no description) — 2 apt packages
- [x] Write docs/inventory/triage-report.md

Phase 3 Coverage:
- [x] Scan ~/.hermes/skills/ for existing coverage — 1246 skills scanned
- [x] Classify covered/partial/missing — 8 covered, 150 partial, 3238 missing (reconciles to 3396)
- [x] Web search fallback skipped by plan decision (local scan sufficient for library packages)
- [x] Write docs/inventory/skill-coverage.md

Phase 4 Implement:
- [x] Write skill generator script — scripts/generate_app_skills.py
- [x] Generate SKILL.md per missing user facing app — 793 skills in ~/.hermes/skills/installed-apps/
- [x] Validate generated skill frontmatter parses as YAML — 793 files, 0 failures
- [x] Reconcile counts — 5 of 5 spot checks match raw inventory versions

Phase 5 Document:
- [x] Changelog entry with real counts and evidence
- [x] Final verification report (no synthetic data check) — all records trace to real command output
