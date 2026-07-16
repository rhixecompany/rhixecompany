# RESEARCH_REPORT — profile

> **Type:** Project research report | **Updated:** 2026-07-16
>
> **Stack:** Django 4.x (target 5.2 LTS / 6.0), PostgreSQL, CKEditor 5, GCS, Docker, GCP, bleach/nh3
> **Status:** Active

---

## Overview

Django blog/CMS with CBVs, CKEditor 5 rich text, GCS media/static hosting, PostgreSQL, Docker + GCP. Researched via 10 web queries across 16 sources (2022–2026); verified Django 6.0 release notes and django-ckeditor-5 GitHub repo.

---

## Similar Projects

| Project | Why Relevant |
|---------|--------------|
| rhixecompany-comics (workspace) | Shared Django + Docker + Celery patterns |
| cookiecutter-django-tailwind (workspace) | Shared Django + PostgreSQL + Docker scaffold |
| ecom (workspace) | Django + DRF conventions |

---

## Key Findings

**Django version posture (verified July 2026).** Django 4.2 LTS hit **end-of-life April 7, 2026** (no security patches) → migrate to **5.2 LTS** urgently. 5.2 adds `CompositePrimaryKey`, async auth, PBKDF2 1,000,000. **Django 6.0** (Dec 3, 2025) supports **Python 3.12–3.14 only**; new built-in **CSP** (`SECURE_CSP` + nonce), template partials, a **Tasks framework** (`@task`), modern email API. Third-party apps now dropping pre-5.2.

**PostgreSQL & ORM.** `CONN_MAX_AGE=600` + PgBouncer; `OPTIONS={'sslmode':'require'}`; partial indexes via `Meta.indexes`; `select_related`/`prefetch_related`; `bulk_create`/`update_or_create`.

**CKEditor 5.** `django-ckeditor` (v4) deprecated w/ CVEs → use **`django-ckeditor-5`** (hvlads; verified 341 commits, image upload). Library warns uploaded files are **not validated server-side by default** → **sanitize with `nh3`/`bleach`**.

**GCS.** Django 4.2+ `STORAGES` → `GoogleCloudStorage` for media+static; separate buckets; IAM + `GS_IAM_SIGN_BLOB=True` for signed URLs.

**Docker.** Multi-stage (slim ~200MB); non-root; `healthcheck` + `/health/`; entrypoint for `collectstatic`/`migrate`.

---

## Cheatsheets & Quick Reference

| Topic | Resource |
|-------|----------|
| Django 6.0 release notes | https://docs.djangoproject.com/en/6.0/releases/6.0 |
| Django 5.2 release notes | https://docs.djangoproject.com/en/6.0/releases/5.2 |
| django-ckeditor-5 | https://github.com/hvlads/django-ckeditor-5 |
| Django + GCS | https://django-storages.readthedocs.io/en/latest/backends/gcloud.html |
| nh3 sanitizer | https://pypi.org/project/nh3 |

---

## Best Practices
1. Pin Django to **5.2 LTS now**; plan 6.0 once third-party deps catch up.
2. **Server-side sanitization** with `nh3` (Rust, faster) before storing CKEditor content.
3. Use Django 6.0's **built-in CSP** (`SECURE_CSP`) — native nonce support.
4. Separate **GCS buckets** for media vs static; IAM signing for private URLs.
5. Multi-stage Docker + non-root + healthchecks; `check --deploy` in CI.

---

## Common Pitfalls

| Pitfall | Layer | Fix |
|---------|-------|-----|
| CKEditor 4 (deprecated) | CKEditor | Migrate to `django-ckeditor-5` |
| Client-only sanitization | CKEditor | `nh3`/`bleach` server-side |
| Unvalidated file uploads | CKEditor | Validate/limit uploads server-side |
| Missing IAM Sign Blob | GCS | `GS_IAM_SIGN_BLOB=True` |
| Shared static/media bucket | GCS | Separate buckets |
| Docker as root | Docker | Non-root user |
| No connection pooling | PostgreSQL | `CONN_MAX_AGE` + PgBouncer |
| Running Django 4.2 post-EOL | Django | Upgrade to 5.2 LTS |

---

## Performance
- **PostgreSQL:** `CONN_MAX_AGE=600`, partial indexes, eager loading
- **GCS:** `GS_BLOB_CHUNK_SIZE` for uploads; CDN fronting
- **Django:** Redis caching + GzipMiddleware; invalidate on publish
- **Docker:** Multi-stage builds; Gunicorn workers = `(2 × CPU) + 1`
- **nh3** sanitizes ~10× faster than pure-Python `bleach`

---

## Security
1. **Django 4.2 EOL** — urgent upgrade; no patches since Apr 2026.
2. **Built-in CSP (6.0)** — `SECURE_CSP` + nonce context processor.
3. **Server-side sanitization** — `nh3`/`bleach` before render.
4. **Settings hardening** — `DEBUG=False`, env `SECRET_KEY`, HSTS, secure cookies.
5. **Auth** — password validators + `django-axes` + `django-ratelimit`; rename `/admin/`.

---

## Related Projects (in workspace)
- **cookiecutter-django-tailwind** — shared Django + PostgreSQL + Docker
- **ecom** — Django + DRF conventions
- **rhixecompany-comics** — Django + Docker + Celery

---

## Resources

| Resource | URL |
|----------|-----|
| Django 6.0 release notes | https://docs.djangoproject.com/en/6.0/releases/6.0 |
| Django 5.2 release notes | https://docs.djangoproject.com/en/6.0/releases/5.2 |
| django-ckeditor-5 | https://github.com/hvlads/django-ckeditor-5 |
| Django + GCS (django-storages) | https://django-storages.readthedocs.io/en/latest/backends/gcloud.html |
| OWASP Django Security | https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html |

**Methodology:** 10 web queries × 16 sources; verified Django 6.0/5.2 notes, hvlads/django-ckeditor-5. EOL + CKEditor migration confirmed from primary sources.
