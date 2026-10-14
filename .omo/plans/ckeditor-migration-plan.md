# CKEditor 4 → 5 Migration Plan

**Spec:** `.omo/specs/ckeditor-migration-spec.md`
**Created:** 2026-10-14
**Status:** Planned
**Workflow:** GA (needs spec, build, verify, test, review, document)

---

## Plan Steps

### Phase 1: Design (Architect)
- [ ] Run `/architect CKEditor 4 to 5 migration` → capture spec (`.omo/specs/ckeditor-migration-spec.md`)
- [ ] Review spec with stakeholders
- [ ] Approve spec → move to build

### Phase 2: Build (Develop)
- [ ] **Package swap**: Update `requirements.txt` (`django-ckeditor-5` replaces `django-ckeditor`)
- [ ] **Install**: `pip install django-ckeditor-5` and `pip uninstall django-ckeditor`
- [ ] **Model**: Change `Post.body` to `CKEditor5Field(config_name='default')`
- [ ] **Settings**: Add `CKEDITOR_5_CONFIGS` with GCS upload URL; update `INSTALLED_APPS`
- [ ] **Templates**: Update `base/templates/base/post_form.html` to use `{% load ckeditor5_tags %}` and `{{ form.body|ckeditor5 }}`
- [ ] **Admin**: Verify admin uses CKEditor 5 widget (add `formfield_overrides` if needed)
- [ ] **Static**: Remove `base/static/admin/ckeditor/` and `base/static/ckeditor/`
- [ ] **Upload view**: Add CKEditor 5 upload route if not auto-registered
- [ ] **Migrations**: `makemigrations base` → `migrate`

### Phase 3: Verify
- [ ] Run `/check verify CKEditor 4 to 5 migration`
  - [ ] `grep django-ckeditor requirements.txt` → only `django-ckeditor-5`
  - [ ] `python manage.py check` → no `ckeditor.W001` warning
  - [ ] `Post.body` field type is `CKEditor5Field`
  - [ ] `CKEDITOR_5_CONFIGS` present in settings

### Phase 4: Test
- [ ] Run `/test CKEditor 4 to 5 migration`
  - [ ] `python manage.py test base.tests` passes
  - [ ] Manual: Create post → editor renders → save
  - [ ] Manual: Edit post → editor loads existing content
  - [ ] Manual: Upload image in editor → verify in GCS bucket
  - [ ] Manual: Admin post form → CKEditor 5 toolbar visible
  - [ ] Manual: View existing post → body renders correctly

### Phase 5: Review (GA)
- [ ] Run `/check review CKEditor 4 to 5 migration`
  - [ ] Security: No CKEditor 4 code remains
  - [ ] Standards: Follows Django conventions
  - [ ] Spec adherence: All acceptance criteria met

### Phase 6: Document
- [ ] Run `/document CKEditor 4 to 5 migration`
  - [ ] Update `CHANGELOG.md`
  - [ ] Update `docs/scope/scope.md` → mark feature 8 as `done`
  - [ ] Update `.omo/plans/ckeditor-migration-plan.md` with final verification notes

---

## Validation Checklist (from Spec)

| # | Criterion | Status |
|---|-----------|--------|
| 1 | `django-ckeditor` removed from requirements | ☐ |
| 2 | `Post.body` uses `CKEditor5Field` | ☐ |
| 3 | Post create/edit forms render CKEditor 5 | ☐ |
| 4 | Image upload writes to GCS | ☐ |
| 5 | Admin uses CKEditor 5 | ☐ |
| 6 | No CKEditor 4 static assets remain | ☐ |
| 7 | Existing post content renders | ☐ |
| 8 | All tests pass | ☐ |

---

## Dependencies
- GCS configuration working (`setting.py` with `GS_BUCKET_NAME`)
- `django-storages[google]` in requirements
- `storages.backends.gcloud.GoogleCloudStorage` available

---

## Rollback
If any phase fails:
1. `git checkout -- requirements.txt base/models.py rhixecompany/settings.py base/templates/ base/static/`
2. `pip install -r requirements.txt`
3. `python manage.py migrate base zero`
4. `python manage.py migrate`