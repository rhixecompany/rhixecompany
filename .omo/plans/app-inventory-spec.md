# App Inventory and Skills Spec

## Goal

Build a real, evidence backed inventory of installed applications across four sources (Windows registry uninstall keys, winget, choco, Kali apt), triage them by function, check each against the local Hermes skills library, and create missing skills for uncovered user facing apps.

## Sources and exact commands

### 1. Windows registry uninstall keys

Via powershell.exe from WSL:

```
powershell.exe -Command "Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*','HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*' | Where-Object {$_.DisplayName} | Select-Object DisplayName,DisplayVersion,Publisher,InstallLocation | ConvertTo-Json -Depth 3"
```

Fields: DisplayName, DisplayVersion, Publisher, InstallLocation.

### 2. winget list

```
powershell.exe -Command "winget list --accept-source-agreements --disable-interactivity"
```

Machine readable form preferred if available: `winget list --accept-source-agreements --output json` (fall back to table parse if the installed winget version does not support it).

### 3. choco list

```
powershell.exe -Command "choco list --local-only --limit-output"
```

`--limit-output` gives name|version lines.

### 4. Kali apt

```
dpkg-query -W -f='${Package}\t${Version}\t${Priority}\t${Section}\t${binary:Summary}\n'
```

Fields: Package, Version, Priority, Section, binary:Summary.

## Data model (per app record)

```json
{
  "name": "string",
  "version": "string",
  "source": "registry|winget|choco|apt",
  "publisher": "string",
  "section": "string",
  "description": "string",
  "category": "string",
  "user_facing": true,
  "stale_flag": false,
  "stale_reason": "string",
  "coverage": "covered|partial|missing",
  "matched_skills": ["skill names"],
  "skill_created": "skill name or null"
}
```

## Categorization heuristics (keyword rules, applied in order)

- recon/scanning: nmap, masscan, recon, enum, nikto, dirb, gobuster, fierce, dnsrecon, sublist3r, theharvester
- exploitation: metasploit, msf, sqlmap, beef, setoolkit, exploit, payload, responder, impacket, crackmapexec
- web: burp, zap, owasp, wfuzz, ffuf, feroxbuster, wpscan, joomscan, nuclei, httpx
- password/cracking: hashcat, john, hydra, medusa, crunch, cewl, seclists, rockyou
- wireless: aircrack, kismet, wifite, reaver, hostapd, bettercap
- forensics: autopsy, sleuth, volatility, binwalk, foremost, exiftool, bulk_extractor, guymager
- reverse engineering: ghidra, radare2, r2, gdb, ida, objdump, strace, ltrace, apktool, jadx
- dev tools: python, gcc, g++, node, npm, git, docker, make, cmake, vscode, vim, nvim, emacs
- browsers: firefox, chromium, chrome, edge, brave, tor browser
- communication: discord, telegram, signal, slack, teams, zoom, thunderbird
- media: vlc, ffmpeg, gimp, inkscape, obs, audacity, blender
- system utilities: wsl, powershell, 7zip, notepad++, sysinternals, process explorer, everything
- security defense: defender, firewall, antivirus, clamav, suricata, snort, wazuh, ossec
- default category: misc

## Stale/duplicate flags

- apt: package with empty summary AND name matching ^(lib|python3?-|perl-|ruby-|gir1.2-|fonts-) → library, not stale but not user facing.
- winget vs registry same product name (case insensitive) → duplicate pair, registry is canonical, winget row flagged duplicate.
- choco vs winget same name → duplicate pair.
- Packages with no description anywhere → flagged stale (info missing).

## Skill coverage check

- Load local skills listing from ~/.hermes/skills/ (walk directories, collect SKILL.md names and frontmatter description keywords).
- For each app, normalize name (lowercase, strip punctuation) and test: exact name match, alias match (known alias table for popular tools like msfconsole→metasploit, r2→radare2, zap→owasp-zap), keyword match against skill descriptions.
- Classify: covered (exact or alias), partial (keyword hit only), missing (no hit).
- Web search fallback only for missing apps that are user facing and not library packages, capped at a bounded sample per run to control cost.

## Skill creation rules

- Only apps with coverage=missing and user_facing=true get a generated skill.
- Generated SKILL.md must have frontmatter: name (slug), description (first 57 chars a self contained trigger: Use when <trigger>. <behavior>), category, version, tags, license MIT, metadata.hermes.tags.
- Body sections: overview, when to use, install notes (the real source and command that proved it installed), basic usage stub, pitfalls (real ones from the tool category), verification checklist.
- Skills land under ~/.hermes/skills/<category>/<slug>/SKILL.md.
- Generator writes from real inventory data only. If inventory row is missing a field, the field is omitted, never invented.

## Reports

- docs/inventory/apps-<source>.json — raw per source inventory.
- docs/inventory/triage-report.md — categorized counts, per category app tables, stale flags.
- docs/inventory/skill-coverage.md — coverage matrix, missing apps list.
- .omo/plans/app-inventory-run-card.md — the run card.
- CHANGELOG entry — what was created, counts, verification evidence.

## Verification

- Every JSON file parses (python json.load).
- Every generated skill parses as YAML frontmatter (yaml.safe_load on the frontmatter block).
- Counts reconcile: apps_total = covered + partial + missing.
- No synthetic values: spot check 5 random records against the raw command outputs.
