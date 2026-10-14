# GCS → Cloudinary Media Storage Migration Specification

**Project:** Django Blog CMS (`base/` + `rhixecompany/`)
**Spec Version:** 1.0
**Date:** 2026-10-14
**Status:** Planned
**Workflow Tier:** GA

---

## 1. Problem Statement

Current media and static file storage uses **Google Cloud Storage (GCS)** via `django-storages[google]` with `storages.backends.gcloud.GoogleCloudStorage`. Migration to **Cloudinary** (`django-cloudinary-storage`) provides:
- Automatic image optimization (format, quality, compression)
- On-the-fly transformations (resize, crop, effects)
- Global CDN delivery
- Generous free tier (25 GB storage, 25 GB bandwidth/month)
- Simpler credential management (`CLOUDINARY_URL` single env var)

---

## 2. Scope

### In Scope
- Replace `django-storages[google]` with `django-cloudinary-storage` in `requirements.txt`
- Update `rhixecompany/setting.py`: `DEFAULT_FILE_STORAGE`, `STATICFILES_STORAGE` → Cloudinary backend
- Configure Cloudinary credentials via `CLOUDINARY_URL` (or `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`)
- Remove GCS-specific settings: `GS_BUCKET_NAME`, `GS_DEFAULT_ACL`, `STATICFILES_DIRS = []`
- Integrate CKEditor 5 uploads with Cloudinary (if CKEditor 5 migration done first)
- Verify existing GCS URLs remain accessible (read-only, no migration of existing assets)
- Update `.env` / deployment config with Cloudinary credentials

### Out of Scope
- Migration of existing GCS assets to Cloudinary (cost/complexity; keep GCS URLs working)
- Cloudinary Advanced features (AI tagging, background removal) — optional future
- Video upload handling (not currently used)
- Frontend template changes (URLs remain compatible)

---

## 3. Technical Design

### 3.1 Package Changes
```diff
# requirements.txt
- django-storages==1.14.6
+ django-cloudinary-storage==0.3.0
+ cloudinary==1.36.0
```

### 3.2 Settings Configuration
```python
# rhixecompany/setting.py
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Cloudinary configuration from CLOUDINARY_URL or individual env vars
cloudinary.config(
    cloud_name=env("CLOUDINARY_CLOUD_NAME", default=None),
    api_key=env("CLOUDINARY_API_KEY", default=None),
    api_secret=env("CLOUDINARY_API_SECRET", default=None),
    secure=True,
)

# Or single URL: cloudinary.config(cloudinary_url=env("CLOUDINARY_URL"))

# Storage backends
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
STATICFILES_STORAGE = "cloudinary_storage.storage.StaticHashedCloudinaryStorage"

# Optional: Cloudinary folder structure
CLOUDINARY_STORAGE = {
    "MEDIA_TAG": "rhixecompany-media",
    "STATIC_TAG": "rhixecompany-static",
    "STATICFILES_MANIFEST": "staticfiles-manifest.json",
    "OVERWRITE_EXISTING": False,  # Keep existing GCS files accessible
}

# Remove GCS settings:
# GS_BUCKET_NAME = ...
# GS_DEFAULT_ACL = "publicRead"
# STATICFILES_DIRS = []
```

### 3.3 CKEditor 5 Integration (if CKEditor 5 migration done)
```python
# rhixecompany/setting.py
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [...],
        "image": {
            "toolbar": [...],
        },
        "filebrowser": {
            "uploadUrl": "/ckeditor5/upload/",  # Cloudinary upload view
        },
    }
}

# Cloudinary upload view for CKEditor 5
# base/views.py
from cloudinary.uploader import upload
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def ckeditor5_upload(request):
    if request.method == "POST" and request.FILES.get("upload"):
        result = upload(request.FILES["upload"], folder="ckeditor5/")
        return JsonResponse({"url": result["secure_url"], "uploaded": True})
    return JsonResponse({"error": "Invalid request"}, status=400)
```

### 3.4 Environment Variables
```bash
# .env (production)
CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
# OR individual vars:
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Remove:
# GS_BUCKET_NAME=...
# APPLICATION_SETTINGS=... (if only used for GCS)
```

### 3.5 Static Files with Cloudinary
```python
# rhixecompany/setting.py
# For static files: hashed filenames + CDN
STATICFILES_STORAGE = "cloudinary_storage.storage.StaticHashedCloudinaryStorage"

# Run after deployment:
# python manage.py collectstatic --noinput
# Generates manifest mapping original → hashed Cloudinary URLs
```

---

## 4. Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | `django-storages` removed, `django-cloudinary-storage` added | `grep -E "django-storages|django-cloudinary-storage" requirements.txt` |
| 2 | `DEFAULT_FILE_STORAGE` = `MediaCloudinaryStorage` | `grep DEFAULT_FILE_STORAGE rhixecompany/setting.py` |
| 3 | `STATICFILES_STORAGE` = `StaticHashedCloudinaryStorage` | `grep STATICFILES_STORAGE rhixecompany/setting.py` |
| 4 | Cloudinary credentials configured | `cloudinary.config()` called with valid creds |
| 5 | GCS settings removed | `grep -c "GS_BUCKET_NAME\|GS_DEFAULT_ACL" rhixecompany/setting.py` = 0 |
| 6 | Media upload writes to Cloudinary | Upload image via admin/post form → verify in Cloudinary Media Library |
| 7 | Static collectstatic works | `python manage.py collectstatic --noinput` → manifest generated |
| 8 | Existing GCS URLs accessible | Visit old GCS image URL → loads (read-only, no migration) |
| 9 | CKEditor uploads to Cloudinary | Upload in editor → verify in Cloudinary folder `ckeditor5/` |
| 10 | All tests pass | `python manage.py test base.tests` |

---

## 5. Migration Steps

### Phase 1: Preparation
1. **Create Cloudinary account** → get `CLOUDINARY_URL` or individual credentials
2. **Backup**: `pip freeze > requirements-backup.txt`
3. **Document existing GCS URLs** for reference (admin, posts, static)

### Phase 2: Package Swap
4. `pip install django-cloudinary-storage cloudinary`
5. `pip uninstall django-storages`
6. Update `requirements.txt`

### Phase 3: Settings Migration
7. Update `rhixecompany/setting.py`:
   - Add Cloudinary config
   - Change `DEFAULT_FILE_STORAGE`, `STATICFILES_STORAGE`
   - Add `CLOUDINARY_STORAGE` dict
   - Remove `GS_BUCKET_NAME`, `GS_DEFAULT_ACL`, `STATICFILES_DIRS = []`

### Phase 4: CKEditor Integration (if applicable)
8. Add CKEditor 5 upload view using `cloudinary.uploader.upload`
9. Update `CKEDITOR_5_CONFIGS['default']['filebrowser']['uploadUrl']`

### Phase 5: Deploy & Verify
10. Set `CLOUDINARY_URL` in deployment environment
11. `python manage.py collectstatic --noinput`
12. Test uploads: admin, post create/edit, CKEditor
13. Verify old GCS URLs still load

### Phase 6: Cleanup
14. Remove GCS service account keys from deployment (if any)
15. Update documentation

---

## 6. Zero-Downtime Strategy

| Asset Type | Strategy |
|------------|----------|
| **Existing GCS media** | Leave in GCS; URLs unchanged; Cloudinary only for *new* uploads |
| **Existing GCS static** | Leave in GCS; `collectstatic` pushes new static to Cloudinary |
| **New uploads** | Route to Cloudinary via new storage backend |
| **Database references** | No change (stores relative paths or URLs) |

**Rollback**: Revert `setting.py` to GCS backend; `pip install django-storages`; `collectstatic` to GCS.

---

## 7. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Cloudinary free tier exceeded | Low | Medium | Monitor usage; set alerts at 80% |
| Credential leakage | Medium | High | Use `CLOUDINARY_URL` single var; never commit to repo |
| Static file hashing mismatch | Medium | Medium | Run `collectstatic` in staging first |
| CKEditor upload view CSRF | Low | Medium | Use `@csrf_exempt` with Cloudinary signed upload alternative |
| `django-cloudinary-storage` version conflicts | Low | Low | Pin version in requirements |

---

## 8. Dependencies

- Cloudinary account (free tier sufficient for start)
- `django-cloudinary-storage>=0.3.0`, `cloudinary>=1.36.0`
- Existing `django-storages` removed
- CKEditor 5 migration (optional, but recommended for upload integration)

---

## 9. Rollback Plan

If migration fails:
1. Revert `rhixecompany/setting.py` to GCS backend
2. `requirements.txt`: restore `django-storages`, remove `django-cloudinary-storage` + `cloudinary`
3. `pip install -r requirements.txt`
4. `python manage.py collectstatic --noinput` (to GCS)
5. Verify uploads work with GCS