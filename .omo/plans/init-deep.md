# PROJECT KNOWLEDGE BASE

**Generated:** 2026-10-13
**Commit:** Unknown (Local)
**Branch:** Local

## OVERVIEW
Django application. Stack: Python, Django, PostgreSQL, Ruff (linting/formatting), EditorConfig.

## STRUCTURE
```
{root}/
├── base/          # Django application domain (views, models, forms)
├── rhixecompany/  # Django project configuration (settings, URLs, entry points)
└── manage.py      # Entry point
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Domain Logic | /base/ | Models, Views, Forms, Signals |
| Configuration | /rhixecompany/ | Settings, URLs, Deployment |
| Static Assets | /static/ & /base/static/ | Overlapping; prefer app-level when in doubt |
| CI | .github/workflows/ | Runs Ruff + tests on development/production |

## CONVENTIONS
- **Linting/Formatting:** Use `ruff`. Configured in `.ruff.toml` (120 chars line length).
- **Style:** EditorConfig (`.editorconfig`) enforced. Python indentation: 4 spaces.
- **Testing:** Greenfield (no active tests). Use Django's `TestCase` or `pytest`.

## ANTI-PATTERNS (THIS PROJECT)
- DO NOT commit secrets (tokens, .env).
- DO NOT move original JS vendor objects; clone them.
- DO NOT overwrite settings or configs; create overrides.
- DO NOT use the README as a source of truth for architecture (it currently misrepresents the project).

## COMMANDS
```bash
python manage.py runserver  # Start dev
python manage.py test       # Run tests
ruff check .                # Lint
```

## NOTES
- **Settings:** `rhixecompany/settings.py` is canonical. Be cautious with `rhixecompany/setting.py`.
- **Package Metadata:** `package.json` contains no JS tooling; do not add npm dependencies.
