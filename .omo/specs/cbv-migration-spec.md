# Function-Based Views → Class-Based Views Migration Specification

**Project:** Django Blog CMS (`base/`)
**Spec Version:** 1.0
**Date:** 2026-10-14
**Status:** Planned
**Workflow Tier:** GA

---

## 1. Problem Statement

`base/views.py` contains **13 function-based views (FBVs)** handling all request logic. Project conventions (`base/AGENTS.md`, `copilot-instructions.md`) prefer **Class-Based Views (CBVs)**. Migration reduces boilerplate, enables built-in mixins (`LoginRequiredMixin`, `UserPassesTestMixin`), and improves maintainability.

---

## 2. Scope

### In Scope
- Refactor all 13 FBVs to CBV equivalents
- Preserve URL routing (`base/urls.py` unchanged)
- Preserve authentication/authorization logic (`@login_required`, `@admin_only`)
- Preserve template names and context variables
- Update `base/tests.py` to match CBV patterns

### Out of Scope
- New features or behavior changes
- API endpoint additions
- Template redesign (reuse existing templates)

---

## 3. View Mapping

| # | FBV | Current Decorators | CBV Equivalent | Mixins / Notes |
|---|-----|-------------------|----------------|----------------|
| 1 | `home` | — | `TemplateView` | `template_name="base/index.html"`; context: `posts` (featured, active, limit 3) |
| 2 | `posts` | — | `ListView` | `model=Post`; `paginate_by=5`; `filterset_class=PostFilter`; `template_name="base/posts.html"` |
| 3 | `post` | — | `DetailView` | `model=Post`; `slug_field=slug`; `template_name="base/post.html"`; context: `post`, `comment_form` |
| 4 | `profile` | `@login_required` | `TemplateView` | `LoginRequiredMixin`; context: `user.profile` |
| 5 | `createPost` | `@login_required`, `@admin_only` | `CreateView` | `LoginRequiredMixin`, `UserPassesTestMixin(test_func=is_admin)`; `form_class=PostForm`; `template_name="base/post_form.html"`; success: `post.get_absolute_url()` |
| 6 | `updatePost` | `@login_required`, `@admin_only` | `UpdateView` | Same mixins as create; `slug_field=slug`; `template_name="base/post_form.html"` |
| 7 | `deletePost` | `@login_required`, `@admin_only` | `DeleteView` | Same mixins; `slug_field=slug`; `template_name="base/delete.html"`; success: `reverse_lazy("posts")` |
| 8 | `sendEmail` | — | `FormView` | `form_class=ContactForm` (new); `template_name="base/contact.html"`; success: `reverse_lazy("email_sent")` |
| 9 | `loginPage` | — | `LoginView` | `template_name="base/login.html"`; `authentication_form=CustomAuthForm`; redirect authenticated |
| 10 | `registerPage` | — | `CreateView` | `form_class=CustomUserCreationForm`; `template_name="base/register.html"`; auto-login on success |
| 11 | `logoutUser` | — | `LogoutView` | `next_page="home"` |
| 12 | `userAccount` | `@login_required` | `DetailView` | `LoginRequiredMixin`; `model=User`; `template_name="base/account.html"`; context: `profile` |
| 13 | `updateProfile` | `@login_required` | `UpdateView` | `LoginRequiredMixin`; dual forms (`UserForm`, `ProfileForm`); `template_name="base/profile_form.html"` |

---

## 4. Implementation Details

### 4.1 Mixins
```python
# base/mixins.py (new file)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class AdminRequiredMixin(UserPassesTestMixin):
    """Restrict to staff/admin users."""
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
```

### 4.2 CBV Examples

```python
# base/views.py (refactored)
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
)
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from .mixins import AdminRequiredMixin
from .models import Post, PostComment
from .forms import PostForm, CustomUserCreationForm, UserForm, ProfileForm

class HomeView(TemplateView):
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(active=True, featured=True)[:3]
        return context


class PostListView(FilterView):
    model = Post
    template_name = "base/posts.html"
    paginate_by = 5
    filterset_class = PostFilter
    queryset = Post.objects.filter(active=True)


class PostDetailView(DetailView):
    model = Post
    template_name = "base/post.html"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = PostCommentForm()  # existing form
        return context


class PostCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "base/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user.profile  # or appropriate logic
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "base/post_form.html"
    slug_field = "slug"

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "base/delete.html"
    slug_field = "slug"
    success_url = reverse_lazy("posts")


class ContactView(FormView):
    template_name = "base/contact.html"
    form_class = ContactForm  # create from sendEmail logic
    success_url = reverse_lazy("email_sent")

    def form_valid(self, form):
        form.send_email()  # method on form
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "base/login.html"
    redirect_authenticated_user = True
    # authentication_form = CustomAuthForm  # if needed


class CustomRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "base/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # auto-login
        return response


class CustomLogoutView(LogoutView):
    next_page = "home"


class UserAccountView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "base/account.html"

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "base/profile_form.html"
    form_class = ProfileForm  # or multi-form handling

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "user_form" not in context:
            context["user_form"] = UserForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        # Handle dual form (UserForm + ProfileForm)
        self.object = self.get_object()
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=self.object)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("account")
        return self.render_to_response(self.get_context_data(
            user_form=user_form, profile_form=profile_form
        ))
```

### 4.3 URL Configuration (Unchanged)
```python
# base/urls.py - routes remain the same, view classes change
from .views import (
    HomeView, PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,
    ContactView, CustomLoginView, CustomRegisterView,
    CustomLogoutView, UserAccountView, ProfileUpdateView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("create_post/", PostCreateView.as_view(), name="create_post"),
    path("update_post/<slug:slug>/", PostUpdateView.as_view(), name="update_post"),
    path("delete_post/<slug:slug>/", PostDeleteView.as_view(), name="delete_post"),
    path("send_email/", ContactView.as_view(), name="send_email"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("account/", UserAccountView.as_view(), name="account"),
    path("update_profile/", ProfileUpdateView.as_view(), name="update_profile"),
]
```

---

## 5. Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | All 13 FBVs replaced with CBVs | `grep -c "def " base/views.py` → 0 (or only helper functions) |
| 2 | URL routes unchanged | `python manage.py show_urls` matches current routes |
| 3 | `@admin_only` → `AdminRequiredMixin` works | Staff can CRUD; non-staff get 403 |
| 4 | `@login_required` → `LoginRequiredMixin` works | Authenticated pages require login |
| 5 | Templates render with correct context | Manual test all 13 routes |
| 6 | Existing tests pass | `python manage.py test base.tests` |
| 7 | Pagination & filtering work | `PostListView` with `PostFilter` |
| 8 | Dual-form profile update works | `ProfileUpdateView` handles `UserForm` + `ProfileForm` |
| 9 | Auto-login on registration works | `CustomRegisterView.form_valid` logs in user |
| 10 | No regressions in post CRUD | Create, edit, delete posts as admin |

---

## 6. Migration Steps

1. **Create `base/mixins.py`** with `AdminRequiredMixin`
2. **Refactor views one by one** (recommended order: simple → complex):
   - `home` → `HomeView`
   - `posts` → `PostListView`
   - `post` → `PostDetailView`
   - `profile` → `ProfileView`
   - `logoutUser` → `CustomLogoutView`
   - `loginPage` → `CustomLoginView`
   - `registerPage` → `CustomRegisterView`
   - `sendEmail` → `ContactView`
   - `createPost` → `PostCreateView`
   - `updatePost` → `PostUpdateView`
   - `deletePost` → `PostDeleteView`
   - `userAccount` → `UserAccountView`
   - `updateProfile` → `ProfileUpdateView`
3. **Update `base/urls.py`** to use `.as_view()`
4. **Run tests** after each view: `python manage.py test base.tests`
5. **Manual smoke test** all routes
6. **Delete old FBV code** from `base/views.py`

---

## 7. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Context variable name changes | Medium | High | Explicitly set `context_object_name` where templates expect specific names |
| `PostFilter` integration | Medium | Medium | Use `django_filters.views.FilterView` for `PostListView` |
| Dual-form profile update | High | Medium | Implement custom `post()` in `ProfileUpdateView` |
| Admin decorators → mixins | Low | High | Test `AdminRequiredMixin` with non-staff users |
| Template form variable names | Medium | Medium | CBVs use `form` by default; templates already use `{{ form }}` |

---

## 8. Dependencies

- `django-filter` already installed (used by `PostFilter`)
- `django.contrib.auth.views` for `LoginView`, `LogoutView`
- Existing forms: `PostForm`, `CustomUserCreationForm`, `UserForm`, `ProfileForm`
- Existing templates: `post_form.html`, `login.html`, `register.html`, `account.html`, `profile_form.html`, `delete.html`, `contact.html`

---

## 9. Rollback Plan

If migration fails:
1. Git revert to pre-migration commit
2. No database migrations needed (views only)
3. `python manage.py test` should pass on original code