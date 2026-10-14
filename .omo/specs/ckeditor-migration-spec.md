# CKEditor 4 → 5 Migration Specification

**Project:** Django Blog CMS (`base/` + `rhixecompany/`)
**Spec Version:** 1.0
**Date:** 2026-10-14
**Status:** Planned
**Workflow Tier:** GA

---

## 1. Problem Statement

Current `django-ckeditor==6.7.3` bundles **CKEditor 4.22.1** which is end-of-life (EOL) with known unfixed security vulnerabilities. Django system check emits warning `ckeditor.W001`. Migration to `django-ckeditor-5` (CKEditor 5) is required for security and maintenance.

---

## 2. Scope

### In Scope
- Replace `django-ckeditor` with `django-ckeditor-5` in `requirements.txt`
- Migrate `Post.body` field: `RichTextUploadingField` → `CKEditor5Field`
- Update all templates using CKEditor widgets (`post_form.html`, admin overrides)
- Update `CKEDITOR_UPLOAD_PATH` → `CKEDITOR_5_CONFIGS` for GCS uploads
- Remove CKEditor 4 vendor assets from `base/static/admin/ckeditor/` and `base/static/ckeditor/`
- Verify admin and staff post forms render with CKEditor 5
- Verify image uploads work with GCS backend

### Out of Scope
- Custom CKEditor 4 plugins/toolbars (none identified)
- Content migration of existing rich text (HTML output compatible)
- Frontend theme changes beyond editor component

---

## 3. Technical Design

### 3.1 Package Changes
```diff
# requirements.txt
- django-ckeditor==6.7.3
+ django-ckeditor-5==0.0.1
```

### 3.2 Model Field Migration
```python
# base/models.py
from ckeditor_uploader.fields import RichTextUploadingField  # REMOVE
from django_ckeditor_5.fields import CKEditor5Field          # ADD

class Post(models.Model):
    body = CKEditor5Field(config_name='default')  # was: RichTextUploadingField(null=True, blank=True)
```

### 3.3 Settings Configuration
```python
# rhixecompany/settings.py
INSTALLED_APPS = [
    # ...
    "django_ckeditor_5",  # replaces "ckeditor", "ckeditor_uploader"
]

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": ["heading", "|", "bold", "italic", "link", "bulletedList", "numberedList", "blockQuote", "imageUpload"],
        "image": {
            "toolbar": ["imageTextAlternative", "|", "imageStyle:alignLeft", "imageStyle:alignRight", "imageStyle:alignCenter", "imageStyle:side"],
            "styles": ["full", "side", "alignLeft", "alignRight", "alignCenter"],
        },
        "filebrowser": {
            "uploadUrl": "/ckeditor5/upload/",  # route to CKEditor 5 upload view
        },
    }
}

# GCS integration
CKEDITOR_5_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
```

### 3.4 Upload View (GCS Compatible)
```python
# base/views.py - new view for CKEditor 5 uploads
from django_ckeditor_5.views import upload_image

# Or custom view if GCS path customization needed
```

### 3.5 Template Updates
```html
<!-- base/templates/base/post_form.html -->
{% load ckeditor5_tags %}
{{ form.media }}  <!-- includes CKEditor 5 JS/CSS -->
{{ form.body|ckeditor5 }}
```

```html
<!-- Admin override if needed -->
{% load ckeditor5_tags %}
{{ form.media }}
```

### 3.6 Static Assets Cleanup
Remove:
- `base/static/admin/ckeditor/` (vendor 4.x assets)
- `base/static/ckeditor/` (vendor 4.x assets)

CKEditor 5 assets served via `django_ckeditor_5` package.

---

## 4. Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | `django-ckeditor` removed from `requirements.txt` | `grep -r django-ckeditor requirements.txt` returns only `django-ckeditor-5` |
| 2 | `Post.body` uses `CKEditor5Field` | Model inspection; `python manage.py check` passes without `ckeditor.W001` |
| 3 | Post create/edit forms render CKEditor 5 | Manual test: `/create_post/` and `/update_post/<slug>/` show editor |
| 4 | Image upload writes to GCS | Upload image in editor → verify object in GCS bucket |
| 5 | Admin uses CKEditor 5 | `/admin/base/post/` shows CKEditor 5 toolbar |
| 6 | No CKEditor 4 static assets remain | `ls base/static/admin/ckeditor/ base/static/ckeditor/` returns empty or removed |
| 7 | Existing post content renders | View existing posts → body HTML renders correctly |
| 8 | All tests pass | `python manage.py test base.tests` |

---

## 5. Migration Steps

1. **Backup**: `pip freeze > requirements-backup.txt`
2. **Install**: `pip install django-ckeditor-5`
3. **Uninstall**: `pip uninstall django-ckeditor`
3. **Update requirements.txt**
4. **Model change**: `Post.body = CKEditor5Field(...)`
5. **Settings**: Add `CKEDITOR_5_CONFIGS`, update `INSTALLED_APPS`
6. **Templates**: Update `post_form.html`, admin templates
7. **Static**: Remove `base/static/{admin,}/ckeditor/`
8. **Migrations**: `makemigrations base` → `migrate`
9. **Test**: Run acceptance criteria checklist
10. **Document**: Update `CHANGELOG.md`, `docs/scope/scope.md`

---

## 6. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| CKEditor 5 config incompatibility | Medium | High | Test config in dev first; keep `config_name='default'` simple |
| GCS upload path mismatch | Medium | High | Verify `CKEDITOR_5_CONFIGS['default']['filebrowser']['uploadUrl']` matches upload view |
| Admin widget not auto-migrated | Low | Medium | Explicitly set `formfield_overrides` in admin if needed |
| Existing content HTML issues | Low | Low | CKEditor 5 outputs compatible HTML; test render |

---

## 7. Dependencies

- Requires GCS configuration working (`setting.py` with `GS_BUCKET_NAME`, `DEFAULT_FILE_STORAGE`)
- `django-storages[google]` already in requirements
- `storages.backends.gcloud.GoogleCloudStorage` used for `CKEDITOR_5_FILE_STORAGE`

---

## 8. Rollback Plan

If migration fails:
1. Revert `requirements.txt` to `django-ckeditor==6.7.3`
2. Revert `base/models.py` to `RichTextUploadingField`
3. Revert `settings.py` `INSTALLED_APPS` and remove `CKEDITOR_5_CONFIGS`
4. Restore static assets from git
5. `pip install -r requirements.txt` → `migrate base zero` → `migrate`