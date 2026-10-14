# FBV → CBV Migration Plan

**Spec:** `.omo/specs/cbv-migration-spec.md`
**Created:** 2026-10-14
**Status:** Planned
**Workflow:** GA (needs spec, build, verify, test, review, document)

---

## Plan Steps

### Phase 1: Design (Architect)
- [ ] Run `/architect FBV to CBV migration` → capture spec (`.omo/specs/cbv-migration-spec.md`)
- [ ] Review spec with stakeholders
- [ ] Approve spec → move to build

### Phase 2: Build (Develop) — View by View

#### 2.1 Foundation
- [ ] Create `base/mixins.py` with `AdminRequiredMixin`
- [ ] Add `context_object_name` where templates expect specific names

#### 2.2 Simple Views (TemplateView, LogoutView)
- [ ] `home` → `HomeView(TemplateView)` — context: `posts` (featured, active, limit 3)
- [ ] `logoutUser` → `CustomLogoutView(LogoutView)` — `next_page="home"`

#### 2.3 Auth Views (LoginView, CreateView)
- [ ] `loginPage` → `CustomLoginView(LoginView)` — `template_name="base/login.html"`, `redirect_authenticated_user=True`
- [ ] `registerPage` → `CustomRegisterView(CreateView)` — `form_class=CustomUserCreationForm`, auto-login in `form_valid`

#### 2.4 List/Detail Views (ListView, DetailView, FilterView)
- [ ] `posts` → `PostListView(FilterView)` — `model=Post`, `paginate_by=5`, `filterset_class=PostFilter`, `queryset=Post.objects.filter(active=True)`
- [ ] `post` → `PostDetailView(DetailView)` — `slug_field=slug`, context: `comment_form`

#### 2.5 Profile Views
- [ ] `profile` → `ProfileView(LoginRequiredMixin, TemplateView)` — context: `request.user.profile`
- [ ] `userAccount` → `UserAccountView(LoginRequiredMixin, DetailView)` — `model=User`, `get_object() → request.user`

#### 2.6 CRUD Views (CreateView, UpdateView, DeleteView)
- [ ] `createPost` → `PostCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView)` — `form_class=PostForm`, `template_name="base/post_form.html"`, `get_success_url() → object.get_absolute_url()`
- [ ] `updatePost` → `PostUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView)` — same as create, `slug_field=slug`
- [ ] `deletePost` → `PostDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView)` — `slug_field=slug`, `success_url=reverse_lazy("posts")`

#### 2.7 Complex Forms
- [ ] `sendEmail` → `ContactView(FormView)` — `form_class=ContactForm`, `form_valid()` calls `form.send_email()`
- [ ] `updateProfile` → `ProfileUpdateView(LoginRequiredMixin, UpdateView)` — dual form handling (`UserForm` + `ProfileForm`) in custom `post()`

#### 2.8 URL Configuration
- [ ] Update `base/urls.py` to use `.as_view()` for all 13 routes

#### 2.9 Cleanup
- [ ] Remove old FBV functions from `base/views.py`
- [ ] Keep only helper functions and mixins

### Phase 3: Verify
- [ ] Run `/check verify FBV to CBV migration`
  - [ ] `grep -c "def " base/views.py` → 0 (or only helpers/mixins)
  - [ ] `python manage.py show_urls` → routes match original
  - [ ] `AdminRequiredMixin` blocks non-staff (403)
  - [ ] `LoginRequiredMixin` requires auth
  - [ ] Templates render with correct context
  - [ ] `PostListView` pagination + `PostFilter` work

### Phase 4: Test
- [ ] Run `/test FBV to CBV migration`
  - [ ] `python manage.py test base.tests` — all pass
  - [ ] Manual: Home → posts list → post detail
  - [ ] Manual: Login → register → logout
  - [ ] Manual: Admin create/edit/delete post
  - [ ] Manual: Profile view → update profile (dual form)
  - [ ] Manual: Contact form → email sent page
  - [ ] Manual: Staff-only routes return 403 for non-staff

### Phase 5: Review (GA)
- [ ] Run `/check review FBV to CBV migration`
  - [ ] Standards: CBVs used per conventions
  - [ ] Spec adherence: All 13 views migrated, no behavior change
  - [ ] Security: Auth/authorization preserved

### Phase 6: Document
- [ ] Run `/document FBV to CBV migration`
  - [ ] Update `CHANGELOG.md`
  - [ ] Update `docs/scope/scope.md` → mark feature 9 as `done`
  - [ ] Update `.omo/plans/cbv-migration-plan.md` with final verification notes

---

## Validation Checklist (from Spec)

| # | Criterion | Status |
|---|-----------|--------|
| 1 | All 13 FBVs replaced with CBVs | ☐ |
| 2 | URL routes unchanged | ☐ |
| 3 | `@admin_only` → `AdminRequiredMixin` works | ☐ |
| 4 | `@login_required` → `LoginRequiredMixin` works | ☐ |
| 5 | Templates render with correct context | ☐ |
| 6 | Existing tests pass | ☐ |
| 7 | Pagination & filtering work | ☐ |
| 8 | Dual-form profile update works | ☐ |
| 9 | Auto-login on registration works | ☐ |
| 10 | No regressions in post CRUD | ☐ |

---

## View Migration Order (Recommended)

| Order | FBV | CBV | Complexity | Notes |
|-------|-----|-----|------------|-------|
| 1 | `home` | `HomeView` | Low | TemplateView, static context |
| 2 | `logoutUser` | `CustomLogoutView` | Low | LogoutView, redirect |
| 3 | `loginPage` | `CustomLoginView` | Low | LoginView, built-in |
| 4 | `registerPage` | `CustomRegisterView` | Medium | CreateView + auto-login |
| 5 | `posts` | `PostListView` | Medium | FilterView + pagination |
| 6 | `post` | `PostDetailView` | Medium | DetailView + comment form |
| 7 | `profile` | `ProfileView` | Low | TemplateView + login required |
| 8 | `userAccount` | `UserAccountView` | Low | DetailView + get_object |
| 9 | `createPost` | `PostCreateView` | Medium | CreateView + AdminRequiredMixin |
| 10 | `updatePost` | `PostUpdateView` | Medium | UpdateView + slug |
| 11 | `deletePost` | `PostDeleteView` | Medium | DeleteView + slug |
| 12 | `sendEmail` | `ContactView` | Medium | FormView + email logic |
| 13 | `updateProfile` | `ProfileUpdateView` | High | Dual form + custom post() |

---

## Dependencies
- `django-filter` (for `FilterView` + `PostFilter`)
- `django.contrib.auth.views` (`LoginView`, `LogoutView`)
- Existing forms: `PostForm`, `CustomUserCreationForm`, `UserForm`, `ProfileForm`
- Existing templates (reused, no changes expected)

---

## Rollback
If any phase fails:
1. `git checkout -- base/views.py base/urls.py base/mixins.py`
2. `python manage.py test base.tests` — should pass on original FBVs
3. No database migrations needed (views only)