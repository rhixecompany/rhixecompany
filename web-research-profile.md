# Web Research — Profile Project

> **Generated:** 2026-07-16
> **Methodology:** Web search (web_search) + content extraction (web_extract) from real sources
> **Target Stack:** PostgreSQL, Python (Django), CKEditor, Docker, GCS (Google Cloud Storage)

---

## Table of Contents

1. [Search Queries Executed](#search-queries-executed)
2. [Django + PostgreSQL Best Practices](#django--postgresql-best-practices)
3. [CKEditor Integration & Security](#ckeditor-integration--security)
4. [Google Cloud Storage (GCS) for Django](#google-cloud-storage-gcs-for-django)
5. [Docker + Django Production Deployment](#docker--django-production-deployment)
6. [Django Security (OWASP)](#django-security-owasp)
7. [Cross-Cutting Pitfalls](#cross-cutting-pitfalls)
8. [Source Index](#source-index)

---

## Search Queries Executed

| # | Query | Source Count |
|---|-------|-------------|
| 1 | `Django PostgreSQL best practices performance optimization 2024 2025` | 10 results |
| 2 | `Django CKEditor integration best practices configuration` | 10 results |
| 3 | `Django Google Cloud Storage GCS static media files configuration` | 10 results |
| 4 | `Django Docker production deployment best practices 2025` | 10 results |
| 5 | `Django security best practices cheatsheet common pitfalls 2024` | 10 results |
| 6 | `CKEditor security XSS prevention Django sanitize HTML content` | 8 results |
| 7 | `Django CKEditor Google Cloud Storage django-storages configuration` | 8 results |
| 8 | `Django PostgreSQL connection pooling CONN_MAX_AGE pgbouncer performance production` | 8 results |

---

## Django + PostgreSQL Best Practices

### 1. Connection Pooling & Persistent Connections

Efficiently managing database connections is critical for production performance.

- **`CONN_MAX_AGE`**: Set to `600` (10 minutes) to reuse connections and reduce overhead. This avoids creating a new connection per request.
- **Connection Pooling**: Libraries like `django-postgres-pool` and `psycopg2-binary` provide connection pooling. For high-traffic apps, use **PgBouncer** as a standalone lightweight connection pooler.
- **SSL connections**: Enforce SSL/TLS between Django and PostgreSQL in production with `OPTIONS = {'sslmode': 'require'}`.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {'sslmode': 'require'},
    }
}
```

**Source:** [10 Best Practices for Optimizing Django with PostgreSQL in Production (Python in Plain English, Nov 2024)](https://python.plainenglish.io/10-best-practices-for-optimizing-django-with-postgresql-in-production-fbb45bb72e0f)

### 2. Strategic Indexing

- Django automatically indexes primary keys and foreign keys.
- Add custom indexes via `Meta.indexes` for frequently filtered/sorted columns.
- Partial indexes (`condition=Q(...)`) for filtered queries on large tables.

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created_at'], name='idx_created_desc'),
        ]
```

**Source:** [10 Tips to Optimize PostgreSQL Queries in Django (GitGuardian Blog)](https://blog.gitguardian.com/10-tips-to-optimize-postgresql-queries-in-your-django-project)

### 3. ORM Efficiency

- **Avoid N+1 queries**: Use `select_related` (for ForeignKey/OneToOne) and `prefetch_related` (for ManyToMany/reverse FK).
- **Bulk operations**: `bulk_create()`, `bulk_update()`, `update_or_create()` for batch processing.
- **Only load what you need**: `.only()`, `.defer()` to limit columns, `.values()`/`.values_list()` for dict/tuple output.
- **Use `explain`**: `queryset.explain()` shows the PostgreSQL query plan (Django 2.1+).

### 4. Migration Safety in Production

- **Review migrations** before deploying — watch for `ALTER TABLE` on large tables.
- **Schedule during low traffic**: `RunPython` operations with large data migrations can lock tables.
- **Wrap in transactions**: Django wraps each migration in a transaction by default.
- **Zero-downtime tools**: `django-pgzero-downtime-migrations` for operations on large tables.

### 5. Monitoring & Tooling

- **Django Debug Toolbar**: `pip install django-debug-toolbar` — inspect SQL queries, cache, templates.
- **pg_stat_activity**: Monitor running queries, find long-running or blocked queries.
- **pgAdmin / Grafana**: Real-time performance monitoring dashboards.
- **Log slow queries**: Configure `log_min_duration_statement` in PostgreSQL.

### 6. Backups & Disaster Recovery

- **Automated backups**: `pg_dump -U user -h host -W -F c db_name > backup.bak`
- **Replication**: Streaming replication for high availability.
- **Point-in-time recovery (PITR)**: Configure WAL archiving.

---

## CKEditor Integration & Security

### ⚠️ Deprecation Notice — django-ckeditor (CKEditor 4)

The author of `django-ckeditor` has **explicitly deprecated the package**:

> *"I do not recommend using this package anymore since the open source version of CKEditor 4 has unfixed security issues."* — [django-ckeditor README](https://github.com/django-ckeditor/django-ckeditor)

Alternatives recommended by the author:
- **[django-prose-editor](https://406.ch/writing/django-prose-editor-prose-editing-component-for-the-django-admin/)** — modern replacement
- **[django-ckeditor-5](https://github.com/hvlads/django-ckeditor-5)** — CKEditor 5 integration (hvlads)

### Recommended: django-ckeditor-5 (CKEditor 5)

**Installation:**
```bash
pip install django-ckeditor-5
```

**settings.py:**
```python
INSTALLED_APPS = [
    ...
    'django_ckeditor_5',
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload'],
    },
    'extends': {
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic',
                    'link', 'underline', 'strikethrough', 'code', 'subscript',
                    'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing',
                    'insertImage', 'bulletedList', 'numberedList', 'todoList', '|',
                    'blockQuote', 'imageUpload', '|', 'fontSize', 'fontFamily',
                    'fontColor', 'fontBackgroundColor', 'mediaEmbed',
                    'removeFormat', 'insertTable'],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter',
                        'imageStyle:side', '|'],
            'styles': ['full', 'side', 'alignLeft', 'alignRight', 'alignCenter'],
        },
    },
}

# Optional: custom file storage for CKEditor uploads
CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage"

# Optional: auto-detect user language
CKEDITOR_5_USER_LANGUAGE = True
```

**models.py:**
```python
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Article(models.Model):
    title = models.CharField('Title', max_length=200)
    body = CKEditor5Field('Body', config_name='extends')
```

**urls.py:**
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Source:** [django-ckeditor-5 GitHub (hvlads)](https://github.com/hvlads/django-ckeditor-5) | [django-ckeditor (deprecated)](https://github.com/django-ckeditor/django-ckeditor)

### CRITICAL: Server-Side HTML Sanitization

CKEditor only sanitizes on the **client side**. A malicious user can bypass the editor and POST raw HTML directly. You **must** sanitize server-side.

**Do NOT rely on `|safe` alone** — always sanitize before storing or rendering:

```python
import bleach

# Whitelist approach — only allow safe tags/attributes
allowed_tags = ['p', 'br', 'strong', 'em', 'a', 'ul', 'ol', 'li',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'blockquote',
                'pre', 'code', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
                'figure', 'figcaption', 'span', 'div', 'hr', 'sub', 'sup']

allowed_attributes = {
    'a': ['href', 'title', 'rel', 'target'],
    'img': ['src', 'alt', 'width', 'height', 'class'],
    '*': ['class', 'id', 'style'],
}

clean_html = bleach.clean(
    raw_html,
    tags=allowed_tags,
    attributes=allowed_attributes,
    strip=True
)
```

Alternatively, use **`nh3`** (ammonia) — a Rust-based HTML sanitizer that is faster and stricter:
```python
import nh3
clean_html = nh3.clean(raw_html)
```

**Source:** [Preventing XSS in Django (Snyk)](https://snyk.io/blog/preventing-xss-in-django) | [How to prevent XSS attacks with WYSIWYG editors (Stack Overflow)](https://stackoverflow.com/questions/6830800/how-to-prevent-xss-attacks-when-i-need-to-render-html-from-a-wysiwyg-editor)

### CKEditor Security Tips

1. **Disable Source mode** if users shouldn't edit raw HTML — remove `sourceEditing` from toolbar
2. **Restrict file uploads**: `CKEDITOR_ALLOW_NONIMAGE_FILES = False`
3. **Restrict by user**: `CKEDITOR_RESTRICT_BY_USER = True` — users only see their own uploads
4. **Restrict by date**: `CKEDITOR_RESTRICT_BY_DATE = True` — organize uploads by date folders
5. **Custom file storage**: `CKEDITOR_5_FILE_STORAGE` sets GCS storage for uploaded images
6. **Use `{{ content|safe }}`** in templates to render CKEditor HTML — but only AFTER sanitization

---

## Google Cloud Storage (GCS) for Django

### Installation

```bash
pip install django-storages[google]
```

### Django 4.2+ STORAGES Configuration

Django 4.2 introduced the unified `STORAGES` dict. Replace the older `DEFAULT_FILE_STORAGE` and `STATICFILES_STORAGE` settings:

```python
# settings.py

from google.oauth2 import service_account

GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID')
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
)
GS_DEFAULT_ACL = 'publicRead'
GS_QUERYSTRING_AUTH = False  # Set to True for private files
GS_BLOB_CHUNK_SIZE = 1024 * 256 * 40  # For large files

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'OPTIONS': {
            'bucket_name': GS_BUCKET_NAME,
            'project_id': GS_PROJECT_ID,
            'credentials': GS_CREDENTIALS,
            'default_acl': 'publicRead',
            'querystring_auth': False,
        },
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.gcloud.GoogleCloudStorage',
        'OPTIONS': {
            'bucket_name': GS_BUCKET_NAME,
            'project_id': GS_PROJECT_ID,
            'credentials': GS_CREDENTIALS,
            'default_acl': 'publicRead',
            'querystring_auth': False,
            'location': 'static',
        },
    },
}

MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
```

**Source:** [django-storages GCS Backend Docs](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html) | [Configure Django and Google Cloud Storage (Stack Overflow)](https://stackoverflow.com/questions/34247702/configure-django-and-google-cloud-storage)

### Authentication Methods

1. **IAM Service Account (Recommended for Cloud Run/GCE/GKE)**
   - Create a service account with `Storage Admin` role
   - The `GOOGLE_APPLICATION_CREDENTIALS` env var points to the JSON key
   - On Cloud Run, the default service account is used automatically

2. **IAM Sign Blob API (For Signed URLs on Cloud Run)**
   - Set `GS_IAM_SIGN_BLOB = True`
   - Required because Cloud Run doesn't have access to a private key file
   - Uses IAM API to generate signed URLs

3. **HMAC Keys (Legacy/Interoperability)**
   - Only needed for S3-compatible tooling
   - Not recommended for new projects

### Multiple Bucket Support

For separate public/private buckets, subclass the storage backend:

```python
from storages.backends.gcloud import GoogleCloudStorage
from django.conf import settings
from urllib.parse import urljoin
from django.utils.deconstruct import deconstructible

@deconstructible
class GoogleCloudMediaStorage(GoogleCloudStorage):
    """Storage for user-uploaded media files."""
    def __init__(self, *args, **kwargs):
        kwargs['bucket_name'] = settings.GS_MEDIA_BUCKET_NAME
        super().__init__(*args, **kwargs)

    def url(self, name):
        return urljoin(settings.MEDIA_URL, name)

@deconstructible
class GoogleCloudStaticStorage(GoogleCloudStorage):
    """Storage for collected static files."""
    def __init__(self, *args, **kwargs):
        kwargs['bucket_name'] = settings.GS_STATIC_BUCKET_NAME
        super().__init__(*args, **kwargs)

    def url(self, name):
        return urljoin(settings.STATIC_URL, name)
```

**Source:** [Using Google Cloud Storage in Your Django Project (Viget, Jun 2022)](https://www.viget.com/articles/using-google-cloud-storage-in-your-django-project)

### Bucket Permissions (IAM)

| Principal | Role | Purpose |
|-----------|------|---------|
| Service Account | `Storage Admin` (roles/storage.admin) | Full control for app |
| `allUsers` | `Storage Legacy Object Reader` | Public read access |
| `allAuthenticatedUsers` | `Storage Object Viewer` | Read for authenticated users only |

> **Note**: Use `fine-grained` access control (not Uniform) if using `GS_DEFAULT_ACL`.

### CKEditor + GCS Integration

For CKEditor 5 uploads to GCS specifically:

```python
# settings.py
CKEDITOR_5_FILE_STORAGE = "myapp.storage.CustomGCSStorage"
```

```python
# storage.py
from storages.backends.gcloud import GoogleCloudStorage

class CustomGCSStorage(GoogleCloudStorage):
    """Custom storage for django_ckeditor_5 images on GCS."""
    def __init__(self, *args, **kwargs):
        kwargs['bucket_name'] = settings.GS_MEDIA_BUCKET_NAME
        kwargs['default_acl'] = 'publicRead'
        kwargs['location'] = 'ckeditor_uploads/'
        super().__init__(*args, **kwargs)
```

**Source:** [django-ckeditor-5 — Custom Storage Example](https://github.com/hvlads/django-ckeditor-5)

---

## Docker + Django Production Deployment

### Multi-Stage Dockerfile

```dockerfile
# === BUILDER STAGE ===
FROM python:3.12-slim-bullseye as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y \
    gcc postgresql-client libpq-dev gettext \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements/production.txt .
RUN pip install --upgrade pip && pip install -r production.txt

# === RUNTIME STAGE ===
FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN groupadd -r django && useradd -r -g django django

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=django:django ./app /app

RUN mkdir -p /app/staticfiles /app/media && \
    chown -R django:django /app/staticfiles /app/media

USER django
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

**Source:** [Production-Ready Django with Docker in 2026 (Medium, Jan 2026)](https://medium.com/@sizanmahmud08/production-ready-django-with-docker-in-2026-complete-guide-with-nginx-postgresql-and-best-1fb248e65983)

### Docker Compose Best Practices

- Use **separate compose files**: `docker-compose.yml` for dev, `docker-compose.prod.yml` for production
- **Environment variables**: Use `.env` file + `env_file` directive in services
- **Health checks**: Add Docker `healthcheck` to the web service
- **Volumes**: Named volumes for database persistence and media files
- **Networks**: Isolate services on an internal network

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env.prod
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${DB_USER} -d $${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build:
      context: .
      dockerfile: docker/django/Dockerfile
    env_file:
      - .env.prod
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8000/health/"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s

  nginx:
    image: nginx:alpine
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Essential Docker Practices

| Practice | Details |
|----------|---------|
| **Non-root user** | `groupadd -r django && useradd -r -g django django` |
| **Slim base images** | `python:3.12-slim-bullseye` instead of `python:3.12` |
| **Multi-stage builds** | Separate build deps (gcc) from runtime deps |
| **`.dockerignore`** | Exclude `.git`, `__pycache__`, `.env`, `.vscode` |
| **Entrypoint script** | Run `collectstatic`, `migrate` before `exec "$@"` |
| **Environment config** | Never hardcode credentials; use `os.environ.get()` |
| **Health checks** | Docker healthcheck + Django `/health/` endpoint |

**Source:** [Django Docker Best Practices: 7 Dos and Don'ts (Better Stack, Feb 2025)](https://betterstack.com/community/guides/scaling-python/django-docker-best-practices)

### Health Check Endpoint

```python
# health/views.py
from django.http import JsonResponse
from django.db import connections

def health_check(request):
    db_ok = all(
        conn.cursor().execute("SELECT 1")
        for conn in connections.all()
    )
    status = db_ok
    return JsonResponse(
        {"status": "ok" if status else "unhealthy"},
        status=200 if status else 503
    )
```

---

## Django Security (OWASP)

Based on the **[OWASP Django Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html)**:

### Settings Checklist

```python
# settings.py — Security Checklist

# Never debug in production
DEBUG = False

# Secret key via env var
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Allowed hosts
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# Security Middleware (order matters)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # First!
    # ...
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

# HTTPS & HSTS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'  # or 'SAMEORIGIN'

# Proxy support (Django behind nginx/GCLB)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Authentication Hardening

```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Rate limiting (django-ratelimit)
# Brute-force protection (django-axes)
INSTALLED_APPS += ['axes', 'ratelimit']
```

### Admin Panel Hardening

```python
# urls.py
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('manage-secret-panel/', admin.site.urls),  # NOT /admin/
]
```

### CSP (Content Security Policy)

Django doesn't ship CSP by default. Use `django-csp`:

```python
INSTALLED_APPS += ['csp']

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "https://cdn.ckeditor.com")
CSP_IMG_SRC = ("'self'", "https://storage.googleapis.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # CKEditor needs inline styles
```

### Built-in Security Check

```bash
python manage.py check --deploy
```

This command checks your settings against Django's security checklist. Address all warnings before production deployment.

**Source:** [OWASP Django Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html) | [Django Security Tips (Snyk)](https://snyk.io/blog/django-security-tips)

---

## Cross-Cutting Pitfalls

| # | Pitfall | Stack Layer | Impact | Mitigation |
|---|---------|-------------|--------|------------|
| 1 | **Using deprecated django-ckeditor (CKEditor 4)** | CKEditor | Unfixed CVEs, XSS | Migrate to django-ckeditor-5 or django-prose-editor |
| 2 | **Client-only HTML sanitization** | CKEditor | Stored XSS | Always sanitize server-side with bleach/nh3 |
| 3 | **Hardcoded SECRET_KEY in settings.py** | Django | Cryptographic weakness | Env variable, 50+ random chars |
| 4 | **DEBUG = True in production** | Django | Information disclosure | Never set DEBUG=True in production |
| 5 | **Shared static/media bucket** | GCS | ACL conflicts, over-permission | Separate buckets per purpose |
| 6 | **Missing IAM Sign Blob API** | GCS/GCP | Signed URLs fail on Cloud Run | Set `GS_IAM_SIGN_BLOB = True` |
| 7 | **No SSL between Django and PostgreSQL** | PostgreSQL | Data in transit exposure | `sslmode=require` in DATABASES OPTIONS |
| 8 | **Docker as root user** | Docker | Container escape risk | Always use non-root user in Dockerfile |
| 9 | **No connection pooling** | PostgreSQL | Connection exhaustion under load | `CONN_MAX_AGE=600` + PgBouncer |
| 10 | **Running on default /admin/** | Django | Brute-force target | Change admin URL |
| 11 | **No health checks** | Docker/Django | Silent failures | Implement health endpoint + Docker healthcheck |
| 12 | **Caching not configured** | Django | Slow page loads | Add Redis/ElastiCache |
| 13 | **Missing .dockerignore** | Docker | Bloated images, slow builds | Exclude git, caches, local env files |
| 14 | **collectstatic not automated** | Django/GCS | Stale static files | Run in entrypoint script |

---

## Performance Tips Summary

| Area | Tip | Why |
|------|-----|-----|
| **PostgreSQL** | `CONN_MAX_AGE=600` + PgBouncer | Reduces connection overhead |
| **PostgreSQL** | Partial indexes on filtered queries | Smaller, faster indexes |
| **PostgreSQL** | `select_related` / `prefetch_related` | Eliminates N+1 queries |
| **GCS** | `GS_BLOB_CHUNK_SIZE` for uploads | Efficient streaming for large files |
| **GCS** | CDN (Cloud CDN) in front of bucket | Edge-cached media delivery |
| **CKEditor** | Lazy toolbar configuration | Don't load plugins you don't need |
| **Django** | Redis caching + cache invalidation on publish | Reduce database load |
| **Django** | Gzip middleware | Smaller responses |
| **Docker** | Multi-stage builds | Smaller images (~200MB vs 1GB) |
| **Docker** | `workers = (2 × CPU) + 1` (Gunicorn) | Optimal concurrency |

---

## Source Index

| Source | URL | Type | Topics |
|--------|-----|------|--------|
| Django + PostgreSQL Best Practices | [python.plainenglish.io](https://python.plainenglish.io/10-best-practices-for-optimizing-django-with-postgresql-in-production-fbb45bb72e0f) | Blog (Nov 2024) | PostgreSQL, Django ORM |
| PostgreSQL Query Optimization | [blog.gitguardian.com](https://blog.gitguardian.com/10-tips-to-optimize-postgresql-queries-in-your-django-project) | Blog | PostgreSQL, Query Optimization |
| django-ckeditor (deprecated) | [github.com/django-ckeditor](https://github.com/django-ckeditor/django-ckeditor) | GitHub Repo | CKEditor 4, Deprecation |
| django-ckeditor-5 | [github.com/hvlads/django-ckeditor-5](https://github.com/hvlads/django-ckeditor-5) | GitHub Repo | CKEditor 5, Integration |
| django-storages GCS Backend | [django-storages.readthedocs.io](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html) | Docs | GCS, Storage Configuration |
| Django + GCS Config | [stackoverflow.com](https://stackoverflow.com/questions/34247702/configure-django-and-google-cloud-storage) | Stack Overflow | GCS, IAM, Buckets |
| GCS in Django Project | [viget.com](https://www.viget.com/articles/using-google-cloud-storage-in-your-django-project) | Blog (Jun 2022) | GCS, Multiple Buckets |
| Django Docker Best Practices | [betterstack.com](https://betterstack.com/community/guides/scaling-python/django-docker-best-practices) | Guide (Feb 2025) | Docker, Compose, Security |
| Production Django + Docker | [medium.com/@sizanmahmud08](https://medium.com/@sizanmahmud08/production-ready-django-with-docker-in-2026-complete-guide-with-nginx-postgresql-and-best-1fb248e65983) | Blog (Jan 2026) | Docker, Nginx, Gunicorn |
| OWASP Django Security Cheat Sheet | [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html) | Cheat Sheet | Security Hardening |
| Preventing XSS in Django | [snyk.io](https://snyk.io/blog/preventing-xss-in-django) | Blog | XSS, Sanitization |
| Django Security Tips | [snyk.io](https://snyk.io/blog/django-security-tips) | Blog | Security Checklist |
| XSS with WYSIWYG Editors | [stackoverflow.com](https://stackoverflow.com/questions/6830800/how-to-prevent-xss-attacks-when-i-need-to-render-html-from-a-wysiwyg-editor) | Stack Overflow | XSS, HTML Sanitization |

---

## Research Methodology

- **web_search**: 8 queries across PostgreSQL, CKEditor, GCS, Docker, and Security domains
- **web_extract**: Deep content extraction from 8 primary sources (GitHub repos, docs sites, blogs, Stack Overflow)
- **Cross-referencing**: Verified CKEditor deprecation notice directly from the source repo
- **Date context**: Searches returned results from 2022–2026; older results were deprioritized
- **Tools used**: `web_search`, `web_extract`
