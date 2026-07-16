# AUDIT — profile

Read-only repo-management audit (Phases 0, 2, 3). Destructive phases HELD.

## Overview
Django web application (`rhixecompany` project). Has AGENTS.md, README/REPOSITORY_SUMMARY.md, `.github/`, `.vscode/`, GCP deploy artifacts (`.gcloudignore`, `migrate.yaml`, `Procfile`). App dir: `rhixecompany/`, `base/`, `templates/`, `static/`.

## Disk Usage
39M (excluding .git/node_modules/venv/caches/build). Bulk includes committed `db.sqlite3` (184 KB) and `static/`.

## Entrypoint
- `manage.py` (Django CLI)
- `Procfile`: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 rhixecompany.wsgi:application`

## Gitignore Audit
`.gitignore` present (Django/Python template).
Covered: node_modules, .env, *.pyc, __pycache__/, dist/, build/, venv/.
MISSING:
- `.DS_Store` — not listed.
- `.next/` — not listed (N/A, Django project, low priority).
- **`db.sqlite3` NOT ignored — and `db.sqlite3` (184 KB) IS committed to the repo.** Flag: SQLite DB tracked in git; recommend ignoring + removing from tracking (destructive — HELD).

## Dependency Audit
- `requirements.txt` present (Django, gunicorn, Pillow, psycopg2-binary, django-storages[google], boto/s3transfer, whitenoise, django-environ, etc.). Unpinned versions (no `==`), so drift/known-vuln risk cannot be assessed from the file alone.
- `pip` available (3.11 venv). `pip-audit` NOT installed — could not run vulnerability scan (read-only; no install performed).
- No lockfile (no pip-tools/poetry lock) → non-reproducible installs.

## Branch State
`git branch`: `* development`, `production`. No `master`/`main`/stray branches. Current = development.

## Destructive Phases HELD
- Phase 1 (branch deletion / push): NOT run.
- Phase 4 (CI creation): NOT run.
- Recommended-but-deferred: add `.DS_Store` + `db.sqlite3` to .gitignore and `git rm --cached db.sqlite3` (requires approval).
