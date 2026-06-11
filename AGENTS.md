# Profile - Django Blog/CMS Context

Django blog/profile CMS with Google Cloud Storage and CKEditor.

## Architecture
- **Framework**: Django 4.x
- **Language**: Python 3.11+
- **Database**: PostgreSQL
- **Storage**: Google Cloud Storage (media files)
- **Editor**: CKEditor 5
- **Deployment**: Docker + GCP

## Conventions
- PEP 8, type hints everywhere
- Django Class-Based Views
- Templates in `templates/`
- Static files via GCS
- Environment variables in `.env`

## Commands
```bash
# Dev server
pip install -r requirements.txt
python manage.py runserver

# Database
python manage.py migrate
python manage.py makemigrations

# Collect static
python manage.py collectstatic

# Tests
python manage.py test
```

## Important Notes
- GCS credentials in `.env` — never commit
- CKEditor config in `ckeditor/` directory
- Media uploads go to GCS bucket