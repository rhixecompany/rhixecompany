"""Smoke tests for base app models and views."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Post, Profile, Tag


class ModelTests(TestCase):
    """Basic model validation tests."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="Test",
            last_name="User",
            email="test@example.com",
        )
        self.tag = Tag.objects.create(name="test-tag")

    def test_profile_creation(self):
        """Test Profile model creation and string representation."""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(str(self.profile), "Test User")

    def test_tag_creation(self):
        """Test Tag model creation."""
        self.assertEqual(str(self.tag), "test-tag")

    def test_post_creation_and_slug_generation(self):
        """Test Post model creation and automatic slug generation."""
        post = Post.objects.create(
            headline="Test Post Headline",
            sub_headline="Test Subhead",
            body="Test body content",
            active=True,
            featured=False,
        )
        post.tags.add(self.tag)

        self.assertEqual(post.headline, "Test Post Headline")
        self.assertTrue(post.slug)
        self.assertIn("test-post-headline", post.slug)
        self.assertEqual(post.tags.count(), 1)

    def test_post_slug_uniqueness(self):
        """Test that duplicate headlines get unique slugs."""
        Post.objects.create(
            headline="Duplicate Title", body="Body 1", active=True
        )
        post2 = Post.objects.create(
            headline="Duplicate Title", body="Body 2", active=True
        )

        self.assertNotEqual(post2.slug, "duplicate-title")
        self.assertIn("duplicate-title-", post2.slug)


class ViewSmokeTests(TestCase):
    """Basic view smoke tests."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="viewuser", email="view@example.com", password="testpass123"
        )
        Profile.objects.create(user=self.user, email="view@example.com")
        self.post = Post.objects.create(
            headline="Published Post",
            body="Published content",
            active=True,
            featured=True,
        )

    def test_home_view(self):
        """Test home view returns 200."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_posts_view(self):
        """Test posts list view returns 200."""
        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view(self):
        """Test post detail view returns 200 for active post."""
        response = self.client.get(f"/post/{self.post.slug}/")
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """Test login page accessible."""
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        """Test registration page accessible."""
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
