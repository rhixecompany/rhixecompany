# RESEARCH_REPORT — profile

> **Type:** Project research report | **Updated:** 2026-07-10

**Type:** Django blog/CMS with cloud media storage
**Tech Stack:** Django 4.x, GCS, CKEditor 5, PostgreSQL, Docker, GCP, bleach/nh3
**Status:** Active

---

## Similar Projects

| Project | URL | Why Relevant |
|---------|-----|--------------|
| Wagtail CMS | <https://github.com/wagtail/wagtail> | leading Django CMS; StreamField for blogs/content |
| django-cms | <https://github.com/django-cms/django-cms> | enterprise Django CMS, mature plugin ecosystem |
| djangocms-text-ckeditor5 | <https://github.com/django-cms/djangocms-text-ckeditor5> | CKEditor 5 integration for django-cms |
| Django CMS with CKEditor | <https://github.com/MoTechStore/Django-CMS-With-CkEditor> | reference blog CMS implementation |

---

## Key Findings

### Django 4.2+ STORAGES Setting

- Unified `STORAGES` config dict introduced in Django 4.2 for storage backends
- `django-storages[google]` for GCS backend; requires `google-cloud-storage` extra
- Separate static vs media buckets recommended for ACL and caching control
- On Django ≥ 4.2: `STORAGES = {"default": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage", "OPTIONS": {...}}, "staticfiles": {...}}`
- On Django < 4.2: `DEFAULT_FILE_STORAGE` + `STATICFILES_STORAGE` globals

### CKEditor 5 Migration (2026)

- Complete rewrite from CKEditor 4 — different MVC architecture
- Use `@ckeditor/ckeditor5-build-classic` or custom builds via online builder
- Client-side sanitization only — **must** sanitize server-side with `bleach` or `nh3`
- `django-ckeditor-5` (hvlads) provides `CKEditor5Field`, `CKEditor5Widget`, image upload support
- Custom storage via `CKEDITOR_5_FILE_STORAGE` setting — can point to GCS
- `CKEDITOR_5_CONFIGS` for toolbar, plugins, image styles, table config
- `CKEDITOR_5_FILE_UPLOAD_PERMISSION` — "staff", "authenticated", "any"
- Automatic image cleanup on object update/delete (disabled by default)
- `CKEDITOR_5_ALLOW_ALL_FILE_TYPES = True` for non-image uploads (security warning!)
- JS callbacks in config via `callback:window.functionName` pattern

### GCS Integration (2026)

- `GS_BUCKET_NAME` + `GS_CREDENTIALS` + `STORAGES` dict configuration
- Use IAM service accounts (not user accounts); `GS_DEFAULT_ACL` + `GS_QUERYSTRING_AUTH`
- Signed URLs require IAM Sign Blob API (`iamcredentials.googleapis.com`)
- `GS_IAM_SIGN_BLOB=True` for signed URLs on Cloud Run (no private key file)
- `GS_SA_EMAIL` to override service account for signing
- Multiple buckets via custom storage classes subclassing `GoogleCloudStorage`
- `GS_BLOB_CHUNK_SIZE` for large file uploads (multiple of 256K)
- Fine-grained ACL required for `GS_DEFAULT_ACL='publicRead'`; otherwise use Uniform + `GS_QUERYSTRING_AUTH=False`
- `GS_EXPIRATION` default 1 day, max 7 days (v4 signed URLs)

### Django CMS Blog Patterns with Cloud Media Storage

- **Wagtail**: StreamField for flexible content blocks; built-in image/document management; Cloud Storage via `wagtail.storages` or `django-storages`
- **django-cms**: Plugin-based; `djangocms-text-ckeditor5` now has full CKEditor 5 support (April 2026); supports text-enabled CMS plugins
- **Custom Django**: `CKEditor5Field` + GCS storage; simpler but build everything yourself
- Media files in GCS: use separate buckets for public (static) vs private (uploads)
- Signed URLs for private media; public URLs for static assets with CDN

### Docker + GCP Deployment for Django (2026)

- **Cloud Run** + **Cloud SQL** (PostgreSQL) + **Cloud Build** + **Secret Manager** + **Artifact Registry**
- Multi-stage Dockerfile: build → runtime; Gunicorn with `uvicorn.workers.UvicornWorker`
- `CONN_MAX_AGE` + pgbouncer (via Cloud SQL proxy) for connection pooling
- Cloud SQL Auth Proxy in docker-compose for local dev
- Cloud Build `cloudmigrate.yaml` for build + migrate + collectstatic
- Secret Manager for `SECRET_KEY`, DB credentials, GCS bucket name
- `PORT` env var (Cloud Run default 8080) passed to Gunicorn
- Service account for Cloud Run with Cloud SQL Client, Secret Manager Accessor, Storage Object Viewer/Creator
- `gcloud run deploy` with `--set-cloudsql-instances`, `--set-secrets`, `--service-account`

### Django collectstatic to GCS Bucket Configuration

```python
# Django ≥ 4.2
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": "my-media-bucket",
            "project_id": "my-project",
            "default_acl": "publicRead",
            "querystring_auth": False,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": "my-static-bucket",
            "project_id": "my-project",
            "default_acl": "publicRead",
            "querystring_auth": False,
            "gzip": True,
            "gzip_content_types": ("text/css", "text/javascript", "application/javascript", "image/svg+xml"),
        },
    },
}
```

- Run `python manage.py collectstatic` — uploads to GCS bucket
- Separate buckets recommended: static (public, CDN, gzip) vs media (private, signed URLs)
- WhiteNoise alternative for static files if not using GCS

### Wagtail vs Custom Django CMS for Blog Platforms (2026)

| Aspect | Wagtail | django-cms | Custom Django + CKEditor 5 |
|--------|---------|------------|---------------------------|
| **Learning Curve** | Low (StreamField, great admin) | Medium (plugin architecture) | Low (just Django + field) |
| **Flexibility** | High (StreamField blocks) | High (plugins, placeholders) | Maximum (build anything) |
| **Content Editing** | Inline, preview, drafts | Frontend editing, plugins | Admin + CKEditor 5 widget |
| **Media Management** | Built-in (images, docs) | Via plugins (aldryn, filer) | Manual (GCS + CKEditor upload) |
| **Search** | Elasticsearch built-in | Via plugins | DIY |
| **Multi-site** | Native | Native | DIY |
| **Workflows** | Built-in | Built-in | DIY |
| **2026 Status** | Active, Wagtail 6.x | Active, django-cms 4.x | Full control |
| **Best For** | Content-heavy sites, blogs, news | Complex sites, marketing, multi-site | Simple blogs, full control needed |

**Key 2026 Insight**: django-cms now has full CKEditor 5 parity (djangocms-text-ckeditor5 0.48.0, April 2026) with text-enabled plugin support. Wagtail remains more developer-friendly for custom content structures.

---

## Cheatsheets & Quick Reference

| Topic | Resource | Type |
|-------|----------|------|
| django-storages GCS | <https://django-storages.readthedocs.io/en/latest/backends/gcloud.html> | Docs |
| Cloud Run Django codelab | <https://codelabs.developers.google.com/codelabs/cloud-run-djangocms> | Tutorial |
| GCS best practices | <https://cloud.google.com/storage/docs/best-practices> | Guide |
| CKEditor 5 Django | <https://github.com/hvlads/django-ckeditor-5> | Integration |
| Viget GCS Django article | <https://www.viget.com/articles/using-google-cloud-storage-in-your-django-project> | Article |
| Google Cloud Run Django | <https://docs.cloud.google.com/python/django/run> | Tutorial |
| Django CMS CKEditor 5 release | <https://www.django-cms.org/en/blog/2026/04/27/full-ckeditor-5-support-lands-in-djangocms-text> | Release Notes |
| Wagtail vs Django CMS | <https://blog.logrocket.com/comparing-wagtail-vs-django-cms> | Comparison |

---

## Best Practices

1. **Use `STORAGES` dict** — Django 4.2+ unified config for static/media backends
2. **Sanitize CKEditor output** — server-side with `bleach` or `nh3`; never `|safe`
3. **Separate buckets** — one for static files, one for user uploads
4. **Connection pooling** — `CONN_MAX_AGE` + pgbouncer for Cloud Run
5. **Custom CKEditor build** — trim unused features via online builder
6. **Signed URLs for private media** — IAM Sign Blob API on Cloud Run
7. **Cloud CDN** — in front of media bucket with long TTLs
8. **Django caching** — Redis/memcached for template fragment and queryset caching
9. **GCS object lifecycle** — auto-cleanup temp files
10. **Gunicorn async workers** — `--worker-class uvicorn.workers.UvicornWorker`
11. **Secret Manager** — never commit credentials; inject at runtime
12. **Multi-stage Docker** — build dependencies separate from runtime

---

## Common Pitfalls

| Pitfall | Impact | Avoidance |
|---------|--------|-----------|
| XSS via CKEditor | script injection | sanitize with bleach/nh3 server-side |
| Missing `[google]` extra | `django-storages` fails | `pip install django-storages[google]` |
| Static/media bucket confusion | ACL/caching chaos | separate buckets per purpose |
| Cloud Run DB exhaustion | 500 errors | `CONN_MAX_AGE` + pgbouncer |
| CKEditor 4→5 breakage | broken toolbar/plugins | full rewrite; test custom build |
| GCS Uniform ACL + publicRead | HTTP 400 on upload | use Fine-grained ACL or Uniform + `GS_QUERYSTRING_AUTH=False` |
| Signed URL expiry > 7 days | fails silently | max 604800 seconds (v4) |
| Default service account can't sign URLs | signed URLs fail | use IAM Sign Blob API or custom SA with key |

---

## Performance

1. **GCS CDN** — Cloud CDN in front of media bucket with long TTLs
2. **Django caching** — Redis/memcached for template fragment and queryset caching
3. **GCS object lifecycle** — auto-cleanup temp files
4. **gunicorn async workers** — `--worker-class uvicorn.workers.UvicornWorker`
5. **collectstatic with gzip** — `GS_IS_GZIPPED=True` + `GZIP_CONTENT_TYPES`
6. **Database connection pooling** — pgbouncer via Cloud SQL proxy
7. **CKEditor lazy loading** — load editor only on admin pages that need it

---

## Security

1. **Always sanitize CKEditor output** — server-side before rendering
2. **Restrict GCS IAM** — least-privilege service accounts; no public write
3. **SECURE_SSL_REDIRECT + HSTS** — enforce HTTPS
4. **django-csp** — restrict inline scripts in CKEditor content
5. **Custom CKEditor build** — exclude dangerous plugins (iframe, etc.)
6. **Signed URLs for private media** — short expiry, IAM Sign Blob API
7. **Secret Manager** — all secrets at runtime, never in code or Docker images
8. **CORS headers** — restrict to known origins for CKEditor uploads

---

## Related Projects (in workspace)

- **cookiecutter-django-tailwind** — shared layered Django settings
- **ecom** — Django monolith; Django + Docker + PostgreSQL overlap
- **rhixecompany-comics** — Django + Docker + PostgreSQL
- **xamehi.tv** — Django monolith; xamehi.tv adds React frontend
- **Django-Scrapy-Selenium** — Django + PostgreSQL scraping platform

---

## Resources

| Resource | URL | Description |
|----------|-----|-------------|
| Django Docs | <https://docs.djangoproject.com/en/4.2/> | Django 4.x documentation |
| GCS Docs | <https://cloud.google.com/storage/docs> | GCS best practices |
| django-ckeditor-5 | <https://github.com/hvlads/django-ckeditor-5> | CKEditor 5 integration |
| django-storages GCS | <https://django-storages.readthedocs.io/en/latest/backends/gcloud.html> | GCS backend docs |
| Viget GCS article | <https://www.viget.com/articles/using-google-cloud-storage-in-your-django-project> | Multi-bucket GCS patterns |
| Cloud Run Django | <https://docs.cloud.google.com/python/django/run> | Official GCP tutorial |
| Wagtail vs Django CMS | <https://blog.logrocket.com/comparing-wagtail-vs-django-cms> | 2024 comparison |
| Django CMS CKEditor 5 | <https://www.django-cms.org/en/blog/2026/04/27/full-ckeditor-5-support-lands-in-djangocms-text> | 2026 release notes |
| Corey Guitar Django Cloud Run | <https://www.coreyguitar.com/blog/8> | Docker + GCS + Cloud Run guide |

---

## New Research Findings (2026-07-10)

### Query 1: Django 4.x + Google Cloud Storage media handling 2026
- **STORAGES dict** is the modern API (Django 4.2+), replacing `DEFAULT_FILE_STORAGE` and `STATICFILES_STORAGE`
- `django-storages[google]` package provides `storages.backends.gcloud.GoogleCloudStorage`
- Critical settings: `GS_BUCKET_NAME`, `GS_CREDENTIALS` (service account), `GS_DEFAULT_ACL`, `GS_QUERYSTRING_AUTH`, `GS_IAM_SIGN_BLOB` for Cloud Run
- Multiple buckets via custom storage classes (see Viget article pattern)
- `GS_BLOB_CHUNK_SIZE` for large uploads (must be multiple of 256KB)

### Query 2: CKEditor 5 integration with Django admin patterns
- `django-ckeditor-5` (hvlads) is the active maintained package (v0.2.20)
- Provides `CKEditor5Field`, `CKEditor5Widget`, custom storage via `CKEDITOR_5_FILE_STORAGE`
- Configure via `CKEDITOR_5_CONFIGS` dict with toolbar, image, table, heading options
- `CKEDITOR_5_FILE_UPLOAD_PERMISSION` controls who can upload ("staff", "authenticated", "any")
- Custom upload view via `CK_EDITOR_5_UPLOAD_FILE_VIEW_NAME`
- Automatic image cleanup on model update/delete (opt-in)
- Server-side sanitization required: `bleach` or `nh3` — CKEditor 5 only does client-side

### Query 3: Django CMS blog patterns with cloud media storage
- **Wagtail**: Best for content-heavy blogs; StreamField = flexible blocks; built-in image/document management with cloud storage backends
- **django-cms**: Plugin architecture; `djangocms-text-ckeditor5` 0.48.0 (Apr 2026) has full CKEditor 5 parity including text-enabled plugins
- **Custom Django**: Maximum control; `CKEditor5Field` + GCS storage + manual admin setup
- For a profile/blog project, Wagtail or custom Django are lighter than django-cms

### Query 4: Docker + GCP deployment for Django applications
- **Cloud Run** is the recommended serverless platform (not App Engine Flex)
- **Cloud Build** with `cloudmigrate.yaml` for build → migrate → collectstatic → deploy
- **Cloud SQL PostgreSQL** with Cloud SQL Auth Proxy (local) and built-in proxy (Cloud Run)
- **Secret Manager** for all secrets (SECRET_KEY, DB creds, GCS bucket)
- **Service accounts** with least privilege: Cloud SQL Client, Secret Manager Accessor, Storage Object Creator/Viewer
- **Multi-stage Dockerfile**: builder stage (compile deps) → runtime stage (slim)
- **Gunicorn** with Uvicorn workers for async: `gunicorn --worker-class uvicorn.workers.UvicornWorker`

### Query 5: Django collectstatic to GCS bucket configuration
- Django 4.2+ uses `STORAGES["staticfiles"]` dict with `BACKEND` and `OPTIONS`
- `GS_DEFAULT_ACL="publicRead"` + `GS_QUERYSTRING_AUTH=False` for public static assets
- `GS_IS_GZIPPED=True` + `GZIP_CONTENT_TYPES` for automatic gzip
- Separate static bucket from media bucket (different caching/CDN policies)
- Run `collectstatic` in Cloud Build step or as Cloud Run Job

### Query 6: Wagtail vs custom Django CMS for blog platforms 2026
- **Choose Wagtail if**: content editors need flexible page structures, built-in workflows, multi-site, search, image management
- **Choose django-cms if**: complex plugin ecosystem needed, marketing integrations, versioning, multilingual built-in
- **Choose custom Django + CKEditor 5 if**: simple blog, full control desired, team knows Django well, minimal dependencies
- **2026 verdict**: Wagtail 6.x is most active; django-cms 4.x stable; custom is viable for simple needs

---

## Confidence Assessment

| Metric | Score |
|--------|-------|
| Source Diversity | 5/5 |
| Recency (2026 sources) | 5/5 |
| Factual Foundation | 5/5 |
| **Overall Confidence** | **High** |

---

## Follow-up Questions

1. What are the exact IAM roles needed for the Cloud Run service account to sign GCS URLs via IAM Sign Blob API?
2. How does `django-ckeditor-5` handle file uploads to GCS when using a custom storage class?
3. What's the recommended pgbouncer configuration for Cloud Run with Cloud SQL?
4. How to configure Cloud CDN cache keys for user-uploaded media vs static assets?
5. What's the migration path from CKEditor 4 to 5 for existing Django projects?