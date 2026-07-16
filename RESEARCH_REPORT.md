# RESEARCH_REPORT — profile

> **Type:** Project research report | **Updated:** 2026-07-16

**Type:** Django blog/CMS with cloud media storage
**Tech Stack:** Django 4.x, GCS, CKEditor 5, PostgreSQL, Docker, GCP, bleach/nh3
**Status:** Active

---

## Similar Projects

| Project | URL | Why Relevant |
|---------|-----|--------------|
| Wagtail CMS | <https://github.com/wagtail/wagtail> | Leading Django CMS with StreamField |
| django-cms | <https://github.com/django-cms/django-cms> | Enterprise Django CMS ecosystem |
| djangocms-text-ckeditor5 | <https://github.com/django-cms/djangocms-text-ckeditor5> | CKEditor 5 for django-cms |

---

## Key Findings

### Django STORAGES Configuration
- Unified `STORAGES` config dict introduced in Django 4.2 — replaces `DEFAULT_FILE_STORAGE`
- `django-storages[google]` for GCS; separate static vs media buckets recommended
- Django ≥ 4.2: `STORAGES = {"default": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage", ...}, "staticfiles": {...}}`
- Use IAM service accounts (not user accounts) for GCS access

### CKEditor 5 Integration
- Complete rewrite from CKEditor 4 — different MVC architecture
- `django-ckeditor-5` (hvlads) provides `CKEditor5Field`, `CKEditor5Widget`, GCS image upload
- **Client-side sanitization only** — must sanitize server-side with `bleach` or `nh3`
- `CKEDITOR_5_FILE_STORAGE` points to GCS for media uploads
- `CKEDITOR_5_CONFIGS` for toolbar, plugins, image styles

### GCS + GCP Deployment
- `GS_BUCKET_NAME` + `GS_CREDENTIALS` + `STORAGES` dict configuration
- Signed URLs require IAM Sign Blob API — `GS_IAM_SIGN_BLOB=True` on Cloud Run
- `GS_DEFAULT_ACL` + `GS_QUERYSTRING_AUTH` for access control
- Docker + Cloud Run deployment: multi-stage Dockerfile, `PORT` env for Cloud Run

---

## Cheatsheets & Quick Reference

| Topic | Resource | Type |
|-------|----------|------|
| Django STORAGES | <https://docs.djangoproject.com/en/4.2/ref/settings/#storages> | Docs |
| django-ckeditor-5 | <https://github.com/hvlads/django-ckeditor-5> | Package |
| GCS + Django | <https://django-storages.readthedocs.io/en/latest/backends/gcloud.html> | Guide |

---

## Best Practices

1. **Separate media/static buckets** — different ACL and caching policies per bucket
2. **Server-side HTML sanitization** — `bleach` or `nh3` for CKEditor 5 output
3. **IAM service accounts** — not user accounts; least-privilege GCS roles
4. **Signed URLs for private media** — time-limited access to paywalled content
5. **Multi-stage Docker** — separate build vs runtime for smaller images

---

## Common Pitfalls

| Pitfall | Impact | Avoidance |
|---------|--------|-----------|
| Client-only sanitization | XSS via CKEditor | Server-side `bleach`/`nh3` sanitization |
| CKEditor 4 → 5 migration | Broken config | Different MVC; rewrite, not drop-in |
| Missing IAM Sign Blob API | Signed URLs fail | `GS_IAM_SIGN_BLOB=True` on Cloud Run |
| Shared media/static bucket | ACL conflicts | Separate buckets per purpose |

---

## Performance

1. **CDN for media delivery** — GCP Cloud CDN with signed URLs
2. **Redis caching** — cache rendered blog content; invalidate on publish
3. **GCS direct upload** — avoid proxying through Django for large files
4. **Image optimization** — serve WebP/AVIF; responsive images via template tags
5. **Database connection pooling** — `CONN_MAX_AGE` or pgbouncer

---

## Security

1. **Server-side HTML sanitization** — `bleach` or `nh3` for all CKEditor output
2. **Signed GCS URLs** — time-limited access for private media
3. **CSP headers** — restrict script sources; allow only CKEditor CDN
4. **HSTS + secure cookies** — `SECURE_HSTS_SECONDS`, `SESSION_COOKIE_SECURE`
5. **Input validation** — Zod or Django forms for all user-submitted content

---

## Related Projects (in workspace)

- **cookiecutter-django-tailwind** — shared Django + PostgreSQL + Docker patterns
- **ecom** — shared Django + DRF conventions
- **rhixecompany-comics** — shared Django + Docker + Celery patterns

---

## Resources

| Resource | URL | Description |
|----------|-----|-------------|
| Django STORAGES | <https://docs.djangoproject.com/en/4.2/ref/settings/#storages> | Storage backend config |
| django-ckeditor-5 | <https://github.com/hvlads/django-ckeditor-5> | CKEditor 5 Django integration |
| GCS Django | <https://django-storages.readthedocs.io/en/latest/backends/gcloud.html> | Google Cloud Storage |

### Research Methodology
- **Web search:** web_search (2026 Django CMS patterns)
- **Documentation:** web_extract (Django STORAGES, CKEditor 5 docs)
- **Cloud storage:** GCS + Django patterns research
- **Last verified:** 2026-07-16
