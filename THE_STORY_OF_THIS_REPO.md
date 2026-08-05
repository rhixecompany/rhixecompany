# The Story of Profile

_The Django blog that learned to love the cloud_

---

## Prologue: The Blog That Needed Scale

"Just a blog." That's how it started. Posts, categories, tags, comments. Standard Django tutorial material.

**Then the images came.** High-res photos. Galleries. Featured images for every post. The `media/` folder grew to 50GB.

**Then the traffic came.** A post hit Hacker News. The VPS disk filled. The site went down.

**Lesson 1:** _Local media storage doesn't scale._

---

## Chapter 1: The Google Cloud Storage Migration

```python
# settings/production.py
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'profile-media-prod'
GS_PROJECT_ID = 'profile-project-123'
GS_CREDENTIALS = json.loads(os.environ['GCS_CREDENTIALS'])
```

**What changed:**

- `collectstatic` → uploads to GCS bucket
- `FileField.save()` → streams to GCS
- Template `{{ post.image.url }}` → serves from `https://storage.googleapis.com/...`
- No more `df -h` anxiety

**The cost:** ~$0.02/GB/month. The 50GB = $1/month. The VPS disk = free but finite.

---

## Chapter 2: CKEditor 5 — The Editor That Almost Worked

```python
# requirements.txt
django-ckeditor==6.4.0
```

```python
# models.py
class Post(models.Model):
    content = RichTextField(config_name='awesome')
```

```python
# settings/base.py
CKEDITOR_CONFIGS = {
    'awesome': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink', 'Image'],
            ['CodeSnippet'],
            ['Source'],
        ],
        'extraPlugins': 'codesnippet,image2',
        'codeSnippet_theme': 'monokai',
    }
}
```

**The good:** Clean HTML output. Code highlighting. Image upload via `image2` plugin.

**The bad:** `django-ckeditor` wraps CKEditor 4. CKEditor 5 requires a completely different integration (collaborative editing, different API). The team stayed on 4 because "migration is risky."

**The ugly:** Image upload in CKEditor 4 + GCS requires custom `image2` plugin config. Took 3 days to debug.

---

## Chapter 3: The Docker + GCP Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "profile.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: "3.8"
services:
  web:
    build: .
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [db]
  db:
    image: postgres:15
    volumes: [postgres_data:/var/lib/postgresql/data]
    env_file: .env
```

**Deploy to GCP Cloud Run:**

```bash
gcloud builds submit --tag gcr.io/profile-project/profile
gcloud run deploy profile --image gcr.io/profile-project/profile --platform managed
```

**Result:** Zero-config scaling. $0 when idle. SSL automatic. Custom domain mapped.

---

## Chapter 4: The Missing Pieces

| Feature    | Status | Notes                             |
| ---------- | ------ | --------------------------------- |
| CI/CD      | ❌     | No GitHub Actions                 |
| Tests      | ⚠️     | Only `python manage.py test`      |
| Monitoring | ❌     | No Sentry, no logging aggregation |
| Backups    | ⚠️     | Manual `pg_dump`                  |
| SEO        | ⚠️     | Basic meta tags only              |
| Analytics  | ❌     | No GA/Plausible                   |

**Why?** "It's just a blog. We'll add it later."

**Reality:** Later never comes. The blog runs. Posts publish. Images serve. The basics work.

---

## Chapter 5: The Consolidation Question

July 2025. Workspace has 17 projects. `profile` is one of two pure-Django projects (other: `ecom`).

| Project               | Stack              | Status            |
| --------------------- | ------------------ | ----------------- |
| `profile`             | Django + GCS       | Maintenance       |
| `ecom`                | Django 3.1 + React | Archive candidate |
| `rhixecompany-comics` | Django + Next.js   | **Survivor**      |

**Profile's fate:** Not a consolidation target. It's a standalone blog. Different purpose than the comic platforms.

**But:** It should get CI/CD. Tests. Monitoring. Before the next Hacker News hit.

---

## Epilogue: The Blog That Works

Posts publish. Images serve from GCS. CKEditor handles rich text. Gunicorn serves requests. Cloud Run scales.

No Kubernetes. No microservices. No message queues. No service mesh.

**Just Django. Just working.**

_Sometimes the best architecture is the one you don't have to think about._

---

_Written by the workspace chronicler, July 25, 2025.  
Filed at `projects/profile/THE_STORY_OF_THIS_REPO.md`._
