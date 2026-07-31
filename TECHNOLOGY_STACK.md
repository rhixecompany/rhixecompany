# 🏗 Technology Stack Blueprint - profile

**Project Path:** `projects/profile`
**Generated:** 2026-07-28
**Status:** Maintenance — Django Blog/CMS with GCS

---

## Core Technologies

| Category | Technology | Version | License |
|----------|-----------|---------|---------|
| **Framework** | Django | 4.x | BSD |
| **Language** | Python | 3.11+ | PSF |
| **Database** | PostgreSQL | Latest | PostgreSQL |
| **Media Storage** | Google Cloud Storage | - | - |
| **Rich Text Editor** | CKEditor 5 | Latest | GPL |
| **WSGI** | Gunicorn | Latest | MIT |
| **Static Files** | WhiteNoise | Latest | MIT |
| **Environment** | django-environ | Latest | MIT |

---

## Dependencies (`requirements.txt`)

```text
Django
django-ckeditor
django-crispy-forms
django-filter
django-js-asset
django-storages
docutils
gunicorn
jmespath
Pillow
psycopg2-binary
python-dateutil
pytz
s3transfer
six
sqlparse
urllib3
whitenoise
django-storages[google]
django-environ
```

---

## Project Structure

```
profile/
├── blog/                    # Main blog app
│   ├── models.py           # Post, Category, Tag models
│   ├── views.py            # CBVs: ListView, DetailView, CreateView
│   ├── forms.py            # CKEditor forms
│   └── admin.py            # Admin customization
├── config/                  # Django settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   └── urls.py
├── media/                   # Local media (dev only)
├── static/                  # Static files
├── templates/
│   └── blog/
│       ├── post_list.html
│       ├── post_detail.html
│       └── post_form.html
├── manage.py
├── requirements.txt
└── Dockerfile
```

---

## Key Features

### 1. Rich Text Editing (CKEditor 5)
```python
# settings/base.py
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', 'imageUpload'],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft', 'imageStyle:alignCenter', 'imageStyle:alignRight'],
            'styles': ['full', 'side']
        }
    }
}
```

### 2. Google Cloud Storage Integration
```python
# settings/production.py
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = env('GCS_BUCKET_NAME')
GS_PROJECT_ID = env('GCS_PROJECT_ID')
GS_CREDENTIALS = env('GCS_CREDENTIALS')  # Service account JSON
```

### 3. Class-Based Views Pattern
```python
# blog/views.py
class PostListView(ListView):
    model = Post
    paginate_by = 10
    queryset = Post.objects.published().select_related('author').prefetch_related('tags')

class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.published()

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'categories', 'tags', 'status']
    success_url = reverse_lazy('blog:post_list')
```

---

## Configuration

### Environment Variables (`.env`)
```env
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgres://user:pass@host:5432/dbname

# Google Cloud Storage
GCS_BUCKET_NAME=your-bucket
GCS_PROJECT_ID=your-project
GCS_CREDENTIALS={"type": "service_account", ...}

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
```

### Settings Hierarchy
```
base.py (shared)
    ├── local.py (DEBUG=True, SQLite, console email)
    └── production.py (DEBUG=False, PostgreSQL, GCS, Gunicorn)
```

---

## Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Database
python manage.py migrate
python manage.py createsuperuser

# Development
python manage.py runserver

# Production
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Testing
python manage.py test
```

---

## Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports: ["8000:8000"]
    environment:
      - DEBUG=False
    env_file: .env
  
  db:
    image: postgres:15
    volumes: [postgres_data:/var/lib/postgresql/data]
    env_file: .env
```

---

## Coding Conventions

| Convention | Standard |
|------------|----------|
| **Views** | CBVs preferred over FBVs |
| **Models** | `snake_case` fields, `PascalCase` classes |
| **URLs** | `kebab-case` paths |
| **Templates** | `app/model_action.html` |
| **Type Hints** | Required in new code |
| **Imports** | `isort` style (stdlib → third-party → local) |
| **Formatting** | Black (line-length: 119) |

---

## CI/CD

**Workflow:** `.github/workflows/profile-ci.yml`

1. **Install** → `pip install -r requirements.txt`
2. **Lint** → `ruff check .` + `djlint templates/`
3. **Type Check** → `mypy --config-file pyproject.toml .`
4. **Test** → `pytest` / `python manage.py test`
5. **Build** → Docker image

---

## Maintenance Notes

- **CKEditor 5** requires GPL license compliance if distributing
- **GCS credentials** must be mounted as secret in production
- **Static files** served by WhiteNoise in production, Django dev server in local
- **Media files** stored in GCS bucket (not in repo)

---

*Generated by Hermes Agent Technology Stack Blueprint Generator*