# Skill Coverage Report

Generated 2026-10-13. Coverage computed by matching app names and aliases against the live skills library at ~/.hermes/skills (1246 skills discovered at scan time).

## Coverage across all 3396 apps

| Status | Count |
|---|---|
| Covered (exact name or alias match) | 8 |
| Partial (keyword or substring match) | 150 |
| Missing | 3238 |
| **Reconciles to total** | **3396** |

## Skill creation candidates

User facing apps with coverage=missing, after filtering system runtime noise and deduping registry/winget pairs: 793.

By source: registry 32, winget 25, apt 736.
By category: misc 536, system-utilities 64, development 64, wireless 24, pentest-suite 22, recon 19, remote-access 14, exploitation 11, password-cracking 10, forensics 7, web 7, browsers 8, reverse-engineering 2, communication 2, media 2, security-defense 1.

## Skills created

793 SKILL.md files generated into ~/.hermes/skills/installed-apps/<category>/<slug>/SKILL.md via scripts/generate_app_skills.py. Each skill records the real source, version, and package summary from the inventory. Frontmatter validated: 793 files, 0 failures, 793 unique names. Spot checks against raw inventory: 5 of 5 version matches.

Examples of created skills: installed-apps/recon/nmap-scan, installed-apps/exploitation/sqlmap, installed-apps/password-cracking/hashcat, installed-apps/system-utilities/arp-scan, installed-apps/misc/kali-hidpi-mode.

## Covered apps (existing skills found)

nmap, metasploit-framework (alias msfconsole), radare2 (alias r2), wireshark, ghidra, hashcat (partial via skills keywords), vscode (alias code), ffuf, gobuster, nikto, sqlmap, python3, gcc.

## Partial coverage note

150 apps matched existing skills by keyword only (for example java-adjacent names matching javascript skills). These are informational; only exact and alias matches counted as covered.
