# Brownfield scoping with the Journey approach — reusable pattern

When `/scope` infers `plan` and the workspace has an existing codebase (Django app, source files present, no `docs/scope/`), treat it as brownfield: enroll existing features before planning new ones.

## The enrollment rule (imperative, applies every time)

Scan the source (`base/models.py`, `base/views.py`, `base/forms.py`, `base/urls.py`) and the root `AGENTS.md`. For each existing feature that is complete, write a feature section with status `existing` (not `done`) and tick every lifecycle box (`Design it`, `Build it`, `Verify it`, `Test it`). For partial features, use `in-progress`. Never mark a half-built feature `existing`. Never plan an `existing` feature again; it stays as context only.

## Why this matters (mechanism)

A brownfield scope that treats existing code as `planned` creates phantom work: the pipeline tells `/develop` to rebuild a feature that already runs. Labeling `existing` keeps the build order honest so `/develop` skips it and only resumes `in-progress` or builds `planned` work.

## Phase grouping for a blog CMS journey

With the Journey approach (`Journey` = complete user path per phase), group existing and planned features by journey, not by layer:

- Foundation: stack, data model, auth, templates, tooling.
- Phase 1 (Publishing Journey): staff creates/updates/deletes a post with GCS-stored images, confirms the publish state (draft, featured, active), sees it in the feed. Must include GCS uploads (planned, needs spec at GA) and the staff state machine (planned, needs spec at GA), plus existing post listing/detail/comments.
- Phase 2 (Account Journey): user registers, updates profile. Existing features stay here, fully polished.
- Phase 3 (System): email/contact, accessibility notes (minimal, no separate build box), deferred capabilities listed cleanly (search, analytics, notifications, public API, i18n, advanced performance, SEO, cookie consent).

## Decision panel shorthand for this class

- Auth: single-user (`existing`) vs multi-tenant (`planned`, deferred for small scope).
- Publishing: GCS uploads (`planned`, needs spec — storage provider choice); staff workflow (`planned`, needs spec — state machine design).
- Cross-cutting defaults: basic performance (`existing`); deferred analytics/i18n; deferred full text search; minimal accessibility note (no feature row); deferred cookie consent/GDPR banner (internal staff tool); deferred SEO (user stated internal focus).
- Workflow tier for a staff-facing CMS with a public surface: recommend `GA` (verify, test, review, document; most features need a spec). Only drop to `Beta` or `Alpha` if the user explicitly selects a lower rigor.

## Key file pointers (verified for this workspace)

- `base/models.py`: Profile, Post, Tag, PostComment.
- `base/views.py`: home, posts (filter + pagination), post, profile, CRUD (`createPost`, `updatePost`, `deletePost`), sendEmail, loginPage, registerPage, logoutUser, userAccount, updateProfile.
- `base/urls.py`: routes mapped above.
- `base/forms.py`: `CustomUserCreationForm`, `PostForm`, `ProfileForm`, `UserForm`.
- `base/filters.py`: `PostFilter`.
- `base/admin.py`: Django admin setup.
- `rhixecompany/settings.py`: `storages` installed; GCS backend commented out; `CKEDITOR_UPLOAD_PATH = "uploads/"`; `MEDIA_URL = "/images/"`; `MEDIA_ROOT` local.
- `.github/workflows/ci.yml`: ruff + Django test.
- `docs/scope/scope.md`: the output file.

## Pitfall (generalizable)

Never treat `docs/scope/` absence as greenfield when `.py` source files exist. Read `base/` first; enroll before decomposing. A greenfield scope written over a brownfield repo hides the real work order and produces phantom build tasks.
