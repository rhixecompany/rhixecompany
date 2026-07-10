# Copilot Instructions

Project-wide guidance for the profile/blog platform.

## Source of truth

- `projects/profile/AGENTS.md`
- `README.md`
- Django app files

## Commands

Run from the project root:

```bash
python -m venv .venv
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py makemigrations
python manage.py collectstatic
python manage.py check --deploy
python manage.py test
pytest
gunicorn profile.wsgi:application --bind 0.0.0.0:8000
```

## Architecture

- Django blog/profile app with posts, tags, comments, and admin editing.
- Rich text content uses CKEditor and template-based rendering.
- Media storage can use Google Cloud Storage or Amazon S3.

## Conventions

- Use Django model conventions (`__str__`, `Meta`, `get_absolute_url`).
- Prefer class-based views and app-level URL namespaces.
- Sanitize CKEditor HTML input carefully.
- Keep secrets in environment variables and never in code.
