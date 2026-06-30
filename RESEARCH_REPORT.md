# RESEARCH_REPORT — profile

> **Type:** Project research report | **Updated:** 2026-06-29

**Type:** Django blog/CMS with cloud media storage
**Tech Stack:** Django 4.x, GCS, CKEditor 5, PostgreSQL, Docker, GCP, bleach/nh3
**Status:** Active

---

## Similar Projects

| Project | URL | Why Relevant |
|---------|-----|--------------|
| Wagtail CMS | https://github.com/wagtail/wagtail | leading Django CMS; StreamField for blogs/content |
| django-cms | https://github.com/django-cms/django-cms | enterprise Django CMS, mature plugin ecosystem |
| djangocms-text-ckeditor5 | https://github.com/django-cms/djangocms-text-ckeditor5 | CKEditor 5 integration for django-cms |
| Django CMS with CKEditor | https://github.com/MoTechStore/Django-CMS-With-CkEditor | reference blog CMS implementation |

---

## Key Findings

### Django 4.2+ STORAGES Setting
- Unified `STORAGES` config dict introduced in Django 4.2 for storage backends
- `django-storages[google]` for GCS backend; requires `google-cloud-storage` extra
- Separate static vs media buckets recommended for ACL and caching control

### CKEditor 5 Migration (2026)
- Complete rewrite from CKEditor 4 — different MVC architecture
- Use `@ckeditor/ckeditor5-build-classic` or custom builds via online builder
- Client-side sanitization only — **must** sanitize server-side with `bleach` or `nh3`

### GCS Integration
- `GS_BUCKET_NAME` + `GS_CREDENTIALS` + `STORAGES` dict configuration
- Use IAM service accounts (not user accounts); `GS_DEFAULT_ACL` + `GS_QUERYSTRING_AUTH`
- Signed URLs require IAM Sign Blob API (`iamcredentials.googleapis.com`)

### Deployment
- Cloud Run + Cloud SQL with `CONN_MAX_AGE` + pgbouncer for connection pooling
- Scaling can overwhelm DB connections without pooling

---

## Cheatsheets & Quick Reference

| Topic | Resource | Type |
|-------|----------|------|
| django-storages GCS | https://django-storages.readthedocs.io/en/latest/backends/gcloud.html | Docs |
| Cloud Run Django codelab | https://codelabs.developers.google.com/codelabs/cloud-run-djangocms | Tutorial |
| GCS best practices | https://cloud.google.com/storage/docs/best-practices | Guide |
| CKEditor 5 Django | https://github.com/solaris17/django-ckeditor-5 | Integration |

---

## Best Practices

1. **Use `STORAGES` dict** — Django 4.2+ unified config for static/media backends
2. **Sanitize CKEditor output** — server-side with `bleach` or `nh3`; never `|safe`
3. **Separate buckets** — one for static files, one for user uploads
4. **Connection pooling** — `CONN_MAX_AGE` + pgbouncer for Cloud Run
5. **Custom CKEditor build** — trim unused features via online builder

---

## Common Pitfalls

| Pitfall | Impact | Avoidance |
|---------|--------|-----------|
| XSS via CKEditor | script injection | sanitize with bleach/nh3 server-side |
| Missing `[google]` extra | `django-storages` fails | `pip install django-storages[google]` |
| Static/media bucket confusion | ACL/caching chaos | separate buckets per purpose |
| Cloud Run DB exhaustion | 500 errors | `CONN_MAX_AGE` + pgbouncer |
| CKEditor 4→5 breakage | broken toolbar/plugins | full rewrite; test custom build |

---

## Performance

1. **GCS CDN** — Cloud CDN in front of media bucket with long TTLs
2. **Django caching** — Redis/memcached for template fragment and queryset caching
3. **GCS object lifecycle** — auto-cleanup temp files
4. **gunicorn async workers** — `--worker-class uvicorn.workers.UvicornWorker`

---

## Security

1. **Always sanitize CKEditor output** — server-side before rendering
2. **Restrict GCS IAM** — least-privilege service accounts; no public write
3. **SECURE_SSL_REDIRECT + HSTS** — enforce HTTPS
4. **django-csp** — restrict inline scripts in CKEditor content
5. **Custom CKEditor build** — exclude dangerous plugins (iframe, etc.)

---

## Related Projects (in workspace)

- **cookiecutter-django-tailwind** — shared layered Django settings
- **ecom** — both use Django + Docker + PostgreSQL
- **rhixecompany-comics** — Django + Docker + PostgreSQL
- **xamehi.tv** — Django monolith; xamehi.tv adds React frontend

---

## Resources

| Resource | URL | Description |
|----------|-----|-------------|
| Django Docs | https://docs.djangoproject.com/en/4.2/ | Django 4.x documentation |
| GCS Docs | https://cloud.google.com/storage/docs | GCS best practices |
| django-ckeditor-5 | https://github.com/solaris17/django-ckeditor-5 | CKEditor 5 integration |
| django-storages GCS | https://django-storages.readthedocs.io/en/latest/backends/gcloud.html | GCS backend docs |
