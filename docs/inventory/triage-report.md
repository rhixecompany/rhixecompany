# App Triage Report

Generated 2026-10-13 from real command output. No synthetic data.

## Sources enumerated

| Source | Command | Count |
|---|---|---|
| Windows registry | powershell.exe Get-ItemProperty (HKLM, WOW6432Node, HKCU Uninstall paths) | 86 |
| winget | powershell.exe winget list (table parse; --output json unsupported on v1.29.380) | 105 |
| choco | powershell.exe choco list --local-only --limit-output | 0 (choco 2.5.0 installed, zero local packages) |
| Kali apt | dpkg-query -W | 3205 |
| **Total** | | **3396** |

Raw data: docs/inventory/apps-registry.json, apps-winget.json, apps-choco.json, apps-apt.json.

## Category distribution (all 3396 records)

| Category | Count |
|---|---|
| misc | 1709 |
| development | 1218 |
| system-utilities | 237 |
| reverse-engineering | 46 |
| recon | 26 |
| wireless | 25 |
| remote-access | 23 |
| pentest-suite | 23 |
| media | 16 |
| browsers | 16 |
| exploitation | 13 |
| password-cracking | 12 |
| forensics | 11 |
| web | 10 |
| communication | 8 |
| games | 2 |
| security-defense | 1 |

## User facing vs libraries

- User facing apps: 1005
- Library or dependency packages (lib*, python3-*, -dev, -dbg, x11, fonts, etc.): 2391

## Stale and duplicate flags

- winget entries duplicating a registry entry of the same product: 46 (flagged, registry kept canonical)
- apt packages with no description: 2
- Windows runtime and driver noise filtered from skill candidates (Visual C++ redistributables, .NET runtimes, Intel drivers, Bonjour, WSL itself, etc.): 67

## Notable real findings

- The Windows host runs Git 2.55.0.5, VLC 3.0.24, WSL 2.7.13.0, AnyDesk ad 9.8.1, Brave 155.1.97.56, Google Chrome 155.0.8059.40 (from registry and winget probes).
- The Kali side carries the full rolling 2026.3 tool set: nmap, sqlmap, hashcat, aircrack-ng, ghidra, volatility, radare2, john, hydra, wpscan, nikto, gobuster, ffuf, nuclei, and several hundred smaller CLI utilities.
- choco is installed on the Windows host but has zero local packages.
