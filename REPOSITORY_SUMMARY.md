# REPOSITORY_SUMMARY.md

# Profile — Django Blog/CMS

**Generated:** 2026-07-25  
**Status:** Maintenance  
**Path:** `projects/profile/`

---

## Architecture

| Property | Value |
|----------|-------|
| **Type** | Django blog/CMS with cloud media storage |
| **Pattern** | Standard Django monolith with CBVs, GCS for media |
| **Reference** | [Workflow Analysis](../docs/Project_Architecture/Workflow_Analysis.md) |

Django 4.x + Google Cloud Storage + CKEditor 5. Blog/CMS with rich text editing, cloud-hosted media, and Docker/GCP deployment.

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django 4.x, Python 3.11+ |
| **Database** | PostgreSQL |
| **Media Storage** | Google Cloud Storage (GCS) |
| **Editor** | CKEditor 5 |
| **Infra** | Docker + GCP |

---

## Project Structure

```
profile/
├── requirements.txt
├── manage.py
├── profile/                  # Django project
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── blog/                     # Main app
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── templates/
├── media/                    # Local media (dev)
├── static/                   # Static files
├── docker-compose.yml
└── Dockerfile
```

---

## Commands

```bash
pip install -r requirements.txt
python manage.py migrate && python manage.py makemigrations
python manage.py collectstatic
python manage.py runserver
python manage.py test
```

---

## Conventions

- Class-Based Views (CBVs) preferred over FBVs
- `.env` — never commit; GCS credentials required
- Static/media files served via GCS in production
- Type hints in models and views
- `snake_case` for Python, `kebab-case` for URLs

---

## CI/CD

**Missing:** No project-level GitHub Actions workflow. Relies on root `pr-ci.yml` only.