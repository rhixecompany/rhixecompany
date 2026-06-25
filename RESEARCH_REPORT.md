# RESEARCH_REPORT — profile

> **Type:** Project research report | **Updated:** 2026-06-25

---

**Type:** Django blog/CMS with cloud media storage
**Tech Stack:** Django 4.x, GCS, CKEditor 5, PostgreSQL, Docker, GCP
**Status:** Active

---

## Similar Projects

| Project | URL | Why Relevant |
| ------- | --- | ------------ |
| django-cms | https://www.django-cms.org/ | Enterprise Django CMS with CKEditor 5 support (2026) |
| Wagtail CMS | https://wagtail.org/ | The most popular Django CMS alternative |

---

## Key Findings

### Django Blog/CMS with CKEditor 5

- django CMS now ships `djangocms-text-ckeditor5` package with enhanced CKEditor 5 support (django-cms.org, June 2026)
- CKEditor 5 integrates with Django via `django-ckeditor-5` package; image upload requires custom upload backend or django-filer
- CBVs (ListView, DetailView, CreateView, UpdateView) remain the recommended pattern for CMS views in Django 4.x (docs.djangoproject.com)

### Google Cloud Storage

- GCS bucket naming and object naming conventions affect performance — use hierarchical namespace for better prefix-based listing (cloud.google.com/docs)
- `django-storages[google]` with `GOOGLE_APPLICATION_CREDENTIALS` env var is the standard integration path
- `collectstatic` uploads to GCS bucket; use `GS_DEFAULT_ACL` and `GS_QUERYSTRING_AUTH` for public vs private access control

### Docker + GCP Deployment

- Cloud Run + Cloud SQL PostgreSQL with connection pooling is the recommended GCP deployment pattern (forum.djangoproject.com, 2026)
- Cloud Run scaling can overwhelm database connections — implement Django's `CONN_MAX_AGE` + pgbouncer for pooling (forum.djangoproject.com)

---

## Cheatsheets & Quick Reference

| Topic | Resource | Type |
| ----- | -------- | ---- |
| GCS best practices | https://cloud.google.com/storage/docs/best-practices | Guide |
| Django + Cloud Run | https://oneuptime.com/blog/post/2026-02-17-how-to-build-a-django-application-with-cloud-sql-and-deploy-to-cloud-run/ | Guide |
| Django-ckeditor-5 | https://github.com/solaris17/django-ckeditor-5 | GitHub |


## Best Practices

1. **CBVs over FBVs** — Use Class-Based Views (ListView, DetailView) for consistent, reusable CMS views
2. **GCS media separation** — Store user-uploaded media in GCS, static files via WhiteNoise or GCS
3. **Connection pooling** — Set `CONN_MAX_AGE` and use pgbouncer when deploying to Cloud Run
4. **CKEditor 5 upload** — Configure image upload handler for rich text; restrict allowed file types server-side

---

## Common Pitfalls

| Pitfall | Impact | Avoidance |
| ------- | ------ | --------- |
| No GCS credentials in `.env` | `collectstatic` fails with auth errors | Use GOOGLE_APPLICATION_CREDENTIALS JSON path |
| CKEditor 5 upload not configured | Broken image upload UX | Implement custom upload endpoint for CKEditor |
| Cloud Run DB connection exhaustion | 500 errors under load | Set MAX_CONNECTIONS and use connection pooling |
| Missing ALLOWED_HOSTS | 400 Bad Request errors | Configure ALLOWED_HOSTS for GCP domains |

---

## Performance

1. **GCS CDN** — Buckets behind Cloud CDN cache static/media assets with long TTLs
2. **Django caching** — Use Redis/memcached for template fragment and queryset caching
3. **Database indexes** — Index publication date, slug, author fields in CMS models
4. **select_related** — Use eager loading on foreign keys in blog list views to avoid N+1 queries

---

## Security

1. **GCS bucket permissions** — Use fine-grained IAM; never make buckets publicly writable
2. **CKEditor XSS** — Sanitize HTML output with bleach or django-html-sanitizer before rendering
3. **Django SECRET_KEY** — Rotate in GCP Secret Manager; never in version control
4. **Cloud Run IAM** — Use service accounts with least-privilege; no public Cloud Run invocations without auth

---

## Related Projects (in workspace)

- **cookiecutter-django-tailwind** — Shares layered Django settings; profile uses Django 4.x vs 5.x
- **ecom** — Both use Docker Compose and PostgreSQL; profile adds GCS for media
- **rhixecompany-comics** — Both use Django + Docker + PostgreSQL

---

## Resources

| Resource | URL | Description |
| -------- | --- | ----------- |
| Django Docs | https://docs.djangoproject.com/en/4.2/ | Django 4.x documentation |
| Google Cloud Storage | https://cloud.google.com/storage/docs | GCS best practices |
| django-ckeditor-5 | https://github.com/solaris17/django-ckeditor-5 | CKEditor 5 Django integration |
| django-storages | https://django-storages.readthedocs.io/ | Django storage backends |

---