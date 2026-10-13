# /rhixecompany/ AGENTS.md

## OVERVIEW
Django project configuration.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Settings | rhixecompany/settings.py | Canonical configuration |
| Routing | rhixecompany/urls.py | Root URL routing |
| Entry | wsgi.py / asgi.py | Deployment entry points |

## CONVENTIONS
- Only edit `settings.py` for config.
- `setting.py` is an override; do not edit unless explicitly required for deployment.

## ANTI-PATTERNS
- Do not add new applications to `settings.py` without verifying path in `manage.py`.
