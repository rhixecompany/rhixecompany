# App Inventory and Skills Plan

Created 2026-10-13 from clarify-requirements answers (5 of 5 answered).

## Environment evidence (real, verified)

- Host: Kali GNU/Linux Rolling 2026.3 (ID=kali, VERSION_CODENAME=kali-rolling) running under WSL2 (kernel 6.18.33.2-microsoft-standard-WSL2), node adminbot.
- Windows host drive accessible at /mnt/c.
- powershell.exe and cmd.exe reachable from WSL (bridge works).
- winget on Windows: v1.29.380 (verified via powershell.exe winget --version).
- choco on Windows: 2.5.0 (verified via powershell.exe choco --version).
- Kali apt/dpkg/apt-get present; 3202 packages installed (dpkg -l, ii state).
- snap: not present.

## Clarified requirements

1. Windows app enumeration: both registry uninstall keys and winget list.
2. Triage: categorize by function, check Hermes skill coverage per app, flag stale or duplicate packages.
3. Skill granularity: one skill per individual app (user explicitly chose per-app skills despite the scale).
4. Artifact location: both workspace reports (.omo/plans/ and docs/) and skills in the live library (~/.hermes/skills/).
5. Coverage check: local skills library scan first, web search fallback for gaps.

## Plan steps (ordered)

1. Enumerate Windows apps via registry uninstall keys (powershell.exe Get-ItemProperty on both 64-bit and 32-bit uninstall paths).
2. Enumerate winget packages (powershell.exe winget list --accept-source-agreements, machine readable output).
3. Enumerate choco packages (powershell.exe choco list --local-only, or clist local).
4. Enumerate Kali apt packages (dpkg-query -W -f with description).
5. Merge into one JSON inventory per source under docs/inventory/ (or .omo/plans/inventory/).
6. Categorize every app by function (recon, exploitation, web, forensics, dev tools, editors, browsers, communication, media, system, security, games, etc.) using keyword heuristics over names and descriptions.
7. Flag stale or duplicate: packages with no description, version marked local, winget entries that overlap with registry entries of the same product, apt packages that are libraries (not user facing apps).
8. Check skill coverage: scan ~/.hermes/skills/ for each app name and known aliases; classify as covered, partially covered, or missing.
9. Web search fallback: for a bounded sample of missing high profile apps, search for community skills (skip for library packages where web search is noise).
10. Create missing skills: generate one SKILL.md per uncovered user facing app via a generator script that writes proper frontmatter and body from the triage metadata, into ~/.hermes/skills/ with category subdirectories.
11. Write triage reports (categorized inventory, stale list, coverage matrix, gap list) into workspace docs/ and .omo/plans/.
12. Verification: validate YAML frontmatter of generated skills, count skills created, confirm no synthetic data, write changelog.

## Scale note

The Kali apt side has 3202 packages, most of which are libraries and dependencies, not user facing apps. The per-app skill decision applies to user facing apps. Libraries will be triaged in the report but get one category skill or none, to avoid thousands of empty stub skills. The generator script enforces: only apps with a user facing signal (has a description, not a lib*-style name, not a python3-* / -dev / -dbg suffix) get their own skill; everything else is documented in the triage report.

## Anti-patterns to avoid

- No synthetic app data: every inventory row must come from a real command output.
- No fabricated skill coverage claims: coverage is computed by matching names against the real skills library listing.
- No committing secrets: none of these commands touch .env.
- Skill files must follow the live skill format (frontmatter with name, description, category, tags) or they will fail validation.
