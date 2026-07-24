# Profile — Technology Stack Blueprint

> **Project:** RhixeCompany Profile — Django Blog/CMS Portfolio Website
> **Stack tier:** LAMP-inspired (Django/Python + PostgreSQL + GCP)

---

## 1. Stack Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                     │
│  Django Templates  │  Bootstrap 4  │  CKEditor 4           │
│  HTML5  │  CSS3  │  JavaScript  │  crispy-forms           │
├─────────────────────────────────────────────────────────────┤
│                      APPLICATION LAYER                      │
│  Python 3.11+  │  Django 3.0.x  │  django-filter          │
│  django-storages  │  django-ckeditor  │  whitenoise        │
│  gunicorn  │  Pillow  │  django-environ                    │
├─────────────────────────────────────────────────────────────┤
│                      DATA LAYER                             │
│  SQLite (dev)  │  PostgreSQL (prod)  │  GCS (media)        │
│  psycopg2-binary  │  django-storages[google]               │
├─────────────────────────────────────────────────────────────┤
│                      INFRASTRUCTURE LAYER                   │
│  Docker  │  Cloud Run  │  Cloud SQL  │  Cloud Build        │
│  Google Secret Manager  │  Cloud SQL Auth Proxy            │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Backend Stack

### 2.1 Core Framework

| Technology | Version | Purpose | Justification |
|---|---|---|---|
| **Python** | 3.11+ | Runtime | Mature ecosystem, Django requires 3.8+ |
| **Django** | 3.0.x | Web framework | Batteries-included: ORM, admin, auth, forms, signals, templates |
| **Gunicorn** | — | WSGI server | Production-grade, Cloud Run compatible |

### 2.2 Django Packages

| Package | Version (req.txt) | Purpose |
|---|---|---|
| `Django` | latest | Core framework |
| `django-ckeditor` | latest | Rich text editing widget |
| `django-crispy-forms` | latest | Bootstrap 4 form rendering |
| `django-filter` | latest | QuerySet filtering for post listing |
| `django-js-asset` | latest | CKEditor JS asset helper |
| `django-storages` | latest | GCS/S3 storage backend |
| `django-storages[google]` | latest | Google Cloud Storage adapter |
| `django-environ` | latest | Environment variable management |
| `whitenoise` | latest | Static file serving in production |
| `Pillow` | latest | Image processing (thumbnails) |
| `psycopg2-binary` | latest | PostgreSQL adapter |

### 2.3 Other Python Dependencies

| Package | Purpose |
|---|---|
| `sqlparse` | SQL query formatting (Django debug toolbar dependency) |
| `pytz` | Timezone support |
| `python-dateutil` | Date parsing utilities |
| `urllib3` | HTTP client (underlying requests) |
| `s3transfer` | S3 transfer manager (storages dependency) |
| `jmespath` | JSON query language (storages dependency) |
| `docutils` | Documentation utilities |
| `six` | Python 2/3 compatibility shim |

---

## 3. Frontend Stack

| Technology | Role | Notes |
|---|---|---|
| **HTML5** | Structure | Django Template Language for server-side rendering |
| **CSS3** | Styling | 4 theme variants (blue, green, purple, default) |
| **JavaScript** | Interactivity | Custom `script.js` + CKEditor JS |
| **Bootstrap 4** | CSS framework | Rendered via `crispy-forms` with `bootstrap4` pack |
| **CKEditor 4** | Rich text editor | Full toolbar, image upload, self-hosted static distribution |
| **Django Templates** | Server-side rendering | Template inheritance (main.html → child templates) |

---

## 4. Database Stack

| Environment | Engine | Configuration |
|---|---|---|
| **Development** | SQLite 3 | `db.sqlite3` in project root — zero config |
| **Production** | PostgreSQL (Cloud SQL) | Via `rhixecompany/setting.py`, connection through Cloud SQL Auth Proxy |

### Database Models (4 tables + Django system tables)

| Model | Table (implied) | Key Fields |
|---|---|---|
| `Profile` | `base_profile` | user (FK→User), first_name, last_name, email, profile_pic, bio, twitter |
| `Tag` | `base_tag` | name |
| `Post` | `base_post` | headline, sub_headline, thumbnail, body (RichText), created, active, featured, slug, tags (M2M) |
| `PostComment` | `base_postcomment` | author (FK→Profile), post (FK→Post), body, created |

---

## 5. Infrastructure & DevOps

| Technology | Role | Details |
|---|---|---|
| **Docker** | Containerization | Base image built in `migrate.yaml` for Cloud Run |
| **Google Cloud Run** | Serverless hosting | Auto-scaling container platform |
| **Google Cloud SQL** | Managed PostgreSQL | Private network, Auth Proxy for secure connections |
| **Google Cloud Storage** | Static/media files | `publicRead` ACL, `django-storages[google]` backend |
| **Google Cloud Build** | CI/CD | `migrate.yaml` pipeline: build → proxy → migrate |
| **Google Secret Manager** | Secrets | `SECRET_KEY`, `ADMIN_PASSWORD`, `APPLICATION_SETTINGS` |
| **Cloud SQL Auth Proxy** | DB connectivity | Sidecar container pattern for secure Cloud SQL access |

### Deployment Pipeline

```
  git push
      │
      ▼
  Cloud Build (migrate.yaml)
      │
      ├── 1. Build Docker image with Cloud SQL Auth Proxy
      ├── 2. Start proxy tunnel to Cloud SQL
      ├── 3. Run `python manage.py makemigrations`
      ├── 4. Run `python manage.py migrate`
      └── 5. Deploy to Cloud Run
```

---

## 6. Development Tooling

| Tool | Configuration | Purpose |
|---|---|---|
| **VS Code** | `.vscode/settings.json` | Editor with Pylance, auto-format on save, organize imports |
| **Debugpy** | `.vscode/launch.json` | Django runserver debug configuration |
| **Pylance** | `.vscode/settings.json` | Python language server with basic type checking |
| **Python venv** | `venv/Scripts/python.exe` | Virtual environment (Windows) |
| **Git** | `.gitignore` | Version control with 3 branches: master, development, production |

### VS Code Settings Highlights

| Setting | Value |
|---|---|
| Default formatter | `ms-python.python` |
| Format on save | `true` |
| Organize imports on save | `explicit` |
| Python type checking | `basic` |
| File associations | `*.txt` → `django-txt`, `requirements/**` → `pip-requirements` |

---

## 7. Environment Variables

| Variable | Used By | Purpose |
|---|---|---|
| `SECRET_KEY` | `rhixecompany/setting.py` | Django secret key (Secret Manager) |
| `APPLICATION_SETTINGS` | Cloud Build + env | Full settings override as env var |
| `CLOUDRUN_SERVICE_URL` | `rhixecompany/setting.py` | Cloud Run hostname → ALLOWED_HOSTS |
| `DEBUG` | `rhixecompany/setting.py` | Debug toggle (default: false in prod) |
| `GS_BUCKET_NAME` | `rhixecompany/setting.py` | GCS bucket for static/media files |
| `USE_CLOUD_SQL_AUTH_PROXY` | migration step | Toggle proxy connection to Cloud SQL |
| `ADMIN_PASSWORD` | Cloud Build | Admin setup (Secret Manager) |
| `EMAIL_HOST_USER` | `settings.py` | Gmail SMTP username |
| `EMAIL_HOST_PASSWORD` | `settings.py` | Gmail SMTP password |

---

## 8. Version Map

| Layer | Technology | Version (approx.) |
|---|---|---|
| **Language** | Python | 3.11+ |
| **Framework** | Django | 3.0.x |
| **Database (dev)** | SQLite | 3.x |
| **Database (prod)** | PostgreSQL | 14+ (Cloud SQL) |
| **Frontend CSS** | Bootstrap | 4.x |
| **Rich text** | CKEditor | 4.x |
| **WSGI** | Gunicorn | 20.x |
| **Cloud** | Google Cloud Platform | (latest) |
| **Container** | Cloud Run | (managed) |

---

## 9. Stack Constraints & Trade-offs

| Constraint | Impact |
|---|---|
| **Django 3.0** (not 4.x/5.x) | Lacks modern async ORM, Redis cache, and some security defaults |
| **SQLite in dev** | No PostgreSQL-specific features testable locally; migration issues possible |
| **CKEditor 4** (not CKEditor 5) | Older editor, no real-time collaboration, larger bundle size |
| **FBVs instead of CBVs** | More repetitive code; AGENTS.md recommends CBVs but code uses FBVs |
| **No DRF** | No REST API — templates-only, no headless CMS capability |
| **No CI/CD tests** | Cloud Build runs migrations but no test step; `base/tests.py` is a stub |
| **Email as username** | Custom pattern using signals; could break if User model changes |

---

## 10. Mermaid Stack Diagram

```mermaid
graph TD
    subgraph "Frontend"
        HTML[HTML5 / DTL]
        CSS[CSS3 + Bootstrap 4]
        JS[JavaScript]
        CK[CKEditor 4]
    end
    
    subgraph "Backend"
        PY[Python 3.11+]
        DJ[Django 3.0.x]
        CRISPY[crispy-forms]
        FILTER[django-filter]
        CK_DJ[django-ckeditor]
        STOR[django-storages[google]]
        ENV[django-environ]
        GN[gunicorn]
    end
    
    subgraph "Data"
        SQLITE[SQLite - Dev]
        PG[PostgreSQL - Prod]
        GCS[Google Cloud Storage]
    end
    
    subgraph "Infra"
        GCR[Cloud Run]
        GCB[Cloud Build]
        GSM[Secret Manager]
        PROXY[Cloud SQL Auth Proxy]
        DOCKER[Docker]
    end
    
    HTML --> DJ
    CSS --> CRISPY
    JS --> DJ
    CK --> CK_DJ
    CK_DJ --> DJ
    CRISPY --> DJ
    FILTER --> DJ
    STOR --> DJ
    ENV --> DJ
    DJ --> SQLITE
    DJ --> PG
    PG --> PROXY
    STOR --> GCS
    GCB --> GCR
    GCR --> DOCKER
    GCR --> PROXY
    GSM --> DJ
```

---

*Generated from codebase inspection. Last updated: 2026-07-24.*
