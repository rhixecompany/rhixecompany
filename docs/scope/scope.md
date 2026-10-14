# Scope: Django Blog CMS

A Django blog and CMS that lets staff publish posts with rich text (CKEditor 5) and stores images on GCS. Target audience: staff editors who create and manage content, and readers who browse and comment. The existing Django app (`base/`) handles posts, profiles, comments, filtering, pagination, auth, and admin CRUD. This scope keeps the existing code intact and adds the GCS media layer and a clear staff publishing workflow.

**Build approach:** Journey (deliver one complete user journey fully before starting the next; depth first per journey, not a thin thread across everything).
**Workflow:** GA (after `/develop`, `/check verify`, `/test`, a fresh model `/check review`, then `/document`; most features need a spec; `Assumed` specs stay flagged).

_These are recommendations, not orders. Skip anything that does not fit: if a feature is already built and complete, it carries no build box. If you already know how to build a feature, you may skip `/architect`, though at GA the decision gate is the safer default. You decide when a feature is `done`._

## At a glance

| # | Feature | Phase | Status |
|---|---------|-------|--------|
| A | Stack and architecture | Foundation | existing |
| B | Data model (Profile, Post, Tag, PostComment) | Foundation | existing |
| C | Auth and user accounts | Foundation | existing |
| D | Design system and templates | Foundation | existing |
| E | Coding standards and tooling | Foundation | existing |
| 1 | GCS image uploads | Publishing Journey | planned |
| 2 | Post publishing workflow | Publishing Journey | planned |
| 3 | Post listing and pagination | Publishing Journey | existing |
| 4 | Post detail and comments | Publishing Journey | existing |
| 5 | User registration and profile | Account Journey | existing |
| 6 | User account and profile update | Account Journey | existing |
| 7 | Email and contact form | System | existing |

## Foundations

### A. Stack and architecture · existing
Django 4.x with PostgreSQL (local SQLite for dev), Gunicorn, WhiteNoise (static files), CKEditor 5, GCS media storage (planned), crispy forms, django filters. The scaffold runs locally (`python manage.py runserver`) and passes build.
**Done when:** the stack is recorded and the empty scaffold boots locally and passes build.
- [x] Decide the stack (spec): `/architect stack and architecture`
- [x] Scaffold from the decision: `/develop stack and architecture`
- [x] Smoke check it runs: `/test`
Spec (existing) · code in `base/` and `rhixecompany/`

### B. Data model · existing
Core entities: Profile (user, image, bio), Post (headline, sub headline, body via `RichTextUploadingField`, thumbnail, active, featured, tags, slug), Tag (name), PostComment (author, post, body, created). Relationships: User-Profile one to one; Post-Tag many to many; Profile-Comment and Post-Comment one to many.
**Done when:** entities and relationships support the publishing and account journeys without a breaking migration.
- [x] Design it (spec): `/architect data model`
- [x] Build it: `/develop data model`
- [x] Verify it: `/check verify data model`
- [x] Test it: `/test data model`
Spec (existing, migrations 0001-0015) · code in `base/models.py`

### C. Auth and user accounts · existing
Django auth (login, register, logout) plus user account and profile update forms (`CustomUserCreationForm`, `ProfileForm`, `UserForm`). Staff access to CRUD is protected by `@admin_only` and `@login_required`.
**Done when:** staff can sign in, register, log out, and update their profile; admin only CRUD is protected.
- [x] Design it (spec): `/architect auth and user accounts`
- [x] Build it: `/develop auth and user accounts`
- [x] Verify it: `/check verify auth and user accounts`
- [x] Test it: `/test auth and user accounts`
Spec (existing) · code in `base/views.py`, `base/forms.py`

### D. Design system and templates · existing
Bootstrap 4 with crispy forms; CKEditor vendor files in `base/static/admin/` and `base/static/ckeditor/`. Templates use `base/index.html`, `base/post_form.html`, `base/posts.html`, `base/post.html`, `base/profile.html`, `base/account.html`.
**Done when:** base templates render for home, posts, post, profile, account, and admin forms.
- [x] Design it (spec): `/architect design system and templates`
- [x] Build it: `/develop design system and templates`
- [x] Verify it: `/check verify design system and templates`
- [x] Test it: `/test design system and templates`
Spec (existing) · code in `templates/` and `base/static/`

### E. Coding standards and tooling · existing
`ruff` (line length 120), `.editorconfig` (4 spaces `.py`, 2 spaces `.md`), `.ruff.toml` (`lf` line endings), Django `TestCase`. CI pipeline (`.github/workflows/ci.yml`) runs ruff check and `python manage.py test`. Virtual environment (`myvenv/`) is active.
**Done when:** lint and format run clean, CI passes, and conventions are recorded in root `AGENTS.md`.
- [x] Capture conventions + tooling choices: `/audit`
- [x] Install the tooling: `/develop tooling`
- [x] Check it runs clean: `/test`
Spec (existing) · code in `.github/workflows/ci.yml`, `AGENTS.md`

## Phase 1: Publishing Journey

*Complete user journey: staff creates or updates a post with GCS-stored images, confirms the publish state (draft, featured, active), and sees it in the feed. Every step of that path, all states, and the GCS storage layer must be complete before the next journey starts. Other journeys (user account management) are deferred entirely to Phase 2, not thinned versions sprinkled in here.*

### 1. GCS image uploads · planned · needs a decision · GA · Needs spec: yes
Enable GCS backed uploads for post thumbnails (`thumbnail`) and CKEditor uploads (`uploads/`). The `storages` package is installed; the GCS backend needs the real GCS keys and bucket name. Images must upload successfully, store in GCS, and render on the public page.
**Done when:** thumbnail and CKEditor uploads write to GCS, the uploaded URLs load in the browser, and an empty or broken upload state renders gracefully.
- [ ] Design it (spec): `/architect GCS image uploads`

Note: because the feature implies a provider and storage choice (GCS key configuration, bucket naming, `STORAGES_BACKEND`, `CKEDITOR_UPLOAD_PATH`), it needs a spec before build.

### 2. Post publishing workflow · planned · needs a decision · GA · Needs spec: yes
Clarify the staff publishing journey: how `draft`, `featured`, and `active` interact; whether staff see only their own posts; whether a confirmation or preview step exists before publish; and how editing before a cutoff works. The existing `admin_only` CRUD handles create/update/delete but does not describe the staff facing state machine.
**Done when:** staff can move a post through its full life cycle (draft to featured to active, or back), edit before a cutoff, and see confirmation; the feed reflects the final state.
- [ ] Design it (spec): `/architect post publishing workflow`

Note: the feature implies a design decision (state machine, staff interaction, preview/confirmation steps, edit before cutoff) that the engineer has not made. It needs a spec.

### 3. Post listing and pagination · existing
Public list with pagination (5 per page) and filtering (`PostFilter` by tags, active, featured). Code handles pagination errors (`EmptyPage`, `PageNotAnInteger`).
**Done when:** the list renders with filters applied, pagination links work, and empty/error states render.
- [x] Design it (spec): `/architect post listing and pagination`
- [x] Build it: `/develop post listing and pagination`
- [x] Verify it: `/check verify post listing and pagination`
- [x] Test it: `/test post listing and pagination`
Spec (existing) · code in `base/views.py`, `base/filters.py`

### 4. Post detail and comments · existing
Individual post page (`post/<slug:slug>/`) with CKEditor body, tags, thumbnail, and a comment form. Comments create via `PostComment` (author from `request.user.profile`). Success message shows after comment.
**Done when:** a reader can view the full post, submit a comment, see a confirmation message, and see errors handled gracefully (e.g., missing profile).
- [x] Design it (spec): `/architect post detail and comments`
- [x] Build it: `/develop post detail and comments`
- [x] Verify it: `/check verify post detail and comments`
- [x] Test it: `/test post detail and comments`
Spec (existing) · code in `base/views.py`, `base/forms.py`

## Phase 2: Account Journey

*Complete user journey: user creates an account, updates their profile and user details, and sees the updated state. All steps fully polished before any other journey opens.*

### 5. User registration and profile · existing
Registration (`CustomUserCreationForm`) creates the user and logs them in. Profile creation links user to `Profile`. Login (`loginPage`) uses email lookup. Logout (`logoutUser`) redirects to home.
**Done when:** a user can register, log in, log out, and the profile is linked correctly.
- [x] Design it (spec): `/architect user registration and profile`
- [x] Build it: `/develop user registration and profile`
- [x] Verify it: `/check verify user registration and profile`
- [x] Test it: `/test user registration and profile`
Spec (existing) · code in `base/views.py`, `base/forms.py`

### 6. User account and profile update · existing
Account page (`userAccount`) shows the profile. Update (`updateProfile`) allows editing user info (`UserForm`) and profile details (`ProfileForm`) with image upload.
**Done when:** a logged-in user can update their details and profile picture; the updated state is visible.
- [x] Design it (spec): `/architect user account and profile update`
- [x] Build it: `/develop user account and profile update`
- [x] Verify it: `/check verify user account and profile update`
- [x] Test it: `/test user account and profile update`
Spec (existing) · code in `base/views.py`

## Phase 3: System and Integration

*Supporting capabilities that complete the product. These are real but lower priority than the core journeys; they stay minimal and do not block the primary paths.*

### 7. Email and contact form · existing
Contact form (`sendEmail`) renders `email_template.html`, sends via Django `EmailMessage`, and shows `email_sent.html`. The email backend is SMTP (`smtp.gmail.com`) but host/user/password are placeholder values (`YOU_EMAIL`, `YOU_EMAIL_PASSWORD`).
**Done when:** the form submits, the email sends (or fails with a clear message), and the sent page renders.
- [x] Design it (spec): `/architect email and contact form`
- [x] Build it: `/develop email and contact form`
- [x] Verify it: `/check verify email and contact form`
- [x] Test it: `/test email and contact form`
Spec (existing) · code in `base/views.py`, `base/templates/`
Note: the GCS media layer (feature 1) requires a working email backend only if notifications are added; notifications are deferred, so the placeholder email settings are acceptable for now.

## Phase 4: Technical Debt & Modernization

*These are internal improvements that reduce risk and modernize the stack without changing user-facing behavior. They are planned after the core journeys complete.*

### 8. CKEditor 4 → 5 migration · planned · needs a decision · GA · Needs spec: yes
Migrate from `django-ckeditor` (CKEditor 4.22.1, end-of-life, security warnings) to `django-ckeditor-5`. CKEditor 4 bundles unsupported code with unfixed CVEs. The migration requires: package swap (`django-ckeditor-5`), model field change (`RichTextUploadingField` → `CKEditor5Field`), template/widget updates (`ckeditor/` templates, admin overrides), and GCS upload path compatibility (`CKEDITOR_UPLOAD_PATH` → `CKEDITOR_5_CONFIGS['default']['filebrowser']['uploadUrl']`).
**Done when:** admin and post forms use CKEditor 5, uploads write to GCS, no CKEditor 4 assets remain, and the Django system check warning is resolved.
- [ ] Design it (spec): `/architect CKEditor 4 to 5 migration`

Note: this is a breaking change to the editor component; it needs a spec to capture widget configs, GCS integration, and any custom toolbar/plugins.

### 9. Function-based views → Class-based views migration · planned · needs a decision · GA · Needs spec: yes
Refactor the 13 function-based views in `base/views.py` (`home`, `posts`, `post`, `profile`, `createPost`, `updatePost`, `deletePost`, `sendEmail`, `loginPage`, `registerPage`, `logoutUser`, `userAccount`, `updateProfile`) to Django Class-Based Views (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`, `FormView`, `LoginView`, `LogoutView`). Benefits: reduced boilerplate, built-in mixins (`LoginRequiredMixin`, `UserPassesTestMixin`), consistent pagination/filtering, and alignment with `base/AGENTS.md` and `copilot-instructions.md` conventions.
**Done when:** all FBVs replaced with CBVs, URL routing unchanged, existing tests pass, and admin `@admin_only`/`@login_required` logic preserved via mixins.
- [ ] Design it (spec): `/architect FBV to CBV migration`

Note: this touches every request handler; it needs a spec to map each FBV to its CBV equivalent, define mixin strategy, and verify no behavior regressions.

### 10. GCS → Cloudinary media storage migration · planned · needs a decision · GA · Needs spec: yes
Migrate media and static file storage from Google Cloud Storage (`storages.backends.gcloud.GoogleCloudStorage`) to Cloudinary (`cloudinary_storage`). Cloudinary provides automatic image optimization, transformations, CDN delivery, and a generous free tier. Migration requires: package swap (`django-cloudinary-storage` replaces `django-storages[google]`), settings update (`DEFAULT_FILE_STORAGE`, `STATICFILES_STORAGE`), Cloudinary credentials configuration (`CLOUDINARY_URL` or `CLOUDINARY_CLOUD_NAME`/`API_KEY`/`API_SECRET`), and CKEditor 5 upload integration with Cloudinary. Existing GCS assets remain accessible via their URLs; new uploads go to Cloudinary.
**Done when:** `DEFAULT_FILE_STORAGE` and `STATICFILES_STORAGE` use Cloudinary backend, uploads (thumbnails, CKEditor images) write to Cloudinary, existing GCS URLs still work, and no `storages.backends.gcloud` references remain in settings.
- [ ] Design it (spec): `/architect GCS to Cloudinary migration`

Note: this is a storage backend change with zero-downtime requirements (existing GCS URLs must remain accessible); it needs a spec to capture credential management, migration strategy, and CKEditor integration.

## Deferred

Features out of scope for the current build pass, kept so the plan stays honest and does not grow unexpectedly.

- **Full text search across posts**: deferred. The existing `PostFilter` handles tag and active filtering; full text search needs a spec (search index, query parser) and is not required for the smallest working version.
- **Staff analytics dashboard**: deferred. No analytics feature for this scope; just basic Django behavior.
- **Email notifications** (new post or comment): deferred. The contact form exists but notification events require a spec (event triggers, templates, delivery guarantees) and are not required.
- **Public API for posts**: deferred. Not part of the smallest working version.
- **Chat and integration posting**: deferred. Not part of the smallest working version.
- **Advanced performance** (CDN, image optimization pipeline): deferred. The basic performance tier (existing WhiteNoise and pagination) is sufficient; advanced optimization needs a spec.
- **Internationalization and RTL layout**: deferred. English only for this scope.
- **SEO metadata, sitemap, structured data**: deferred. The user stated the app is internal/staff focused and no SEO is needed; no SEO feature row is added.
- **Cookie consent and GDPR banner**: deferred. No legal or compliance feature is required for this staff facing internal tool; no cookie consent row is added.

## Legend

**The decision box.** Every feature carries exactly one: the sub-task whose label ends with `(spec)`. For a planned feature with `needs a decision`, that box is `Design it (spec): /architect <feature>`. For a planned feature without a decision, it is `Build it: /develop <feature>`. The next step is always the first unticked box.

**Feature lifecycle.** The scope updates as a feature moves; each row shows what it is and who sets it:

| State | Set by | The feature shows |
|---|---|---|
| `planned` · needs a decision | `/scope` | one box: `Design it (spec): /architect <feature>` |
| `planned` · no decision needed | `/scope` | one box: `Build it: /develop <feature>` |
| `in-progress` (designed) | `/architect` at spec capture | `Design it` ticked; spec linked; `Build it` + 2 to 5 milestones rolled up from the spec; the tier's closing boxes (`Verify it`, `Test it`, `Review it`, `Document it` at GA) |
| `in-progress` (building) | `/develop` | milestone sub-boxes tick one by one; code pointer filled |
| `in-progress` (verified) | `/check verify` | `Build it` + milestones ticked; `Verify it` ticked |
| `done` | you, when you decide | boxes ticked; skipped ones marked skipped; at GA, the last stage (`/test`) closes it |

**Journey approach.** This scope uses the Journey approach: one complete user journey per phase. Phase 1 (Publishing Journey) must finish fully — every step of staff publishing with GCS uploads — before Phase 2 (Account Journey) begins. Deferred journeys (analytics, notifications, API) are kept out, not thinned.

**Status.** `planned` → `in-progress` → `done`, plus `existing` (pre-workflow, complete) and `dropped` (de-scoped, kept for history). `existing` is not `done`: it predates the workflow; `/develop` and `/sync` leave it alone. `replan` may set a feature to `dropped`; never delete rows.

**Approach tag.** A tag beside a heading (e.g., `· Facade`) overrides the project default. No tag = inherit the default (`Journey`). This scope uses the project default for every feature; no override tags are set.

**Workflow tier.** The project default is `GA` (`**Workflow:** GA`). A feature can override with a tag (`· Prototype`, `· Beta`); no tag = inherit GA. At GA, most features are `Needs spec: yes`, and the full verification chain (`/check verify`, `/test`, `/check review`, `/document`) applies. `Assumed` specs stay flagged but never block `done`.

**Pointer line.** A line (`spec <n> · code in <path>`) appears only once those exist: the spec link is added by `/architect` at capture, the code path by `/develop`.

**Accessibility note.** A minimal note (no separate feature build) that public pages should meet WCAG AA. It does not add a build box; it informs the spec capture for features 1 and 2.

**References level.** None. No `## References` section is added; the scope reads clean. Recommendations that are not user dictated carry no citation.

## /scope plan · Django blog CMS

**6 features planned (5 existing + 2 planned: GCS uploads and publishing workflow), build approach Journey, workflow GA.**
Next: `/clear`, then `/architect GCS image uploads` (the first planned feature with `needs a decision`; the entry command is the single box `Design it (spec): /architect GCS image uploads`).
Heads up: both planned features (`GCS image uploads`, `post publishing workflow`) are `needs a decision` at GA; they need specs before build. The existing features (`post listing`, `post detail`, `user registration`, `email`) are `existing` and do not need new work unless you extend them.
Scope written to `docs/scope/scope.md`.
