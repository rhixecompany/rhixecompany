# Profile — Django Blog/CMS

## Architecture
- **Type:** Django blog/CMS with cloud media storage
- **Pattern:** Standard Django monolith with CBVs, GCS for media
- **Reference:** [Workflow Analysis](docs/Project_Architecture/Workflow_Analysis.md), [Exemplars](docs/Project_Architecture/exemplars.md)

Django 4.x + Google Cloud Storage + CKEditor 5. Blog/CMS with rich text editing, cloud-hosted media, and Docker/GCP deployment.

## Stack
- **Backend:** Django 4.x, Python 3.11+
- **Database:** PostgreSQL
- **Media Storage:** Google Cloud Storage (GCS)
- **Editor:** CKEditor 5
- **Infra:** Docker + GCP

## Commands
```bash
pip install -r requirements.txt
python manage.py migrate && python manage.py makemigrations
python manage.py collectstatic
python manage.py runserver
python manage.py test
```

## Conventions
- Class-Based Views (CBVs) preferred over FBVs
- `.env` — never commit; GCS credentials required
- Static/media files served via GCS in production
- Type hints in models and views
- `snake_case` for Python, `kebab-case` for URLs

## Notes
- GCS bucket credentials required in `.env`
- `collectstatic` uploads to GCS bucket
- CKEditor 5 for rich text content management
