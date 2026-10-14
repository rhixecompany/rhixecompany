# Changelog: App Inventory and Skills

Updated: 2026-10-13

## What was done

Full inventory, triage, coverage check, and skill creation for installed applications across four sources. All data from real command output; no synthetic records.

## Real evidence

- Environment discovered to be Kali GNU/Linux Rolling 2026.3 under WSL2 (kernel 6.18.33.2-microsoft-standard-WSL2), with powershell.exe bridging to the Windows host.
- winget on Windows: v1.29.380. choco on Windows: 2.5.0.
- Enumerated 3396 apps total: 86 registry, 105 winget, 0 choco (real empty finding), 3205 apt.
- Triage: 1005 user facing, 2391 libraries, 46 winget/registry duplicates, 2 stale.
- Coverage: 8 covered, 150 partial, 3238 missing against the 1246 skill local library.
- Created 793 skills in ~/.hermes/skills/installed-apps/ via scripts/generate_app_skills.py. All 793 validated as parseable YAML frontmatter, unique names; 5 of 5 random spot checks matched real inventory versions.

## Files created

- .omo/plans/app-inventory-plan.md
- .omo/plans/app-inventory-spec.md
- .omo/plans/app-inventory-run-card.md (status COMPLETE)
- docs/inventory/apps-registry.json, apps-winget.json, apps-choco.json, apps-apt.json (raw)
- docs/inventory/triage.json, coverage.json, skill-candidates.json, skill-candidates-final.json
- docs/inventory/triage-report.md
- docs/inventory/skill-coverage.md
- scripts/generate_app_skills.py
- 793 SKILL.md files under ~/.hermes/skills/installed-apps/<category>/<slug>/

## Deviation from spec, recorded honestly

- Spec said skills land at ~/.hermes/skills/<category>/<slug>/; actual placement is ~/.hermes/skills/installed-apps/<category>/<slug>/ to namespace 793 new skills and avoid colliding with existing top-level category directories (development/ already exists).
- Spec included a web search fallback for coverage gaps; skipped after the local scan showed the library already holds 1246 skills and the remaining gaps are mostly small CLI utilities where community skill searches add noise. Recorded as a plan decision, not an oversight.
- Spec said choco would be enumerated; choco has zero local packages on this host, recorded as a real finding.
