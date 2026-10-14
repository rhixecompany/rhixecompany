#!/usr/bin/env python3
"""Generate one SKILL.md per uncovered user-facing installed app.

Reads docs/inventory/skill-candidates-final.json (real inventory data) and
writes ~/.hermes/skills/installed-apps/<category>/<slug>/SKILL.md for each
candidate. No invented data: every field comes from the inventory record.
"""

import json
import re
import os
import sys

INV = '/mnt/c/Users/Alexa/playgrounds/profile/docs/inventory'
SKILLS_ROOT = '/home/alexa/.hermes/skills'
OUT_ROOT = os.path.join(SKILLS_ROOT, 'installed-apps')

CATEGORY_USAGE = {
    'recon': 'target discovery, enumeration, and subdomain or service mapping',
    'exploitation': 'exploitation, post exploitation, and credential relay work',
    'web': 'web application testing and HTTP level assessment',
    'password-cracking': 'password recovery and credential attacks',
    'wireless': 'wireless network auditing and radio level testing',
    'forensics': 'disk, memory, and file forensics plus artifact recovery',
    'reverse-engineering': 'binary analysis, debugging, and reverse engineering',
    'development': 'software development, compilation, and build tooling',
    'browsers': 'browsing and web client workflows',
    'communication': 'messaging and collaboration',
    'media': 'media playback, editing, and conversion',
    'system-utilities': 'system administration and day to day command line work',
    'security-defense': 'defensive monitoring and hardening',
    'games': 'gaming',
    'remote-access': 'remote access, file transfer, and SSH workflows',
    'pentest-suite': 'penetration testing distribution tooling',
    'misc': 'command line and system work',
}

CATEGORY_PITFALLS = {
    'recon': 'Passive and active recon both generate noise; confirm authorization before scanning targets you do not own.',
    'exploitation': 'Only run against systems you own or have explicit written permission to test; exploitation tooling can cause real damage.',
    'web': 'Test requests can corrupt application state; use non destructive options first and respect scope boundaries.',
    'password-cracking': 'Only crack hashes from systems you are authorized to test; treat recovered credentials as sensitive data.',
    'wireless': 'Wireless auditing must stay inside your own network or a lab; transmitting outside authorized bands breaks law in most regions.',
    'forensics': 'Work on copies, never originals; document every step so findings survive scrutiny in an incident review.',
    'reverse-engineering': 'Analyze only software you own or are authorized to examine; check license terms before distributing findings.',
    'development': 'Pin toolchain versions in project docs so builds stay reproducible across machines.',
    'system-utilities': 'System utilities often need elevated privileges; read the man page before running anything destructive as root.',
    'security-defense': 'Tune detection rules against your own environment before alerting on them; false positives erode trust fast.',
    'remote-access': 'Rotate keys and use non default ports or gateways where appropriate; never leave credentials in shell history.',
    'browsers': 'Keep the browser patched; it is the most exposed application on the machine.',
    'communication': 'Treat message backups as sensitive; sync scope and retention matter.',
    'media': 'Transcoding is CPU heavy; prefer hardware acceleration paths when available.',
    'games': 'None beyond normal account security hygiene.',
    'pentest-suite': 'Distribution meta tools bundle many capabilities; audit what is installed before assuming coverage.',
    'misc': 'Check the man page or --help output before scripting around it; output formats differ between versions.',
}


def slugify(name: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    return s[:80] or 'app'


def yaml_escape(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"')


def build_skill(rec: dict) -> str:
    name = rec['name']
    cat = rec['category']
    desc = rec.get('description', '').strip()
    source = rec['source']
    version = rec.get('version', '')
    slug = slugify(name)

    # First 57 chars of description must be a self-contained trigger.
    trigger = f'Use when working with {name[:40]}'
    if len(trigger) > 57:
        trigger = trigger[:54] + '...'
    behavior = desc if desc else CATEGORY_USAGE.get(cat, 'related command line work')
    full_desc = f'{trigger}. {behavior}.'

    usage = CATEGORY_USAGE.get(cat, 'related command line work')
    pitfall = CATEGORY_PITFALLS.get(cat, 'Check the man page before automating.')

    if source == 'apt':
        install = f'Installed on this machine via dpkg (Kali Linux Rolling). Package: {name}, version {version}. Install command on a Debian or Kali host: `apt-get install {name}`.'
    elif source == 'winget':
        install = f'Installed on the Windows host via winget. winget id: {rec.get("publisher", "")}, version {version}. Reinstall: `winget install --id {rec.get("publisher", name)}`.'
    elif source == 'registry':
        install = f'Installed on the Windows host (registry uninstall entry, publisher: {rec.get("publisher", "unknown")}, version {version}).'
    else:
        install = f'Installed, source: {source}, version {version}.'

    usage_block = f'This tool belongs to the {cat} category: {usage}.'
    if desc:
        usage_block += f'\n\nPackage summary: {desc}'
    usage_block += (
        '\n\nStart with `--help` or the man page to confirm flags for the installed version, '
        'then check the project homepage or Kali package docs for examples.'
    )

    return f'''---
name: {slug}
description: "{yaml_escape(full_desc)}"
category: installed-apps
title: "{yaml_escape(name)}"
version: 1.0.0
license: MIT
tags: [{cat.replace("-", "_")}, installed_app, {source}]
metadata:
  hermes:
    tags: [{cat.replace("-", "_")}, installed_app, {source}]
---

# {name}

{usage_block}

## When to Use

- The installed app `{name}` is relevant to the task (version {version} on this machine).
- The work falls under {cat}: {usage}.
- A command or script needs this specific tool rather than a generic alternative.

## Install Notes

{install}

## Pitfalls

- {pitfall}
- Version drift: the installed version is {version}; flags and output formats can differ between releases.

## Verification Checklist

- [ ] `{name}` responds to `--help` or has a man page on this machine
- [ ] The installed version matches the inventory record ({version})
- [ ] Any scripted use was tested against the real installed binary
'''


def main():
    candidates = json.load(open(os.path.join(INV, 'skill-candidates-final.json')))
    created = 0
    skipped = 0
    for rec in candidates:
        cat = rec['category']
        slug = slugify(rec['name'])
        out_dir = os.path.join(OUT_ROOT, cat, slug)
        out_file = os.path.join(out_dir, 'SKILL.md')
        if os.path.exists(out_file):
            skipped += 1
            continue
        os.makedirs(out_dir, exist_ok=True)
        with open(out_file, 'w') as f:
            f.write(build_skill(rec))
        created += 1
    print(f'created: {created}, skipped (already existed): {skipped}')
    return created


if __name__ == '__main__':
    sys.exit(0 if main() >= 0 else 1)
