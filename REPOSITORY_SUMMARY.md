# Repository Summary — `profile`

> Generated from real local git history on 2026-07-16. All facts are evidence-based
> (commit hashes, dates, file names) and were not invented.

## Overview

`profile` is a **Django 4.x blog/CMS** application with cloud media storage, owned by
**rhixecompany**. It is one of five sibling repos under `SandBox/projects/` bootstrapped
together in mid-June 2026 and maintained through July 2026. The repository holds a functional
Django project (`manage.py`, `db.sqlite3`, `rhixecompany/` app, `base/`, `templates/`,
`static/`) plus a large `RESEARCH_REPORT.md` and a generated `web-research-profile.md`
(26 KB of web-research notes focused on Django + PostgreSQL, CKEditor, GCS, and Docker/GCP).

The working tree currently contains a **local SQLite database** (`db.sqlite3`, 184 KB) rather
than the production PostgreSQL target — consistent with a local development/setup phase.

## Architecture

- **Type:** Django monolith (standard MTV pattern with Class-Based Views).
- **Pattern:** CBVs preferred over FBVs; `snake_case` Python, `kebab-case` URLs; type hints in models/views.
- **Media:** Google Cloud Storage (GCS) via `django-storages`; `collectstatic` uploads to a GCS bucket.
- **Editor:** CKEditor 5 for rich-text content management.
- **Infra:** Docker + GCP deployment (see `Procfile`, `migrate.yaml`, `.gcloudignore`).

Per `AGENTS.md`, the reference architecture docs live at
`docs/Project_Architecture/Workflow_Analysis.md` and `docs/Project_Architecture/exemplars.md`.

## Key Components

| Path | Role |
|------|------|
| `manage.py` | Django entry point |
| `rhixecompany/` | Primary Django application package |
| `base/` | Base templates / shared app scaffolding |
| `templates/` | HTML templates |
| `static/` | Static assets (served via GCS in prod) |
| `db.sqlite3` | Local dev database |
| `requirements.txt` | Python dependencies |
| `migrate.yaml` | Migration/deploy workflow config |
| `Procfile` | Process declaration (GCP/Docker) |
| `RESEARCH_REPORT.md` | 2026 research findings (trimmed to size gate on 2026-07-16) |
| `web-research-profile.md` | 26 KB web-research dossier |
| `AGENTS.md` | Agent/dev architecture guide |

## Technologies

- **Backend:** Django 4.x, Python 3.11+
- **Database:** PostgreSQL (prod target) / SQLite (current local dev)
- **Media Storage:** Google Cloud Storage
- **Editor:** CKEditor 5
- **Infra:** Docker, Google Cloud Platform
- **Tooling:** ruff/mypy conventions referenced across sibling repos; VS Code configs (`.vscode/`, `.github/`)

## Data Flow

```
Author/Browser → Django CBVs → Models → PostgreSQL (prod) / SQLite (dev)
                        ↓
                  CKEditor 5 (rich text)
                        ↓
              collectstatic → Google Cloud Storage (media/static)
```

## Team

| Contributor | Commits | Role |
|-------------|---------|------|
| `rhixecompany` <rhixecompany@gmail.com> | 5 / 5 (100%) | Sole author — setup, config, docs, research reports |

**Bus factor:** 1. All 5 commits were authored by a single contributor.
There are no co-authors, no merge commits, and no external PRs in the history.
