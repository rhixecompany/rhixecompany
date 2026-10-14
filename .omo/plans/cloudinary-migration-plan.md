# GCS → Cloudinary Migration Plan

**Spec:** `.omo/specs/cloudinary-migration-spec.md`
**Created:** 2026-10-14
**Status:** Planned
**Workflow:** GA (needs spec, build, verify, test, review, document)

---

## Plan Steps

### Phase 1: Design (Architect)
- [ ] Run `/architect GCS to Cloudinary migration` → capture spec (`.omo/specs/cloudinary-migration-spec.md`)
- [ ] Review Cloudinary free tier limits vs. projected usage
- [ ] Approve spec → move to build

### Phase 2: Build (Develop)

#### 2.1 Cloudinary Account & Credentials
- [ ] Create Cloudinary account (or use existing)
- [ ] Note `CLOUDINARY_URL` or `CLOUDINARY_CLOUD_NAME`/`API_KEY`/`API_SECRET`
- [ ] Add to deployment environment (not `.env` committed)

#### 2.2 Package Swap
- [ ] `pip install django-cloudinary-storage cloudinary`
- [ ] `pip uninstall django-storages`
- [ ] Update `requirements.txt`

#### 2.3 Settings Migration (`rhixecompany/setting.py`)
- [ ] Add Cloudinary config block:
  ```python
  import cloudinary
  cloudinary.config(
      cloud_name=env("CLOUDINARY_CLOUD_NAME"),
      api_key=env("CLOUDINARY_API_KEY"),
      api_secret=env("CLOUDINARY_API_SECRET"),
      secure=True,
  )
  ```
- [ ] Change storage backends:
  ```python
  DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
  STATICFILES_STORAGE = "cloudinary_storage.storage.StaticHashedCloudinaryStorage"
  ```
- [ ] Add `CLOUDINARY_STORAGE` config dict
- [ ] Remove GCS settings:
  - `GS_BUCKET_NAME`
  - `GS_DEFAULT_ACL`
  - `STATICFILES_DIRS = []`

#### 2.4 CKEditor 5 Upload Integration (if CKEditor 5 done)
- [ ] Add `ckeditor5_upload` view using `cloudinary.uploader.upload`
- [ ] Update `CKEDITOR_5_CONFIGS['default']['filebrowser']['uploadUrl']`
- [ ] Add URL route in `base/urls.py`

#### 2.5 Static Files
- [ ] Run `python manage.py collectstatic --noinput` (after deploy)
- [ ] Verify `staticfiles-manifest.json` generated

#### 2.6 Deploy Configuration
- [ ] Set `CLOUDINARY_URL` in deployment (Cloud Run, etc.)
- [ ] Remove `GS_BUCKET_NAME` from deployment config
- [ ] Remove GCS service account if no longer used

### Phase 3: Verify
- [ ] Run `/check verify GCS to Cloudinary migration`
  - [ ] `grep -E "django-storages|django-cloudinary-storage" requirements.txt` → only cloudinary
  - [ ] `grep DEFAULT_FILE_STORAGE rhixecompany/setting.py` → `MediaCloudinaryStorage`
  - [ ] `grep STATICFILES_STORAGE rhixecompany/setting.py` → `StaticHashedCloudinaryStorage`
  - [ ] `grep -c "GS_BUCKET_NAME\|GS_DEFAULT_ACL" rhixecompany/setting.py` = 0
  - [ ] `cloudinary.config()` called with creds (check logs)

### Phase 4: Test
- [ ] Run `/test GCS to Cloudinary migration`
  - [ ] `python manage.py test base.tests` passes
  - [ ] Manual: Create post with image → verify in Cloudinary Media Library
  - [ ] Manual: Edit post → thumbnail upload → Cloudinary
  - [ ] Manual: CKEditor image upload → Cloudinary folder `ckeditor5/`
  - [ ] Manual: `collectstatic` → static files in Cloudinary with hashed names
  - [ ] Manual: Old GCS image URL → loads (read-only)
  - [ ] Manual: Admin post form → upload works

### Phase 5: Review (GA)
- [ ] Run `/check review GCS to Cloudinary migration`
  - [ ] Security: Credentials via env var only; no keys in repo
  - [ ] Standards: Django storage backend pattern followed
  - [ ] Spec adherence: All acceptance criteria met
  - [ ] Cost: Free tier usage within limits

### Phase 6: Document
- [ ] Run `/document GCS to Cloudinary migration`
  - [ ] Update `CHANGELOG.md`
  - [ ] Update `docs/scope/scope.md` → mark feature 10 as `done`
  - [ ] Update `.omo/plans/cloudinary-migration-plan.md` with final verification notes

---

## Validation Checklist (from Spec)

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `django-storages` removed, `django-cloudinary-storage` added | ☐ |
| 2 | `DEFAULT_FILE_STORAGE` = `MediaCloudinaryStorage` | ☐ |
| 3 | `STATICFILES_STORAGE` = `StaticHashedCloudinaryStorage` | ☐ |
| 4 | Cloudinary credentials configured | ☐ |
| 5 | GCS settings removed | ☐ |
| 6 | Media upload writes to Cloudinary | ☐ |
| 7 | Static collectstatic works | ☐ |
| 8 | Existing GCS URLs accessible | ☐ |
| 9 | CKEditor uploads to Cloudinary | ☐ |
| 10 | All tests pass | ☐ |

---

## Zero-Downtime Deployment

| Step | Action | Rollback if Fails |
|------|--------|-------------------|
| 1 | Deploy settings with Cloudinary backend | Revert settings.py |
| 2 | Set `CLOUDINARY_URL` in prod env | Unset env var |
| 3 | Run `collectstatic` | Revert to GCS static |
| 4 | Test media upload | Revert storage backend |
| 5 | Monitor Cloudinary usage | Alert at 80% free tier |

---

## Dependencies
- Cloudinary account (free tier: 25 GB storage, 25 GB bandwidth/month)
- `django-cloudinary-storage>=0.3.0`, `cloudinary>=1.36.0`
- CKEditor 5 migration (optional, for upload integration)
- Deployment environment supporting env vars

---

## Rollback Plan
If any phase fails:
1. `git checkout -- rhixecompany/setting.py requirements.txt`
2. `pip install -r requirements.txt` (restores `django-storages`)
3. `python manage.py collectstatic --noinput` (to GCS)
4. Verify uploads work with GCS backend
5. Remove `CLOUDINARY_URL` from deployment env