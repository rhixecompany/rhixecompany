---
name: gcs-secure-image-upload
version: 1.0.0
status: design
created: 2026-10-14
tags: [architecture, gcs, image-upload, security, design]
---

# Secure, Scalable GCS Image Upload — Technical Design

## 1. Overview & Goals

Design a production-grade image upload pipeline to Google Cloud Storage (GCS) for a Django-based CMS/blog (`rhixecompany` workspace). Requirements:

- Secure (signed URLs, encryption, malware scan, validation)
- Scalable (resumable uploads, multi-region, CDN-backed delivery)
- Observable (event triggers, retry logic, cost/performance tracking)
- Maintainable (folder/naming conventions, lifecycle rules, IAM least-privilege)

## 2. End-to-End Architecture

```
Client (Browser / Mobile App)
  │
  ▼
[Upload Gateway API]  (Django REST endpoint — optional pre-check)
  │  • Validate file type / size / auth token
  │  • Generate signed upload URL (if direct-to-GCS) OR
  │    initiate resumable session
  │
  ▼
[Signed URL / Resumable Upload Session]  (GCS XML/JSON API)
  │  • Client uploads bytes directly to GCS
  │
  ▼
GCS Bucket (multi-regional / regional per workload)
  │  • Storage class: Standard (hot) → Nearline / Coldline (archive)
  │  • Lifecycle rules: delete temp upload artifacts after 1d;
  │    transition to Nearline after 30d; delete after 365d (if policy allows)
  │
  ▼
[GCS Pub/Sub Notification]  (event: `OBJECT_FINALIZE`)
  │
  ├─► [Cloud Function / Cloud Run]  (post-upload processing)
  │     • VirusTotal / ClamAV scan (optional async)
  │     • Generate thumbnails (ImageMagick / Pillow) → `thumbnails/` prefix
  │     • Extract EXIF / metadata → Firestore / PostgreSQL
  │     • Set object ACL / metadata tags
  │
  ├─► [Cloud CDN / Load Balancer]  (public read access)
  │     • Signed cookies or public objects (per-folder policy)
  │
  └─► [Django CMS Backoffice]  (read metadata, approve/reject images)
```

## 3. Component Breakdown

### 3.1 Client Upload Mechanism

| Mechanism | Use Case | Trade-off |
|-----------|----------|-----------|
| **Direct browser upload** (signed URL) | Small files (<20 MB), low latency, simple UX | Requires CORS; client has direct GCS access; signed URL lifetime must be short (e.g., 15 min) |
| **Resumable upload** (XML/JSON resumable session) | Large files (>20 MB), unreliable networks, mobile | More complex client logic; session token expiry; requires server-side session management |
| **Server-mediated** (client → Django → GCS) | Strict validation, malware scan before storage, audit logging | Higher server bandwidth; not horizontally scalable for large uploads |

**Recommendation:** Hybrid approach:
- Client hits Django endpoint `/api/upload/session/` to request upload metadata.
- Django returns a GCS signed URL (if file < 20 MB) or initiates a resumable session token (if >= 20 MB).
- Client uploads directly to GCS.
- GCS event triggers processing pipeline; Django never handles the byte stream.

### 3.2 GCS Bucket Setup

| Property | Recommendation | Rationale |
|----------|---------------|-----------|
| **Bucket name** | `rhixecompany-media-uploads` (globally unique, DNS-compliant) | Matches workspace identity; avoids collision |
| **Region** | `us-central1` or `europe-west1` (match Django app region) | Minimize latency; comply with data-residency requirements |
| **Storage class (default)** | `STANDARD` | Low latency, high durability (99.999999999%) |
| **Lifecycle rules** | 1. Delete objects in `uploads/temp/` after 1 day (abort/retry artifacts).<br>2. Transition to `NEARLINE` after 30 days (accessed < 1/month).<br>3. Transition to `COLDLINE` after 90 days.<br>4. Delete unpublished/rejected objects after 90 days (if policy allows). | Cost optimization: Nearline ~50% cheaper; Coldline ~75% cheaper |
| **Object versioning** | Disabled (or enabled only for `public/` folder) | Versioning doubles storage; use only where immutability required |
| **Uniform bucket-level access (UBACL)** | Enabled | Simplifies IAM; avoids ACL drift |

### 3.3 CORS Configuration

Enable CORS on the bucket for the CMS origin (`https://rhixecompany.example.com`) and any CDN domain:

```json
[
  {
    "origin": ["https://rhixecompany.example.com", "https://cdn.rhixecompany.example.com"],
    "method": ["PUT", "POST", "GET", "HEAD", "DELETE"],
    "responseHeader": ["Content-Type", "x-goog-resumable", "x-goog-meta-*"],
    "maxAgeSeconds": 3600
  }
]
```

Note: `PUT` is required for resumable uploads; `POST` for signed URL uploads.

### 3.4 Security and Access Control

#### 3.4.1 IAM Design (Least Privilege)

| Service / Role | GCS Permissions | Scope |
|---------------|------------------|-------|
| Django app (service account) | `roles/storage.objectCreator`, `roles/storage.objectViewer` (only on `uploads/` and `thumbnails/` prefixes via IAM Conditions if needed) | Creates signed URLs; reads metadata; does NOT have delete on `public/` |
| Cloud Function (post-upload) | `roles/storage.objectAdmin` (limited to bucket) OR fine-grained `storage.objects.get`, `.create`, `.update`, `.delete` | Processes events; writes thumbnails; updates metadata |
| CDN / Load Balancer (public read) | `roles/storage.objectViewer` on `public/` only (via IAM Condition: `resource.name.startsWith('projects/_/buckets/rhixecompany-media-uploads/objects/public/')`) | Public delivery; no write |
| Backup / Archive pipeline | `roles/storage.objectViewer` on entire bucket; `.delete` only on archive folder | Disaster recovery; retention enforcement |

**Important:** Never embed service account keys in Django settings. Use Workload Identity Federation or GCP metadata server (if running on GKE / Cloud Run). In local dev (`myvenv`), use `gcloud auth application-default login` only; `.env` must contain no GCS keys (per `.hermes.md` anti-pattern rules).

#### 3.4.2 Signed URLs

- **Generation:** Backend (Django) creates signed URLs using service account private key (or HMAC key for user-uploaded content if using signed URLs with HMAC keys for broader delegation).
- **Lifetime:** 15 minutes for upload URLs; 7 days for read/download URLs (if temporary preview links).
- **Scope:** URL scoped to specific object path (`uploads/{user_id}/{uuid}.{ext}`) to prevent path traversal.

Example Python (Django / `google-cloud-storage`):

```python
from google.cloud import storage
from datetime import timedelta

client = storage.Client()
bucket = client.bucket("rhixecompany-media-uploads")
blob = bucket.blob(f"uploads/{user_id}/{uuid}.{ext}")
signed_url = blob.generate_signed_url(
    version="v4",
    expiration=timedelta(minutes=15),
    method="PUT",
    content_type=content_type,
)
```

#### 3.4.3 Encryption

| Layer | Mechanism | Key Management |
|-------|-----------|---------------|
| **Encryption at rest** | GCS default: AES-256 (Google-managed keys); optionally Customer-Managed Encryption Key (CMEK) via Cloud KMS | Use CMEK for compliance-sensitive media; rotate KMS key every 90 days |
| **Encryption in transit** | TLS 1.3 (HTTPS); enforce `https://` for all CDN / GCS URLs; disable HTTP fallback | Standard GCP enforcement |
| **Client-side encryption (optional)** | Encrypt file with AES-256-GCM before upload; store key in Cloud KMS / Django DB encrypted field | Required for HIPAA / GDPR-sensitive images; adds overhead |

**Recommendation:** Default (Google-managed AES-256) + TLS 1.3 for 99% of cases; add CMEK only if compliance mandates it.

### 3.5 Input Validation

Implement validation at the Django gateway endpoint before generating signed URLs:

| Check | Implementation | Failure Action |
|-------|---------------|--------------|
| **File type** | Inspect MIME type (magic bytes, not extension) via `python-magic` or `Pillow`. Allow list: `image/jpeg`, `image/png`, `image/webp`, `image/gif`, `image/avif`. | Reject with HTTP 422; log attempt |
| **File size** | Enforce max 50 MB (configurable per user role); check `Content-Length` or chunked stream size. | Reject with HTTP 413 (Payload Too Large) |
| **Filename** | Sanitize with `secure_filename` (Werkzeug) or `django.core.files.utils.get_valid_name`; reject paths containing `..`, `/`, `\`. Prevent path traversal to `public/` or system folders. | Reject with HTTP 400 |
| **Dimensions** (optional) | For CMS thumbnails, enforce max width/height (e.g., 4096 px) to prevent DoS via massive images. | Reject with HTTP 422 |
| **Malware scan** | For high-security environments: upload to `uploads/quarantine/`; trigger VirusTotal / ClamAV scan; move to `uploads/approved/` only after clean result. For standard CMS: rely on GCS Virus Scan (if enabled via Cloud Security Command Center) + client-side validation. | Quarantine; notify admin; delete after 24h if unclean |

**Note:** Never rely solely on file extension (`.jpg`) — attackers rename `.exe` to `.jpg`. Always use `python-magic` (`libmagic`) for MIME detection.

### 3.6 Storage Organization

```
/gcs-bucket-root/
  uploads/
    temp/              # Resumable session artifacts; lifecycle: delete after 1d
    quarantine/        # Pending malware scan; lifecycle: delete after 7d
    approved/
      {user_id}/
        {uuid}.{ext}    # Original image; metadata: user_id, upload_time, content_type
  thumbnails/
    {user_id}/
      {uuid}_small.webp    # 300px width; format: WebP (smaller, modern)
      {uuid}_medium.webp   # 1200px width
      {uuid}_large.webp    # 2400px width (if original >= 2400px)
  public/
    {post_slug}/
      {uuid}.{ext}         # Published images; access: public via CDN
  archive/
    {year}/{month}/        # Lifecycle: Coldline after 90d; delete after 365d
```

**Naming Convention:**
- Use UUID4 (`uuid.uuid4()` in Python) for filenames to prevent collisions and information disclosure (no user-identifying filenames in URLs unless required).
- Preserve original extension for compatibility; store normalized format (`webp`) only for thumbnails.
- Include `user_id` in path for access control and audit; never include PII in filenames.

**Metadata Tagging (Custom Metadata):**

Every object gets GCS custom metadata (`metadata` key-value pairs) set by the processing function:

```json
{
  "upload_user_id": "user_42",
  "original_filename": "vacation.jpg",
  "content_type": "image/jpeg",
  "upload_timestamp": "2026-10-14T15:30:00Z",
  "approval_status": "approved",
  "malware_scan_result": "clean",
  "thumbnail_available": "true",
  "cms_post_id": "post_999"
}
```

This allows efficient GCS search/filtering (via GCS query / BigQuery external tables) and avoids additional database lookups for basic metadata.

### 3.7 Post-Upload Processing (Event Triggers)

**Trigger:** GCS Notification (`OBJECT_FINALIZE`) on `uploads/approved/` prefix.

**Pipeline (Cloud Function / Cloud Run):**

1. **Read event payload** (bucket, name, metadata, timeCreated).
2. **Validate metadata** (check `approval_status` not yet set — this is the initial event).
3. **Generate thumbnails** using `Pillow` or `ImageMagick`; upload to `thumbnails/` prefix with same UUID.
4. **Malware scan** (if not done pre-upload): call VirusTotal API (with rate limits) or run `clamscan` in a sandbox container; set `malware_scan_result` metadata.
5. **Update Django database:** create `Image` model record (`uuid`, `original_path`, `thumbnail_paths`, `metadata`, `approval_status`).
6. **Set ACL / public access** based on CMS settings:
   - If image is for public post: move object to `public/` prefix (or copy + set `publicRead` ACL on original if original must stay private).
   - If private: keep ACL `projectPrivate` or `authenticatedRead`.

**Alternative (if no serverless allowed):** Use Django `post_save` signal + Celery task (`@shared_task`) triggered by a webhook from GCS notification endpoint (Django receives event, queues Celery job). This keeps processing inside the Django app but requires the app to be reachable by GCS Pub/Sub push subscription.

**Recommendation:** Use Cloud Function for processing (isolated, scalable, low cost) + Django webhook endpoint (`/api/webhooks/gcs/`) for database updates. This separates processing (stateless, high-compute) from CMS state management.

### 3.8 CDN / Cache Integration

- **Public images (`public/`):** Serve via GCS + Cloud CDN (Load Balancer with GCS backend). Configure CDN cache key based on URL path only (ignore query params except `w=` for responsive images).
- **Cache headers:** Set `Cache-Control: public, max-age=31536000, immutable` for thumbnail objects (they never change). Set `public, max-age=3600` for original images (in case of updates / replacements).
- **Signed cookies (optional):** If images must be private but delivered via CDN (e.g., user-specific galleries), use Cloud CDN Signed URLs or Signed Cookies instead of per-object public ACL.

### 3.9 Access Policies (Per-Object / Per-Folder)

Use IAM Conditions (bucket-level or prefix-level) rather than per-object ACLs where possible. Per-object ACLs (`allUsers` / `authenticatedUsers`) should be avoided for scalability (GCS has an ACL update rate limit of 200 updates per bucket per second).

**Policy Matrix:**

| Folder | Read Access | Write Access | CDN Enabled |
|--------|-------------|--------------|-------------|
| `uploads/temp/` | None (service account only) | Django + upload session | No |
| `uploads/quarantine/` | Admin service account | Cloud Function only | No |
| `uploads/approved/` | Authenticated users (via signed cookie) OR public (if moved) | Cloud Function (updates metadata) | Optional (preview) |
| `public/` | All users | Cloud Function (publish), Django (retract) | Yes |
| `thumbnails/` | Same as parent image (public or private) | Cloud Function (create/update) | Yes |
| `archive/` | Admin / backup role | Archive pipeline only | No |

## 4. Data Flow Description

1. **User selects image** → Client validates size/type locally.
2. **Client requests upload session** → `POST /api/upload/session/` (Django REST, auth required). Django validates user quota (e.g., max 10 uploads/day, max 500 MB total storage) and returns signed URL or resumable session token.
3. **Client uploads bytes** → Direct PUT/POST to GCS (`https://storage.googleapis.com/upload/storage/v1/b/...`). Client includes `Content-Type` header and optional custom metadata.
4. **GCS triggers event** → Pub/Sub pushes `OBJECT_FINALIZE` event.
5. **Cloud Function processes** → Generates thumbnails, scans malware, updates GCS metadata.
6. **Cloud Function calls Django webhook** → `POST /api/webhooks/gcs/` with event JSON. Django creates `Image` record and updates CMS post associations.
7. **Django updates access policy** → If image is approved for public display, Django instructs GCS (via service account) to update ACL / move object; or Django updates its own database and relies on CDN rules based on folder path.
8. **User sees image** → Client fetches via CDN URL (`https://cdn.rhixecompany.example.com/public/post_999/abc.webp`). CDN serves from cache or pulls from GCS origin.

## 5. Error Handling & Retry Logic

| Failure Point | Retry Strategy | Backoff | Max Retries | Fallback |
|--------------|----------------|---------|-------------|----------|
| Signed URL generation (GCS API error) | Exponential backoff (1s, 2s, 4s) | None | 3 | Return 503 to client; log error; alert admin if persistent |
| Client upload (network timeout) | Client retries PUT with same session token (resumable allows partial uploads) | Linear (5s) | 5 per session | Client shows "upload failed"; allows new session request |
| GCS event delivery (Pub/Sub push to webhook) | Pub/Sub automatic retry (exponential up to 600s) | Built-in | 5 attempts (Pub/Sub config) | Send to dead-letter topic; alert via Cloud Monitoring |
| Cloud Function timeout / failure | Cloud Functions retries (max 7 attempts over ~10 min); use dead-letter queue for unprocessed events | Built-in | Configurable (default 7) | Dead-letter Pub/Sub topic for manual replay; Django webhook logs failure |
| Thumbnail generation (Pillow error / corrupt file) | Log error with full object path; do NOT retry (corrupt file won't fix itself). Move object to `uploads/quarantine/corrupt/` for admin review. | N/A | 0 | Admin notification; object quarantined |
| Malware scan timeout (VirusTotal rate limit) | Queue event in Pub/Sub with delay (e.g., retry after 1 hour); limit concurrent scan requests to 10/second. | Linear (1h) | 3 | Quarantine object; notify admin; do not publish |
| Django webhook unreachable (Cloud Function → Django) | Cloud Function retries (same as above); Django logs all webhook attempts in `GCSEvent` model for audit. | N/A | 3 (function retries) | Event stays in Pub/Sub; admin can replay via Pub/Sub replay feature |

**Client Retry Example (resumable upload — Python `requests`):**

```python
import requests

session = requests.Session()
session.mount("https://", requests.adapters.HTTPAdapter(max_retries=3))

# Upload with resumable session token; on 408/503, resume from last byte
response = session.put(
    resumable_url,
    headers={"Content-Range": f"bytes 0-{file_size-1}/{file_size}"},
    data=file_chunk,
    timeout=60,
)
```

**Server-Side Retry (Django + Celery, if using webhook):**

```python
@app.task(bind=True, max_retries=3, default_retry_delay=30)
def process_gcs_event(self, event_data):
    try:
        # Process event
    except DatabaseError as exc:
        raise self.retry(exc=exc, countdown=30)
```

## 6. Cost / Performance Trade-offs

| Approach | Cost Impact | Performance Impact | Recommendation |
|----------|-------------|-------------------|---------------|
| Direct upload (signed URL) | Low (no server bandwidth) | High (fast upload, low latency) | Primary mechanism |
| Resumable upload | Low (same as direct; session token overhead minimal) | Slightly lower (extra round-trip for session creation; resume overhead) | Large files (>20 MB) |
| Server-mediated (Django handles bytes) | High (egress + compute) | Low (server bottleneck, single-threaded) | Only for small files with strict validation requirements |
| Standard storage class | Baseline ($0.020/GB/month) | Fastest retrieval | Active images (<30 days) |
| Nearline | ~50% lower ($0.010/GB/month) | Retrieval latency slightly higher; early retrieval fee ($0.01/GB) | Images accessed rarely (>30 days) |
| Coldline | ~75% lower ($0.004/GB/month) | Retrieval fee ($0.05/GB); latency higher | Archive (>90 days) |
| CDN (Cloud CDN) | Cache hit: low cost; miss: standard GCS retrieval cost + egress | Very fast (edge caching, TLS termination at edge) | Enable for all `public/` images |
| Cloud Function (post-upload) | $0.40 per million invocations + compute time (~128MB, 60s = ~$0.000002) | Async (does not block upload) | Required for thumbnails + metadata |
| CMEK (Cloud KMS) | Extra cost ($0.06/key version/month + $3.00/key/month active) + KMS API calls | Minimal overhead (encryption/decryption at GCS layer) | Only if compliance requires |
| VirusTotal API | Free tier: 4 requests/min; paid: ~$0.10/1000 scans (varies) | Async delay (scan time 30-120s) | Use free tier for low volume; queue and rate-limit for high volume |

**Cost Optimization Strategy:**
- Set lifecycle rules aggressively (Nearline after 30d, Coldline after 90d).
- Delete `temp/` objects quickly (1 day) — resumable session artifacts are small but accumulate.
- Use WebP for thumbnails (~25-35% smaller than JPEG); reduces storage and CDN egress costs.
- Monitor `gsutil du -sh` monthly; set budget alerts at 75% of projected spend.

**Performance Optimization:**
- Enable GCS `Cache-Control` headers; use CDN for `public/` images.
- For responsive images, generate thumbnails at fixed widths (300px, 1200px, 2400px) rather than on-demand resizing (avoids compute overhead per request).
- Pre-warm CDN for high-traffic releases (e.g., new blog post with many images) by fetching each public URL once via `curl` after publish.

## 7. Key Implementation Recommendations

### 7.1 Django Integration (Workspace Context)

Given the `rhixecompany` Django CMS workspace:

- Create a new Django app (`media_upload`) with models `Image`, `Thumbnail`, `UploadSession`.
- Configure settings (`rhixecompany/settings.py` or override `rhixecompany/setting.py`) with GCS bucket name, region, and service account project ID.
- Never store GCS keys in `.env` or `settings.py` directly (per `.hermes.md` anti-pattern). Use `django-environ` with environment variables that load from GCP metadata server in production, or `gcloud` auth locally.
- Add upload endpoint to Django REST framework (`rest_framework` is common in Django CMS stacks):
  - `POST /api/upload/session/` (auth required)
  - `GET /api/images/` (list approved images)
  - `GET /api/images/{uuid}/` (metadata + URLs)

### 7.2 Security Checklist

- [ ] Signed URL lifetime <= 15 minutes; URL includes single-use token if needed.
- [ ] Client validates file type (magic bytes) and size before upload.
- [ ] GCS bucket has UBACL enabled; ACL updates limited; IAM conditions used.
- [ ] Encryption at rest: AES-256 (default) or CMEK (if required); TLS 1.3 enforced.
- [ ] Malware scan triggered for all uploads; quarantine folder isolated; admin alerted.
- [ ] `.env` and `settings.py` contain no GCS private keys; use service account JSON only in CI/deploy pipeline, never in repo.
- [ ] CORS configured only for CMS origin + CDN domain; `PUT` and `POST` allowed only with correct `Content-Type`.
- [ ] Lifecycle rules delete temp artifacts; archive folder cleaned per retention policy.

### 7.3 Monitoring & Observability

- **Cloud Monitoring:** Alert on:
  - GCS bucket storage growth rate (>10% weekly increase)
  - Upload failure rate (>1% of upload attempts)
  - Cloud Function error rate (>0.1%)
  - CDN cache miss rate (>20% for public images — indicates new content or misconfigured headers)
- **Django Logging:** Log every upload session creation, GCS webhook event, approval/rejection action in `Image` model audit log.
- **Cost Tracking:** Label GCS bucket and Cloud Function resources with `project: rhixecompany`, `service: media-upload`; use GCP Cost Explorer monthly.

### 7.4 Testing Strategy

- **Unit tests (Django):** Mock GCS client; test session generation, validation logic, webhook handling.
- **Integration tests (local / CI):** Use `fake-gcs-server` or `gcs-emulator` (if available) or mock signed URL generation; test Django endpoint with `pytest` + `rest_framework.test.APIClient`.
- **Load tests:** Use `locust` or `k6` to simulate 100 concurrent uploads (direct + resumable); verify GCS upload throughput and Django endpoint response time stays < 200ms for session creation.
- **Security tests:** Try uploading `.jpg` that is actually `.exe` (rename); attempt path traversal (`../../../etc/passwd` in filename); verify rejection.

## 8. Component Diagram (Simplified)

```
┌──────────────────────┐
│  User Browser / App │
└─────────┬────────────┘
          ▼
┌──────────────────────────────┐
│ Django API (rhixecompany)   │  ← Session creation, auth, validation
│  POST /upload/session/     │
│  GET /images/              │
└─────────┬────────────────────┘
          │ Signed URL / Token
          ▼
┌──────────────────────────────┐
│  GCS Bucket (Standard)     │  ← Direct upload
│  uploads/temp/             │
│  uploads/approved/         │
└─────────┬────────────────────┘
          │ Pub/Sub Event (OBJECT_FINALIZE)
          ▼
┌──────────────────────────────┐
│ Cloud Function / Cloud Run │  ← Thumbnail, malware scan, metadata
│  Process Upload Event       │
└─────────┬────────────────────┘
          │ Webhook / DB Update
          ▼
┌──────────────────────────────┐
│ Django CMS (Database)      │  ← Image model, approval status, post links
│  Image, Thumbnail, EventLog │
└─────────┬────────────────────┘
          │ CDN / Public Access
          ▼
┌──────────────────────────────┐
│  GCS + Cloud CDN (public/) │  ← Thumbnail + approved original delivery
│  Cache: max-age=1yr         │
└──────────────────────────────┘
```

## 9. References & Related Workspace Documents

- Workspace identity: `.hermes.md` (agent identity rules, anti-patterns: no secrets in `.env`, identity sync required before changes)
- Django sub-app identity: `base/AGENTS.md`
- Existing spec pattern: `SPEC.md` (repo-level spec format)
- Project rules: `.cursorrules`, `MASTER_RULES.md`, `PROJECT_RULES.md`
- Verification checklist (identity sync + ruff + Django tests): `AGENTS.md`
- GCS documentation: https://cloud.google.com/storage/docs (referenced for lifecycle rules, signed URLs, CORS, Pub/Sub notifications)

---
*Document version: 1.0.0 — Design stage; not yet implemented. Implementation requires identity sync verification (`.hermes.md` ↔ `AGENTS.md` ↔ `.cursorrules`), ruff lint pass, and Django test pass (per workspace verification checklist) before any production deployment.*
