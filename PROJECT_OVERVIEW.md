# Antigravity Study Platform — Comprehensive Architecture & Technical Guide

Welcome to the **Antigravity Study Platform (SST Study Site)**. This platform is a secure, high-performance, private digital portal designed specifically for students at **Scaler School of Technology (SST)**. It enables students to browse, read, search, and bookmark lecture notes across their computer science and machine learning curriculum.

---

## 1. Executive Summary & Vision

The platform is designed around four core engineering principles:

1. **Extreme Performance for Content Delivery**:
   Course notes are pre-compiled into static, schema-validated JSON files served via CDN edges. Note reads require **zero database round-trips**.
2. **Zero-Trust Security & Domain Isolation**:
   Access to notes is strictly gated to authenticated SST students with active `@sst.scaler.com` Google Workspace accounts. Asymmetric RS256 JSON Web Tokens (JWTs) protect all static data assets before CDN cache lookups.
3. **Resilient Local & Production Lifecycle**:
   A multi-layered fallback strategy allows local offline development (in-memory MongoDB and Redis mock layers, client-side dev bypass) while maintaining strict fail-closed security in production on Vercel.
4. **Rich Reader Experience**:
   A 3-panel desktop reader layout, keyboard-driven command palette (`Ctrl+K`), KaTeX mathematical equation rendering, table of contents with scrollspy, theme customizability (`OLED Slate`, `Minimalist Midnight`, `Clean Light`), and optimistic bookmark synchronization.

---

## 2. System Architecture & Component Diagram

```
                                      +---------------------------------------------+
                                      |          Scaler Student (Browser)           |
                                      |  React 19 + TypeScript + Vite + Custom CSS  |
                                      +----------------------+----------------------+
                                                             |
                                         +-------------------+-------------------+
                                         |                                       |
                       (API Requests: /api/*)                (Note Data: /data/*)
                                         |                                       |
                                         v                                       v
                     +-----------------------+               +-----------------------+
                     |  FastAPI Backend API  |               | Vercel Edge Middleware|
                     |  (Python 3.10+, Uvicorn)              |    (middleware.ts)    |
                     +-----------+-----------+               +-----------+-----------+
                                 |                                       |
        +------------------------+------------------------+              |  Verifies RS256
        |                        |                        |              |  Access JWT
        v                        v                        v              v
+---------------+        +---------------+        +---------------+ +------------------+
| Google OAuth2 |        | MongoDB Atlas |        | Upstash Redis | | Static Note CDN  |
|  GIS / JWKS   |        |  (Atlas M0+)  |        | (Sliding Rate)| |  (/data/*.json)  |
+---------------+        +---------------+        +---------------+ +------------------+
```

---

## 3. Directory & File Structure

```text
sst-study-platform/
│
├── .env                              # Root environment variables (Atlas, Upstash, RS256 keys)
├── package.json                      # Workspace orchestration & npm scripts
├── vercel.json                       # Vercel deployment routes, build commands & rewrites
├── middleware.ts                     # Vercel Edge routing middleware protecting /data/**
│
├── api/                              # Backend FastAPI Application
│   ├── index.py                      # FastAPI routes, lifecycle & exception handlers
│   ├── auth.py                       # Token lifecycle, Google verification, CSRF & cookies
│   ├── config.py                     # Environment variables & RSA PEM loader
│   ├── database.py                   # MongoDB Atlas connection & in-memory dev fallback
│   ├── models.py                     # Pydantic schemas for request & response models
│   ├── rate_limiter.py               # Upstash Redis & in-memory sliding-window limiter
│   └── requirements.txt              # Python production dependencies
│
├── content/
│   └── fixtures/                     # Authoritative source notes (JSON Schema v1)
│       ├── cml-lecture-01-linear-regression.json
│       ├── cn-lecture-01-introduction.json
│       └── cn-lecture-02-packet-switching.json
│
├── data/                             # Compiled protected assets (built by tooling)
│   ├── notes-index.json              # Search catalogue & navigation manifest
│   └── notes/                        # Individual note content payloads
│
├── tooling/
│   ├── build_notes.py                # Schema validator & static catalogue builder
│   ├── generate_keys.py              # Generates RS256 RSA-2048 private/public keys
│   └── dev.js                        # Unified runner launching API & Web concurrently
│
├── tests/
│   └── test_api_auth_bookmarks.py    # Pytest acceptance test suite (12 test cases)
│
└── web/                              # React 19 Frontend Web Application
    ├── index.html                    # HTML5 shell loading fonts & Google GIS script
    ├── vite.config.ts                # Vite dev server with proxy to backend
    ├── src/
    │   ├── main.tsx                  # React DOM root mounting Providers & App
    │   ├── App.tsx                   # Main 3-panel layout & view state coordinator
    │   ├── index.css                 # Global CSS design tokens, themes & typography
    │   ├── components/
    │   │   ├── Navbar.tsx            # Header bar with search, theme, bookmarks, & auth
    │   │   ├── Sidebar.tsx           # Course catalogue list & subject tabs (ALL, CML, CN)
    │   │   ├── TableOfContents.tsx   # Active heading scrollspy sidebar
    │   │   ├── MarkdownViewer.tsx    # Safe Markdown, KaTeX & code block renderer
    │   │   ├── SearchModal.tsx       # Spotlight command palette (Ctrl+K)
    │   │   └── GoogleSignInButton.tsx# Google Identity Services integration
    │   ├── context/
    │   │   ├── AuthContext.tsx       # Session state, login, refresh, logout, dev bypass
    │   │   └── BookmarkContext.tsx   # Optimistic bookmarks & toast notifications
    │   ├── services/
    │   │   ├── apiClient.ts          # Fetch wrapper with CSRF injection
    │   │   └── notesService.ts       # Note catalogue & note detail fetcher
    │   └── types/
    │       └── note.ts               # TypeScript interfaces (Note, User, Theme, etc.)
    └── public/
        └── data/                     # Local copy of static note assets for dev preview
```

---

## 4. Deep-Dive: Core Subsystems

### 4.1. Authentication & Security Engine (`api/auth.py` & `middleware.ts`)

#### 1. Identity Verification
- Students sign in using **Google Identity Services (GIS)**.
- The backend verifies the Google ID token using Google's public certificates.
- **Hosted Domain Restriction**: Enforces `hd == "sst.scaler.com"` and checks that the verified email strictly ends in `@sst.scaler.com`. Non-SST Google accounts are rejected with `403 Forbidden`.
- **One-time Nonces**: `/api/auth/nonce` generates a single-use cryptographically random nonce stored in memory (5-minute TTL) that must be echoed back in the ID token to prevent replay attacks.
- **Quick Dev Login Bypass**: In development environments (`ENVIRONMENT != "production"` and `ALLOW_DEV_MOCK_LOGIN == true`), sending an ID token prefixed with `mock:student@sst.scaler.com` simulates a valid student login without interacting with Google servers.

#### 2. Asymmetric RS256 Access Tokens
- The server generates an asymmetric **RSA-2048 (RS256)** signed JWT.
- **Expiry**: 15 minutes.
- **Header**: Contains a dynamic key ID (`kid`), derived from the SHA-256 fingerprint of the public key.
- **Payload Claims**: `sub` (unique student ID), `email`, `role: "sst_student"`, `iss`, `aud`, `iat`, `exp`, `jti`.
- Signed exclusively using the server's RSA private key (`JWT_PRIVATE_KEY_B64`).
- Verified by **Edge Middleware** using only the lightweight RSA public key (`JWT_PUBLIC_KEY_B64`).

#### 3. Rotating Refresh Tokens
- **Expiry**: 7 days.
- Stored as a raw 32-byte cryptographically secure random hex string inside a secure, HttpOnly cookie.
- Stored on the server strictly as a **SHA-256 hash** (`token_hash`) inside MongoDB Atlas `refresh_tokens` collection (or `InMemoryStore` in development).
- Upon calling `/api/auth/refresh`, the old refresh token is atomically revoked and replaced with a newly generated pair (**refresh token rotation**).

#### 4. Cookie Architecture
All cookies are set with strict security attributes:
- `HttpOnly`: Inaccessible to client JavaScript (mitigates XSS token extraction).
- `SameSite=Strict`: Cookies are omitted on cross-site requests (mitigates CSRF).
- `Path=/`: Valid for all routes.
- `Secure`: Dynamically set to `true` in production (HTTPS) and `false` in local development.

#### 5. CSRF Protection
- For all state-changing endpoints (`POST`, `PUT`, `DELETE`), the client must echo the opaque `x-csrf-token` header.
- The server stores CSRF tokens mapped to user sessions with expiry timestamps.
- Origin validation enforces that incoming requests originate from approved frontend hosts (`clean_app` + local development ports `5173`, `5174`, `3000`, `8000`).

---

### 4.2. Database & Storage Architecture (`api/database.py`)

The platform supports two persistence strategies:

1. **MongoDB Atlas (Production & Connected Dev)**:
   - **`users` Collection**:
     - `google_sub_id` (Unique Index): Google Subject ID.
     - `email`: SST email address.
     - `display_name`: Student full name.
     - `status`: Active or suspended.
   - **`refresh_tokens` Collection**:
     - `token_hash` (Unique Index): SHA-256 hash of raw refresh token.
     - `user_id`: MongoDB ObjectId string.
     - `expires_at`: ISO timestamp (indexed with TTL for automatic document eviction).
   - **`bookmarks` Collection**:
     - Compound unique index on `(user_id, note_id)`: Guarantees a student cannot bookmark the same note multiple times.

2. **In-Memory Store (`InMemoryStore`)**:
   - A thread-safe, mock database storing users, refresh sessions, and bookmarks in Python dictionaries.
   - **Automatic Dev Fallback**: If `settings.MONGODB_URI` is unset or if MongoDB Atlas experiences a network outage during local development, the system automatically logs a warning and falls back to `in_memory_store`.

---

### 4.3. Rate Limiting Engine (`api/rate_limiter.py`)

- **Sliding-Window Algorithm**: Tracks timestamps within rolling windows (e.g., 15 attempts / 60 seconds on login).
- **Upstash Redis Pipeline**: Uses Upstash Redis REST API (`ZREMRANGEBYSCORE`, `ZCARD`, `ZADD`, `EXPIRE`) to maintain distributed state without local Redis dependencies.
- **IP Extraction**: Safely extracts the real end-user IP from Vercel's `x-vercel-forwarded-for` header to prevent IP spoofing, falling back to raw TCP socket peer addresses locally.
- **Fail-Safe Development Mode**: In local development, if Upstash credentials are empty or the cluster is temporarily unreachable, the system automatically falls back to an in-memory sliding-window limiter instead of halting with `503`.
- Mock logins during local development are exempted from aggressive rate limits.

---

### 4.4. Content Pipeline & Static Note Builder (`tooling/build_notes.py`)

Course notes are managed as structured JSON documents following **Schema Version 1**:

#### Required Note Schema
```json
{
  "schema_version": 1,
  "note_id": "cn-lecture-01-introduction",
  "term": "Term 2",
  "subject_code": "CN",
  "topic_title": "Introduction to Computer Networks & Network Core",
  "tags": ["computer-networks", "osi-model", "tcp-ip", "packet-switching"],
  "learning_objectives": [
    "Understand the difference between network edge and network core",
    "Analyze packet switching vs circuit switching performance"
  ],
  "summary": "Foundational concepts in computer networking...",
  "key_takeaways": [
    "Packets share resources dynamically via statistical multiplexing"
  ],
  "sections": [
    {
      "section_id": "network-edge-core",
      "heading": "1. Network Edge vs. Network Core",
      "body": "Detailed Markdown content...",
      "citations": ["Kurose & Ross Chapter 1"]
    }
  ],
  "last_updated": "2026-10-01T12:00:00Z",
  "approval_status": "approved"
}
```

#### Pipeline Steps:
1. Validates all required fields and schema constraints (e.g., regex `^[a-z0-9-]+$`, `approval_status == 'approved'`).
2. Copies validated notes into `data/notes/<note_id>.json` and `web/public/data/notes/<note_id>.json`.
3. Compiles a high-speed catalogue index (`data/notes-index.json`) containing metadata for all notes, pre-sorted by subject and topic.

---

### 4.5. Frontend Architecture & Design System (`web/`)

#### 1. Layout & Usability
- **3-Panel Desktop Reader**:
  1. *Left Panel (Sidebar)*: Course Catalogue list, subject filter tabs (`ALL`, `CML`, `CN`), note count badge, search filter.
  2. *Center Panel (Reader)*: Note title, subject & term badges, approval tag, learning objectives callout, key takeaways callout, body sections, citations, and bookmark toggle button.
  3. *Right Panel (TOC)*: "On this page" outline with dynamic active section highlighting via `IntersectionObserver`.
- **Spotlight Search (`Ctrl+K` / `Cmd+K`)**:
  - Global keyboard listener launches a floating modal search overlay.
  - Searches note titles, summaries, tags, subjects, and terms in real time.
  - Supports keyboard navigation (`ArrowUp`, `ArrowDown`, `Enter`, `Escape`).

#### 2. Visual Design System (`web/src/index.css`)
- Custom CSS variable tokens without Tailwind overhead.
- **Three Curated Themes**:
  - `oled-slate`: Deep pure blacks (`#000000`), slate cards (`#0b0f19`), ice-blue accents (`#38bdf8`).
  - `minimalist-midnight`: Deep navy midnight (`#090d16`), purple-indigo accents (`#818cf8`).
  - `clean-light`: Crisp paper white (`#f8fafc`), clean borders (`#e2e8f0`), high-contrast text (`#0f172a`).

#### 3. State Management & Optimistic UI
- **`AuthContext`**: Manages user authentication lifecycle, silent cookie refresh on load, CSRF token storage, dev mock bypass, and account deletion.
- **`BookmarkContext`**:
  - Loads saved bookmarks on mount.
  - **Optimistic Updates**: Toggling a bookmark immediately updates the UI; if the network request fails, the state automatically rolls back and displays an error toast.

#### 4. Markdown Rendering Security (`MarkdownViewer.tsx`)
- Configured using `react-markdown` with strict plugins:
  - `remark-gfm`: GitHub flavored tables, strikethrough, task lists.
  - `remark-math` + `rehype-katex`: High-performance LaTeX math rendering in untrusted mode (`trust: false`).
  - Raw HTML parsing is **disabled** (`skipHtml={true}`) to eliminate stored XSS vectors.
  - External links automatically receive `target="_blank"` and `rel="noopener noreferrer"`.

---

## 5. API Reference Summary

| Method | Endpoint | Description | Auth Required | CSRF Checked |
|---|---|---|---|---|
| `GET` | `/api/health` | Health check & service name | No | No |
| `GET` | `/api/auth/nonce` | Generate single-use login nonce | No | No |
| `POST` | `/api/auth/google` | Google ID Token / Dev Mock login | No | No (Origin checked) |
| `POST` | `/api/auth/refresh` | Rotate 7-day refresh token | Cookie | No (HttpOnly cookie) |
| `POST` | `/api/auth/logout` | Revoke session & clear cookies | Cookie | **Yes** |
| `GET` | `/api/users/me` | Current student profile & status | Cookie / Bearer | No |
| `DELETE` | `/api/users/me` | Delete profile and all bookmarks | Cookie / Bearer | **Yes** |
| `GET` | `/api/bookmarks` | List all saved bookmark note IDs | Cookie / Bearer | No |
| `POST` | `/api/bookmarks` | Add note to personal bookmarks | Cookie / Bearer | **Yes** |
| `DELETE` | `/api/bookmarks/{note_id}` | Remove note from bookmarks | Cookie / Bearer | **Yes** |
| `GET` | `/data/notes-index.json` | Protected catalogue index | Cookie / Bearer | No |
| `GET` | `/data/notes/{id}.json` | Protected full note JSON | Cookie / Bearer | No |

---

## 6. How to Run & Develop Locally

### Prerequisites
- **Node.js**: >= 18.0
- **Python**: >= 3.10

### 1. Unified One-Command Start
Run the combined development server from the repository root:
```bash
npm run dev
```
This automatically:
1. Validates and compiles course notes into both `data/` and `web/public/data/`.
2. Starts the **FastAPI backend** on `http://127.0.0.1:8000` with auto-reload.
3. Starts the **Vite frontend** on `http://localhost:5173`.

### 2. Manual Commands
- **Backend Only**:
  ```bash
  npm run dev:api
  # or: python -m uvicorn api.index:app --reload --port 8000
  ```
- **Frontend Only**:
  ```bash
  npm run dev:web
  # or: cd web && npm run dev
  ```
- **Compile Notes Catalogue**:
  ```bash
  python tooling/build_notes.py
  ```
- **Run Acceptance Tests**:
  ```bash
  pytest
  ```
- **Production Build**:
  ```bash
  npm run build
  ```

---

## 7. Testing & Quality Assurance

The platform is covered by an automated pytest acceptance suite in `tests/test_api_auth_bookmarks.py`:
- `test_health_check`: Validates service availability.
- `test_nonce_endpoint_returns_nonce`: Checks random 16+ byte nonce generation.
- `test_google_login_dev_mode`: Tests mock login with `student@sst.scaler.com`.
- `test_google_login_disallowed_domain`: Rejects non-SST emails (`@gmail.com`) with 403.
- `test_mock_login_blocked_in_production`: Verifies mock tokens are strictly blocked (401) in production.
- `test_authenticated_user_profile_and_bookmarks`: Tests the end-to-end user lifecycle (login -> fetch profile -> add bookmark -> list bookmarks -> remove bookmark).
- `test_refresh_token_rotation`: Tests that refresh tokens are rotated and old tokens invalidated.
- `test_logout_flow`: Ensures session invalidation and cookie clearing.
- `test_csrf_token_validation`: Verifies state-changing requests reject invalid CSRF tokens.
- `test_bookmark_invalid_note_id`: Ensures non-existent note IDs cannot be bookmarked (400 Bad Request).
- `test_delete_account`: Tests full student account deletion and data removal.
- `test_rate_limiting`: Verifies rate limit enforcement on sensitive endpoints.

---

## 8. Summary of Recent Enhancements

- **Quick Dev Login Bypass Enabled**: Fixed local origin mismatches for `http://127.0.0.1:5173` and port increments (`:5174`), decoupled dev bypass from Google Client ID presence, and added client-side dev fallback.
- **Resilient Fallback**: In local development, the backend automatically falls back to in-memory storage if MongoDB Atlas is unreachable or experiencing replica set timeouts.
- **Enhanced Visual Feedback**: Added clear error messaging below login buttons and wrapped dev login triggers with error handling.
- **Streamlined Tooling**: Added `tooling/dev.js` and an updated `npm run dev` script to run both FastAPI and Vite with a single command.
