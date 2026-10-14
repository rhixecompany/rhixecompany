# Copilot instructions for profile

This repository is two things at once: a Hermes agent profile/configuration workspace and a Django blog/CMS app. Treat the project-level rules in the repo root (`AGENTS.md`, `.hermes.md`, `CLAUDE.md`, `.cursorrules`) as canonical; this file adds the repo-specific workflow and structure that future sessions need to know quickly.

## Build, test, and lint

Run commands from the repository root:

```bash
# Lint
ruff check .

# Type-check (project metadata exposes this as the repo's Python static check)
pyright .

# Django tests
python manage.py test

# Single test target example
python manage.py test base.tests
# or
python manage.py test base.tests.TestSomething.test_case_name
```

The CI workflow in `.github/workflows/ci.yml` runs the same core checks:

```bash
pip install -r requirements.txt
ruff check .
python manage.py test
```

Package scripts are minimal wrappers around the Python tooling; the project is not a Node-heavy app:

```bash
bun run lint
bun run typecheck
```

## Architecture at a glance

- `base/` holds the app-domain logic for the blog/CMS: models, views, forms, and URL routing.
- `rhixecompany/` holds the Django project configuration: settings, URL root wiring, WSGI/ASGI configuration, and project-level integration.
- `templates/` and `static/` hold project-wide templates and static assets, including CKEditor vendor files.
- `requirements.txt` is the source of truth for Python dependencies; this repo does not rely on a large JavaScript toolchain.
- The repo also contains Hermes identity/profile configuration files (`.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`) alongside the Django app, so identity/config edits and app edits are both in scope.

Important boundary: keep business logic in `base/`, not in `rhixecompany/`. The `base/AGENTS.md` file is explicit about this and says new tests should live in `base/tests.py` or `base/test_*.py`.

## Key conventions

- Use class-based Django views when adding request handling in `base/views.py`.
- Prefer `snake_case` field and variable names and `PascalCase` model classes in the Django app.
- Keep settings and project wiring in `rhixecompany/`; do not scatter Django config into the app package.
- Do not add npm dependencies or invent a frontend build system unless the task explicitly requires it; the repo has no real JS app tooling.
- Do not overwrite CKEditor vendor files or move original vendor assets; clone or preserve them when making customizations.
- Check the repo identity rules before making agent-identity/config changes; the root docs are authoritative for profile linkage and file-hierarchy behavior.
- Treat `.env` as sensitive and do not edit or commit it.

## Working style for this repo

- Prefer targeted changes over broad refactors.
- Validate with the smallest relevant command: a single Django test target when possible, otherwise the repo lint/test flow.
- When a task involves repo identity or profile config, read the root `AGENTS.md` and related identity files first so you do not contradict the workspace’s Hermes rules.
- For Django logic work, start in `base/` and the app-level tests before touching project settings.

## Related references

- `README.md` — project overview and profile/provider configuration
- `AGENTS.md` — workspace-level rules and identity expectations
- `CLAUDE.md` — Claude-specific repo behavior
- `.cursorrules` — Cursor-specific conventions
- `.github/workflows/ci.yml` — actual validation flow used in CI
- `base/AGENTS.md` — app-specific domain boundaries and testing expectations
