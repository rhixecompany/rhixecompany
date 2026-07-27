# RESEARCH_REPORT — profile

> **Type:** Project research report | **Updated:** 2026-07-28

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
- Unified `STORAGES` dict (Django 4.2+) replaces legacy `DEFAULT_FILE_STORAGE`
- `django-storages[google]` for GCS; separate media vs static buckets recommended
- IAM service accounts preferred over user accounts for GCS access

### CKEditor 5 Integration
- Complete rewrite from CKEditor 4 — different MVC, not a drop-in replacement
- `django-ckeditor-5` provides `CKEditor5Field`, `CKEditor5Widget`, GCS image upload
- **Must sanitize server-side** with `bleach` or `nh3` (client-side only is insufficient)
- `CKEDITOR_5_FILE_STORAGE` → GCS; `CKEDITOR_5_CONFIGS` for toolbar/plugins

### GCS + GCP Deployment
- `GS_BUCKET_NAME` + `GS_CREDENTIALS` + `STORAGES` dict; signed URLs need IAM Sign Blob API
- Docker + Cloud Run: multi-stage Dockerfile, `PORT` env for Cloud Run

---

## Cheatsheets & Quick Reference

| Topic | Resource | Type |
|-------|----------|------|
| Django STORAGES | <https://docs.djangoproject.com/en/4.2/ref/settings/#storages> | Docs |
| django-ckeditor-5 | <https://github.com/hvlads/django-ckeditor-5> | Package |
| GCS + Django | <https://django-storages.readthedocs.io/en/latest/backends/gcloud.html> | Guide |

---

## Best Practices

1. **Separate media/static buckets** — different ACL and caching policies
2. **Server-side HTML sanitization** — `bleach`/`nh3` for all CKEditor output
3. **IAM service accounts** — not user accounts; least-privilege GCS roles
4. **Signed URLs for private media** — time-limited access to paywalled content
5. **Multi-stage Docker** — separate build vs runtime for smaller images

---

## Common Pitfalls

| Pitfall | Impact | Avoidance |
|---------|--------|-----------|
| Client-only sanitization | XSS via CKEditor | Server-side `bleach`/`nh3` |
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
5. **Input validation** — Django forms for all user-submitted content; search for `|safe` and `@csrf_exempt`

---

## Testing & Quality Assurance

1. **pytest + pytest-django** — DB-backed tests for models, views, and CKEditor output
2. **bleach/nh3 sanitization tests** — verify XSS vectors are stripped from rich text
3. **GCS mock integration** — `mock.patch` for storage backends in CI (no real GCS credentials)
4. **CI coverage enforcement** — `--cov-fail-under=80` with branch coverage
5. **Django `check --deploy`** — automated in CI pipeline before every deployment

---

## Related Projects (in workspace)

- **cookiecutter-django-tailwind** — shared Django + PostgreSQL + Docker patterns
- **ecom** — shared Django + DRF conventions
- **Django-Scrapy-Selenium** — shared Django architecture

---

## Resources

| Resource | URL | Description |
|----------|-----|-------------|
| Django STORAGES | <https://docs.djangoproject.com/en/4.2/ref/settings/#storages> | Storage backend config |
| django-ckeditor-5 | <https://github.com/hvlads/django-ckeditor-5> | CKEditor 5 Django integration |
| GCS Django | <https://django-storages.readthedocs.io/en/latest/backends/gcloud.html> | Google Cloud Storage |

### Research Methodology
- **Web search:** web_search (2026 Django CMS patterns, GCS storage)
- **Documentation:** web_extract (Django STORAGES, CKEditor 5 docs)
- **Cloud storage:** GCS + Django patterns research
- **Last verified:** 2026-07-28
