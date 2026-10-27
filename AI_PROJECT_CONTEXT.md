# Scaler School of Technology (SST) Study Platform
## Comprehensive Technical Context, Architecture, and Engineering Specification for AI Models

> **Instruction for AI Models / LLM Agents:**
> You are reading the authoritative, comprehensive technical specification and codebase guide for the **Antigravity Study Platform (SST Study Site)**. This document contains complete architectural, algorithmic, behavioral, and structural context across the entire repository. Use this document to understand the codebase without needing to read every file individually. Adhere strictly to the design patterns, security invariants, dual-persistence fallback behaviors, and coding standards documented herein.

---

## 1. Project Mission & Identity

The **Antigravity Study Platform** (repository: `its-shadow7/SST-Study-Platform`) is a production-grade, secure, high-performance study and reference portal engineered specifically for computer science and machine learning undergraduate students at **Scaler School of Technology (SST)**.

### Core Philosophy & Architectural Pillars:
1. **Sub-millisecond Static Content Delivery**:
   Curriculum notes are authored in a validated **JSON Schema v1**, pre-compiled by backend tooling, and served directly as static JSON files via CDN edges. Reading lecture notes requires **zero database round-trips**.
2. **Zero-Trust Multi-Tiered Security**:
   Curriculum access is strictly restricted to verified `@sst.scaler.com` Google accounts. Access to static note assets (`/data/**`) is enforced directly at the edge via **Vercel Edge Middleware** using asymmetric **RS256 JSON Web Tokens (JWT)**.
3. **Dual-Persistence & Zero-Dependency Development**:
   The entire backend incorporates seamless dual-mode persistence:
   - **Production / Connected**: MongoDB Atlas + Upstash Redis REST API.
   - **Local / Disconnected**: Thread-safe in-memory mock store (`InMemoryStore`) + sliding-window rate limiter fallback. The platform runs locally out-of-the-box without requiring live cloud database or Redis credentials.
4. **Rich, Distraction-Free 3-Island Reader Experience**:
   A modular desktop layout comprising:
   - **Left Island**: Curriculum catalogue, term switchers, subject filter tabs, and fast search.
   - **Center Island**: Compact, high-density lecture reader with mathematical equation rendering ($\LaTeX$ via KaTeX), code blocks with syntax highlighting, learning objectives, key takeaways, embedded interactive quizzes, and threaded section-anchored discussions.
   - **Right Island**: Dynamic Table of Contents (scrollspy using `IntersectionObserver`) and personal Student Scratchpad.
5. **Academic Integrity & Peer Collaboration**:
   Integrated discussions with Markdown and KaTeX, net-score voting, user reputation badges, role-based moderation queue (`student`, `moderator`, `admin`), velocity-based auto-quarantine for reported content, and private student scratchpads with debounced auto-save.

---

## 2. Technology Stack & Runtime Specifications

| Layer | Technologies & Libraries | Key Versions & Details |
|---|---|---|
| **Frontend Framework** | React, TypeScript, Vite | React 19 (`^19.0.0`), TypeScript (`^5.7.3`), Vite (`^6.1.0`) |
| **Routing & Navigation** | React Router DOM | `react-router-dom` (`^7.18.4`) |
| **Styling & Design System** | Vanilla CSS Tokens, Lucide Icons, Tailwind (build-time) | Custom CSS properties in `index.css`, `lucide-react` (`^1.16.0`), PostCSS |
| **Math & Markdown Rendering** | React-Markdown, KaTeX, Rehype, Remark | `react-markdown` (`^10.0.0`), `katex` (`^0.16.21`), `remark-math` (`^6.0.0`), `rehype-katex` (`^7.0.1`), `remark-gfm` (`^4.0.0`), `rehype-sanitize` (`^6.0.0`) |
| **Syntax Highlighting** | React Syntax Highlighter | `react-syntax-highlighter` (`^16.1.2`) with Prism engine |
| **UI Notifications & Feedback**| Sonner | `sonner` (`^2.0.8`) toast engine |
| **Backend Framework** | Python, FastAPI, Uvicorn, Pydantic | Python 3.10+ (tested on 3.12), FastAPI (`^0.115.0`), Pydantic v2 |
| **Cryptography & Tokens** | PyCryptodome, PyJWT, Jose (Node/Edge) | RS256 RSA-2048 keypairs, dynamic SHA-256 `kid`, `jose` (`^5.9.6`) on Vercel Edge |
| **Database (Primary)** | MongoDB Atlas | `pymongo` (`^4.9.0`), Atlas M0/M10 clusters |
| **Cache & Rate Limiting** | Upstash Redis REST API | `httpx` (`^0.27.0`) calling Upstash REST endpoints |
| **AI Content Moderation** | OpenAI Moderation API | Optional automatic toxicity/harassment flagging |
| **Testing Suites** | Pytest (Backend), Vitest (Frontend) | Pytest 9.x (`pytest-anyio`), Vitest 5.x (`@testing-library/react`, JSDOM) |
| **Hosting & Edge Infrastructure**| Vercel | Vercel Serverless Functions (`api/index.py`), Vercel Edge Middleware (`middleware.ts`) |

---

## 3. High-Level System Architecture

```text
                                       +-----------------------------------------------+
                                       |            Scaler Student Browser             |
                                       |       React 19 + TypeScript + Vite SPA        |
                                       +-----------------------+-----------------------+
                                                               |
                                     +-------------------------+-------------------------+
                                     |                                                   |
                   API Requests (/api/*)                                  Static Protected Notes (/data/*)
                                     |                                                   |
                                     v                                                   v
                     +-------------------------------+                   +-------------------------------+
                     |      FastAPI Backend API      |                   |    Vercel Edge Middleware     |
                     |     (Vercel Serverless /      |                   |        (middleware.ts)        |
                     |       Local Uvicorn :8000)    |                   +---------------+---------------+
                     +---------------+---------------+                                   |
                                     |                                                   | Verifies RS256
                +--------------------+--------------------+                              | Access Token JWT
                |                    |                    |                              | directly at edge
                v                    v                    v                              v
        +---------------+    +---------------+    +---------------+              +---------------+
        | Google OAuth2 |    | MongoDB Atlas |    | Upstash Redis |              | Static Note   |
        |  GIS / JWKS   |    | (or In-Memory)|    | (or In-Memory)|              | Content CDN   |
        +---------------+    +---------------+    +---------------+              +---------------+
```

---

## 4. Complete Repository Directory Tree & File Inventory

```text
SST-Study-Platform/
├── .env                              # Root environment variables (Atlas URI, Upstash, RS256 keys)
├── .env.example                      # Template documentation of required environment variables
├── package.json                      # Root workspace scripts (build, dev, test)
├── vercel.json                       # Vercel deployment routes, Python runtime setup & rewrites
├── middleware.ts                     # Vercel Edge Middleware protecting /data/** with RS256 JWT checks
├── pytest.ini                        # Pytest configuration
├── tsconfig.json                     # Root TypeScript configuration
│
├── api/                              # Backend FastAPI Application
│   ├── __init__.py
│   ├── auth.py                       # Identity, GIS token verification, RS256 JWT, CSRF, batch regex
│   ├── comments.py                   # Threaded comments, voting, reports, and reaction endpoints
│   ├── config.py                     # Pydantic Settings class & RSA base64 PEM key loaders
│   ├── database.py                   # MongoDB Atlas client & thread-safe InMemoryStore mock layer
│   ├── dependencies.py               # FastAPI Depends: get_current_student, get_db_or_fail
│   ├── index.py                      # FastAPI entry point, lifecycle, error handlers & core routes
│   ├── models.py                     # Pydantic request/response schemas (Auth, User, Bookmarks)
│   ├── moderation.py                 # Moderation queue, resolution actions, and audit logging
│   ├── notifications.py              # In-app user notification feeds and mark-as-read handlers
│   ├── quizzes.py                    # Quiz attempt persistence, score tracking, and user stats
│   ├── rate_limiter.py               # Upstash Redis REST & InMemoryRateLimiter sliding-window
│   ├── requirements.txt              # Production Python dependencies
│   └── scratchpad.py                 # Student private scratchpad endpoints & summary metadata
│
├── content/                          # Authoritative Curriculum Source Notes (Schema v1)
│   └── fixtures/
│       ├── term-3/
│       │   ├── cml/                  # Term 3 Classical Machine Learning fixtures
│       │   └── cn/                   # Term 3 Computer Networks fixtures
│       └── term-5/
│           ├── cml/                  # Term 5 CML L1-L15 Gold Standard lecture notes
│           └── computer-networks/    # Term 5 CN L1-L13 comprehensive lecture notes
│
├── data/                             # Compiled static artifacts (built via tooling/build_notes.py)
│   ├── notes-index.json              # Fast search catalogue and navigation manifest
│   └── notes/                        # Compiled individual note JSON payloads (<note_id>.json)
│
├── models/                           # Shared Python Data Models (Pydantic schemas)
│   ├── __init__.py
│   ├── comment.py                    # CommentDocument, Vote, Report, AuditLog & Notification models
│   ├── quiz.py                       # QuizAttempt, QuestionAnswer, and UserQuizStats models
│   └── scratchpad.py                 # PrivateNoteDocument, ScratchpadResponse, Summary models
│
├── tests/                            # Automated Backend Pytest Acceptance Test Suite
│   ├── conftest.py                   # Pytest fixtures, test client setup & ephemeral RS256 keys
│   ├── test_api_auth_bookmarks.py    # 22 tests: Auth lifecycle, GIS, RS256, CSRF, rate limits, bookmarks
│   ├── test_comments.py              # 13 tests: Comments CRUD, replies, voting, report velocity quarantine
│   └── test_scratchpad.py            # 4 tests: Scratchpad save, update, debounce safety, summary
│
├── tooling/                          # Build automation and administrative scripts
│   ├── build_notes.py                # Schema v1 validator & notes-index compiler
│   ├── dev.js                        # Unified runner concurrently launching FastAPI (:8000) & Vite (:5173)
│   ├── generate_keys.py              # Script to generate RSA-2048 keypair base64 strings
│   ├── clean_db.py                   # Administrative database cleanup script
│   ├── set_role.py                   # Administrative script to promote a user to moderator or admin
│   └── data_cml_*.py / data_l*.py    # Curriculum generator scripts compiling Gold Standard notes
│
└── web/                              # Frontend React 19 Application
    ├── index.html                    # HTML5 shell loading Google Fonts & Google Identity Services script
    ├── package.json                  # Frontend dependencies and npm scripts
    ├── vite.config.ts                # Vite config with path alias (@ -> /src) & backend proxy
    ├── vitest.config.ts              # Vitest test configuration with JSDOM
    │
    ├── src/
    │   ├── main.tsx                  # React root mounting ThemeProvider, AuthProvider, BookmarkProvider
    │   ├── App.tsx                   # Main router, 3-island layout coordination & search palette
    │   ├── index.css                 # Global CSS design tokens, 4 themes, light mode & typography
    │   │
    │   ├── components/               # Modular UI Components
    │   │   ├── Navbar.tsx            # Header bar with search button, theme picker, notifications, auth
    │   │   ├── Sidebar.tsx           # Course catalogue, subject tabs (ALL, CML, CN), search filter
    │   │   ├── RightSidebar.tsx      # Right Island container switching between TOC and Scratchpad
    │   │   ├── TableOfContents.tsx   # Active heading outline with IntersectionObserver scrollspy
    │   │   ├── Scratchpad.tsx        # Student scratchpad with debounced auto-save & KaTeX preview
    │   │   ├── MarkdownViewer.tsx    # Secure Markdown renderer with KaTeX, syntax highlighting, sanitization
    │   │   ├── QuizSection.tsx       # Interactive quiz UI with score ring, answer review & retry controls
    │   │   ├── QuizMarkdown.tsx      # Specialized parser rendering inline KaTeX in quiz questions/options
    │   │   ├── CommentSection.tsx    # Threaded discussions, upvoting/downvoting, reporting, markdown
    │   │   ├── SearchModal.tsx       # Spotlight command palette modal (Ctrl+K / Cmd+K)
    │   │   ├── NotificationsDropdown.tsx # In-app notification center with unread badges
    │   │   ├── ProfileSetupModal.tsx # First-login setup modal for special accounts
    │   │   ├── StudentProfileModal.tsx # Quick profile peek modal for discussion authors
    │   │   ├── ReportModal.tsx       # Modal to submit comment reports with violation categories
    │   │   ├── RoleBadge.tsx         # Visual role tags (Student, Moderator, Admin)
    │   │   ├── GoogleSignInButton.tsx# Google Identity Services button integration
    │   │   ├── NoteSkeleton.tsx      # Skeleton loader placeholder while fetching notes
    │   │   └── NoteRedirector.tsx    # Universal permalink handler for /read/:noteId
    │   │
    │   ├── context/                  # React Context Providers
    │   │   ├── AuthContext.tsx       # Student session, Google login, refresh loop, dev mock login
    │   │   ├── BookmarkContext.tsx   # Optimistic bookmark toggle, state synchronization & rollback
    │   │   └── ThemeContext.tsx      # 4 curated themes, light mode switch, localStorage persistence
    │   │
    │   ├── pages/                    # Routed Page Views
    │   │   ├── ReaderPage.tsx        # 3-Island layout mounting Sidebar, Note Reader, and RightSidebar
    │   │   ├── TermsPage.tsx         # Curriculum Hub listing accessible terms and subject cards
    │   │   ├── BookmarksPage.tsx     # Student's bookmarked lectures library
    │   │   ├── LoginPage.tsx         # SST Google Sign-In wall and Dev Mode bypass button
    │   │   ├── ProfilePage.tsx       # Public student profile with stats, badges, and recent comments
    │   │   ├── SettingsPage.tsx      # Student settings (display name, username, bio, avatar)
    │   │   └── ModerationPage.tsx    # Moderator/Admin dashboard for review queue & audit logs
    │   │
    │   ├── services/                 # HTTP API Clients
    │   │   ├── apiClient.ts          # Central fetch wrapper with automatic CSRF header injection
    │   │   └── notesService.ts       # Note catalogue index & individual note content fetchers
    │   │
    │   ├── types/                    # TypeScript Type Definitions
    │   │   ├── note.ts               # Note, NoteSection, QuizQuestion, User, Theme types
    │   │   ├── comment.ts            # Comment, VoteAction, ModerationItem types
    │   │   └── scratchpad.ts         # ScratchpadState, PrivateNote types
    │   │
    │   └── test/                     # Frontend Unit and Integration Tests
    │       ├── setup.ts              # Test setup, mocks for window, matchMedia, and ResizeObserver
    │       ├── quizMarkdown.test.tsx # Tests verifying KaTeX math rendering in quiz questions
    │       ├── quizSectionMath.test.tsx # Acceptance tests for quiz math rendering & review screens
    │       └── components.test.tsx   # Tests for SearchModal, Sidebar, Bookmarks, and Comments
    │
    └── public/
        └── data/                     # Local copy of compiled static notes for dev preview
```

---

## 5. Security, Identity & Authentication Subsystem

### 5.1. Google Identity Services (GIS) Flow
1. **Nonce Generation**: The client calls `GET /api/auth/nonce`. The backend generates a cryptographically secure 24-byte random hex string, stored with a 5-minute TTL.
2. **Google Sign-In**: The client initializes Google Identity Services with this nonce.
3. **Backend Verification (`api/auth.py`)**:
   - The client posts the Google ID token to `POST /api/auth/google`.
   - The token signature is verified against Google's public JWKS certificates.
   - The token's `nonce` claim is verified against stored nonces (preventing replay attacks).
   - **Domain Restriction**: Enforces `hd == "sst.scaler.com"` and strictly ensures the verified email ends in `@sst.scaler.com`. Non-SST emails receive `403 Forbidden`.

### 5.2. Batch Identification & Term Access Control Algorithm
SST students are assigned roll-number emails formatted as `firstname.YYprogramroll@sst.scaler.com` (e.g. `surya.25bcs10632@sst.scaler.com`).
The backend regex in `extract_batch_info(email)` evaluates:
```python
match = re.search(r'(?:^|[._])([0-9]{2})[a-zA-Z]+[0-9]*@sst\.scaler\.com$', email, re.IGNORECASE)
```
- **Admission Year**: `batch_year = 2000 + YY` (e.g., `25` -> `2025`).
- **Academic Year Progression**: Scaler academic sessions commence in July (`ref_date.month >= 7`). Current academic calendar year is calculated accordingly.
- **Year of Study**: `year_of_study = academic_cal_year - batch_year + 1` (clamped between 1 and 4).
- **Max Allowed Term**: SST operates on 4 terms per academic year across a 4-year degree (16 terms total).
  $$\text{max\_allowed\_term} = \text{year\_of\_study} \times 4$$
- **Access Rule**: A student in Year 1 can only view **Terms 1–4**; Year 2 can view **Terms 1–8**; Year 3 can view **Terms 1–12**; Year 4 can view **Terms 1–16**.
- **Special Accounts**: Accounts configured in `SPECIAL_EMAILS` (e.g., faculty/admins) bypass roll-number regex and automatically receive full access (`max_allowed_term = 16`).

### 5.3. Development Mock Login Bypass
When `ENVIRONMENT != "production"` and `ALLOW_DEV_MOCK_LOGIN == true`:
- The client can send a token prefixed with `mock:student@sst.scaler.com`.
- The backend skips Google validation and logs in or creates the mock user immediately.
- In the frontend `AuthContext.tsx`, if the backend is unreachable, a client-side mock fallback creates an offline session so UI development is never blocked.

### 5.4. Dual-Token Architecture
```text
[Client] --- (Login) ---> [FastAPI Backend]
                              |
     +------------------------+------------------------+
     |                                                 |
     v                                                 v
[RS256 Access Token]                           [Refresh Token]
- Lifetime: 15 minutes                         - Lifetime: 7 days
- Signed with RSA-2048 Private Key             - 32-byte secure random hex
- Contains dynamic 'kid' (SHA-256 of PubKey)   - Stored in DB as SHA-256 hash
- Stored in HttpOnly cookie: 'access_token'     - Stored in HttpOnly cookie: 'refresh_token'
- Verified by Edge Middleware on CDN           - Rotated atomically on POST /api/auth/refresh
```

#### RS256 Dynamic `kid` Implementation:
To enable key rotation and secure caching on the edge:
```python
public_pem = settings.get_public_key_pem()
kid = hashlib.sha256(public_pem).hexdigest()[:16]
token = jwt.encode(payload, private_key_pem, algorithm="RS256", headers={"kid": kid})
```

### 5.5. Edge Middleware (`middleware.ts`)
Deployed to Vercel Edge, protecting all `/data/**` requests before CDN lookup:
- Parses `access_token` from cookies.
- Decodes header and validates non-empty `kid`.
- Imports public key via `jose.importSPKI(pem, 'RS256')` (cached in memory).
- Verifies token signature, issuer, audience, and 10-second clock tolerance.
- Validates that `role` is `sst_student` or `admin`.
- If authorized, passes request to CDN with `x-middleware-next: 1` and sets `vercel-cdn-cache-control: max-age=3600, s-maxage=3600`.
- If invalid or expired, returns `401 Unauthorized` with `cache-control: private, no-store`.

### 5.6. CSRF Mitigation
- All state-mutating requests (`POST`, `PUT`, `PATCH`, `DELETE`) require an `x-csrf-token` header.
- CSRF tokens are generated via `secrets.token_hex(32)` during login/refresh and returned in the JSON payload.
- The frontend `apiClient.ts` stores the CSRF token in memory and automatically attaches it as the `x-csrf-token` header.
- Origin validation ensures requests originate from approved frontend hosts (`settings.APP_ORIGIN`, `localhost:5173`, `localhost:3000`).

---

## 6. Dual-Persistence & Storage Architecture

### 6.1. Primary Engine: MongoDB Atlas
When `MONGODB_URI` is provided, the backend connects to MongoDB Atlas:
- **`users` Collection**:
  - `google_sub_id` (Unique index): Google subject ID.
  - `email` (Unique index): SST email address.
  - `username` (Unique index, sparse): Unique student handle (`^[a-zA-Z0-9_]{3,30}$`).
  - `display_name`: Full name.
  - `active_term`: Currently active study term (1–16).
  - `role`: `"student"`, `"moderator"`, or `"admin"`.
  - `avatar_url`, `bio`, `needs_profile_setup`.
- **`refresh_tokens` Collection**:
  - `token_hash` (Unique index): SHA-256 hash of the refresh token.
  - `user_id`: Reference to user document.
  - `expires_at`: ISO timestamp with **TTL index** for automatic eviction.
- **`bookmarks` Collection**:
  - Compound unique index on `(user_id, note_id)`.
- **`comments` Collection**:
  - `note_id`, `user_id`, `content` (max 1000 chars), `parent_id` (for nested replies).
  - `score`: Aggregate score (`len(upvoted_by) - len(downvoted_by)`).
  - `status`: `"published"`, `"quarantined"`, `"reported"`, `"deleted"`.
  - `upvoted_by`: Array of user IDs.
  - `downvoted_by`: Array of user IDs.
  - `report_history`: Array of `{user_id, reason, timestamp}` for audit & velocity tracking.
- **`moderation_audit_logs` Collection**:
  - Detailed record of every moderator action or automated quarantine event.
- **`notifications` Collection**:
  - In-app alerts for comment replies, upvote milestones, and report resolutions.
- **`private_notes` Collection (Scratchpad)**:
  - Note-specific scratchpads: compound unique index on `(user_id, note_id)`.
  - `content`: Markdown text up to 30,000 characters.
- **`quiz_attempts` Collection**:
  - Quiz persistence: compound unique index on `(user_id, note_id)`.
  - `selected_answers`: Map of `question_id -> [option_ids]`.
  - `checked_questions`: Map of `question_id -> boolean`.
  - `score`, `total_questions`, `percentage`, `is_completed`.

### 6.2. Dev Fallback Engine: `InMemoryStore`
Defined in `api/database.py`, `InMemoryStore` provides complete thread-safe emulation of all MongoDB collections using Python dictionaries and a threading lock:
- Automatically activated if `MONGODB_URI` is missing or fails to connect within a 5-second timeout.
- Fully supports user profiles, refresh token hashing, bookmark toggles, threaded comments, upvoting/downvoting, report tracking, scratchpads, and quiz attempt persistence.
- Guarantees zero local development blockers.

---

## 7. Distributed Rate Limiting Subsystem

Defined in `api/rate_limiter.py`:
- **Algorithm**: Sliding-Window Counter using millisecond timestamps.
- **Upstash Redis REST Implementation**:
  - Safely extracts client IP from `x-vercel-forwarded-for` (handling reverse proxy chains) or client socket host.
  - Issues atomic Redis pipeline commands via HTTP REST:
    1. `ZREMRANGEBYSCORE key 0 (now - window_seconds)`: Prune entries outside the rolling window.
    2. `ZCARD key`: Count remaining events in current window.
    3. `ZADD key now random_uuid`: Record current attempt.
    4. `EXPIRE key window_seconds`: Set key TTL.
- **Configured Limits**:
  - `GET /api/auth/nonce`: 60 requests / 60 seconds.
  - `POST /api/auth/google`: 15 requests / 60 seconds.
  - `POST /api/auth/refresh`: 30 requests / 60 seconds.
  - `POST /api/notes/{id}/comments`: 10 comments / 60 seconds.
- **Fail-Safe Fallback**: If Upstash credentials are missing or unreachable, the system automatically falls back to `InMemoryRateLimiter` without interrupting service.

---

## 8. Curriculum Content Pipeline & Schema v1

### 8.1. Note Schema Definition
Every course lecture note conforms to **JSON Schema Version 1**:
```json
{
  "schema_version": 1,
  "note_id": "cml-l01-intro-linear-regression",
  "term": "Term 5",
  "subject_code": "CML",
  "topic_title": "Introduction to Machine Learning & Linear Regression",
  "tags": ["machine-learning", "linear-regression", "gradient-descent", "loss-functions"],
  "learning_objectives": [
    "Formulate the Mean Squared Error (MSE) objective function",
    "Derive analytical Ordinary Least Squares (OLS) normal equation: w = (X^T X)^{-1} X^T y",
    "Implement Batch Gradient Descent in Python with convergence checks"
  ],
  "summary": "Deep dive into regression fundamentals, vector formulation, analytical vs iterative solutions...",
  "key_takeaways": [
    "Closed-form normal equations require O(d^3) computation; gradient descent scales to O(n d)",
    "Feature standardization ensures circular convex contours and stable learning rates"
  ],
  "sections": [
    {
      "section_id": "mathematical-formulation",
      "heading": "1. Mathematical Formulation & Normal Equations",
      "body": "Detailed Markdown content with LaTeX formulas: $\\min_w \\frac{1}{2n} \\|Xw - y\\|^2_2$...",
      "citations": ["Bishop PRML Chapter 3", "Hastie ESL Chapter 3"]
    }
  ],
  "quiz": [
    {
      "question_id": "cml-l01-q1",
      "question": "What is the primary computational bottleneck when solving $w = (X^T X)^{-1} X^T y$ for large feature dimensions $d$?",
      "options": [
        {"id": "A", "text": "Computing the matrix product $X^T y$"},
        {"id": "B", "text": "Inverting the $d \\times d$ Gram matrix $(X^T X)$ which costs $\\mathcal{O}(d^3)$"},
        {"id": "C", "text": "Evaluating predictions during inference"}
      ],
      "correct_answer": ["B"],
      "explanation": "Matrix inversion scales with $\\mathcal{O}(d^3)$, becoming intractable when $d > 10^4$ features.",
      "multi_select": false
    }
  ],
  "last_updated": "2026-10-20T12:00:00Z",
  "approval_status": "approved"
}
```

### 8.2. Static Compilation Pipeline (`tooling/build_notes.py`)
1. Scans `content/fixtures/` recursively for `.json` notes.
2. Validates schema constraints:
   - `note_id`: Regex `^[a-z0-9-]+$`.
   - `approval_status`: Strictly `"approved"`.
   - Required fields, sections, quizzes, and objectives.
3. Outputs validated notes to:
   - `data/notes/<note_id>.json` (server & edge distribution).
   - `web/public/data/notes/<note_id>.json` (local frontend preview).
4. Compiles high-speed search index `data/notes-index.json` containing note metadata (excluding large body text) pre-sorted by term and subject.

### 8.3. Curriculum Scope Currently Implemented
- **Term 3**:
  - `CML`: Foundations of Classical Machine Learning.
  - `CN`: Computer Networks (OSI layer model, packet switching).
- **Term 5**:
  - `CML` (Lectures 1–15 Gold Standard): Linear & Polynomial Regression, Ridge/Lasso Regularization, Logistic Regression, Convex Optimization, Linear Discriminant Analysis (LDA), Support Vector Machines (SVM & Kernels), Decision Trees & Impurity Metrics, Ensemble Methods (Random Forests, Gradient Boosting, XGBoost), Principal Component Analysis (PCA & SVD), K-Means & Hierarchical Clustering, Expectation-Maximization (EM & GMM), Naive Bayes, Evaluation Metrics (ROC/AUC, PR curves).
  - `Computer Networks` (Lectures 1–13): Network Core & Packet Switching, Application Layer (HTTP/1.1, HTTP/2, HTTP/3, DNS), Transport Layer (UDP, TCP 3-way handshake, Flow & Congestion Control: Reno/Cubic), Network Layer (IP addressing, Subnetting, Dijkstra Link-State, Distance-Vector BGP/OSPF), Link Layer (Ethernet, ARP traces, CSMA/CD), Production Network Triage Playbooks.

---

## 9. Interactive Features & Student Workspace

### 9.1. Interactive Quiz & Self-Assessment Subsystem
- **Component**: `web/src/components/QuizSection.tsx`.
- **LaTeX Math Support**: Quiz questions, options, and explanations render full $\LaTeX$ math expressions via `QuizMarkdown.tsx` (using regex split on `$$...$$` and `$...$` combined with `rehype-katex`).
- **Persistence API (`api/quizzes.py`)**:
  - `GET /api/notes/{note_id}/quiz/attempt`: Fetches saved quiz progress for current student.
  - `PUT /api/notes/{note_id}/quiz/attempt`: Debounced persistence of student's selected answers, checked questions, score, and completion state.
  - `DELETE /api/notes/{note_id}/quiz/attempt`: Resets quiz attempt for clean retries.
  - `GET /api/users/me/quiz-stats`: Returns student's global quiz statistics (total attempted, completed, accuracy percentage).
- **UI Highlights**:
  - Circular SVG accuracy progress ring.
  - Interactive answer checking with instant visual feedback (green/red borders).
  - Explanations card revealed upon checking.
  - Post-completion Question-by-Question review screen with retry controls.

### 9.2. Student Private Scratchpad Subsystem
- **Component**: `web/src/components/Scratchpad.tsx` embedded in `RightSidebar.tsx`.
- **Functionality**:
  - Note-anchored personal study notes (up to 30,000 characters).
  - Split Editor & Live Preview modes with real-time Markdown and KaTeX math rendering.
  - **Debounced Auto-Save (1200ms)**: Automatically syncs edits to `PUT /api/notes/{note_id}/scratchpad`.
  - **Race Condition & Abort Controller Guards**: Cancels in-flight requests if note changes or new edits occur before network completion.
  - Shows clear sync status indicators: "Saving...", "Saved", "Unsaved changes".
  - Metadata endpoint `GET /api/scratchpads/summary` returns a list of notes containing scratchpad notes to badge them in the UI.

### 9.3. Threaded Discussions & Comments Subsystem
- **Component**: `web/src/components/CommentSection.tsx`.
- **Functionality**:
  - Lecture-wide or section-anchored discussion threads.
  - Arbitrary nested replies (`parent_id`).
  - Markdown editor with KaTeX math rendering and character count limits (max 1000 chars).
  - **Net-Score Voting Engine (`POST /api/comments/{comment_id}/vote`)**:
    - Supports `"upvote"` and `"downvote"`.
    - Clicking the same action toggles/removes the vote.
    - Score is dynamically computed: $\text{score} = \text{len(upvoted\_by)} - \text{len(downvoted\_by)}$.
    - Optimistic UI updates with automatic rollback on network failure.
  - **Reporting & Auto-Quarantine Engine**:
    - Students can report inappropriate content with categories (`spam`, `harassment`, `inappropriate`, `misinformation`, `other`).
    - **Velocity Auto-Quarantine**: If a comment receives 5+ reports within a rolling 2-hour window (`AUTO_QUARANTINE_REPORT_THRESHOLD`), its status is automatically changed to `"quarantined"` and removed from public view until moderator review.
    - Rate limit: 10 comments / 60 seconds.

### 9.4. Content Moderation & Audit System
- **Page**: `web/src/pages/ModerationPage.tsx`.
- **Authorization**: Accessible strictly to users with role `"moderator"` or `"admin"`.
- **Endpoints (`api/moderation.py`)**:
  - `GET /api/moderation/queue`: Returns all reported or quarantined comments.
  - `POST /api/moderation/queue/{comment_id}/resolve`: Takes action (`"approve"` to republish, `"delete"` to permanently remove).
  - `GET /api/moderation/audit-log`: Returns paginated audit trail of all moderation actions and automated quarantine events.

### 9.5. In-App Notifications Subsystem
- **Component**: `web/src/components/NotificationsDropdown.tsx`.
- **Notification Triggers**:
  - Reply to a student's comment (`type: "reply"`).
  - Upvote milestones (e.g., 10, 50 upvotes) (`type: "system"`).
  - Report resolution updates (`type: "report_resolved"`).
- **Endpoints (`api/notifications.py`)**:
  - `GET /api/notifications`: Returns user's notification list and unread count.
  - `PATCH /api/notifications/{id}/read`: Marks individual notification as read.
  - `POST /api/notifications/mark-all-read`: Marks all notifications as read.

### 9.6. Student Profiles & Reputation System
- **Pages/Modals**: `ProfilePage.tsx`, `SettingsPage.tsx`, `StudentProfileModal.tsx`, `ProfileSetupModal.tsx`.
- **Customizable Attributes**:
  - Username: Unique regex `^[a-zA-Z0-9_]{3,30}$`.
  - Display Name: 1–100 characters.
  - Bio: Up to 500 characters.
  - Avatar URL: Custom image link.
  - Active Term: Default curriculum landing term.
- **Dynamic Reputation Badges**:
  - 🎓 **Academic Peer**: Default badge for all active students.
  - ⭐ **Helpful Contributor**: Awarded at $\ge 10$ aggregate comment upvotes.
  - 🔥 **Top Contributor**: Awarded at $\ge 30$ aggregate comment upvotes.
  - 🏆 **Master Scholar**: Awarded at $\ge 100$ aggregate comment upvotes.
  - 🛡️ **Community Guardian**: Awarded to users with `"moderator"` or `"admin"` roles.

---

## 10. Frontend Design System & Theme Engine

### 10.1. Curated Themes & Comprehensive Light Mode
Defined in `web/src/index.css` via CSS variable tokens:
1. `oled-slate`: Pure black backgrounds (`#000000`), slate cards (`#0b0f19`), ice-blue accents (`#38bdf8`).
2. `minimalist-midnight`: Deep navy midnight (`#090d16`), dark slate cards, purple-indigo accents (`#818cf8`).
3. `clean-light`: Pure crisp paper white (`#f8fafc`), clean border lines (`#e2e8f0`), high-contrast dark slate text (`#0f172a`), refined subtle shadows.
- **Full Light Mode Support**: Every single component (Navbar, Sidebar, Reader, Code blocks, Quiz cards, Comments, Modals, Badges) is styled with complete light mode compatibility.

### 10.2. Compact Vertical Typography Density
The reader view implements a streamlined, compact vertical typography hierarchy:
- Reduced vertical margins on headings (`h1`, `h2`, `h3`).
- Tightened paragraph line heights (`leading-relaxed`).
- Compact table layouts and callout cards (Objectives, Key Takeaways).
- Maximizes visible code and mathematical derivations on laptop screens without excessive scrolling.

### 10.3. Spotlight Command Palette (`Ctrl+K` / `Cmd+K`)
- **Component**: `web/src/components/SearchModal.tsx`.
- Global keyboard listener captures `Ctrl+K` or `Cmd+K`.
- Real-time search across note titles, summaries, tags, terms, and subject codes.
- Full keyboard accessibility: `ArrowUp`, `ArrowDown`, `Enter` (to navigate), `Escape` (to close).

---

## 11. Complete REST API Reference

All protected endpoints require authentication via the `access_token` HttpOnly cookie or `Authorization: Bearer <token>` header. State-mutating endpoints (`POST`, `PUT`, `PATCH`, `DELETE`) require the `x-csrf-token` header.

| Method | Endpoint | Description | Auth | CSRF | Rate Limit |
|---|---|---|---|---|---|
| `GET` | `/api/health` | Health check & service identifier | No | No | None |
| `GET` | `/api/auth/nonce` | Generate single-use login nonce | No | No | 60/min |
| `POST` | `/api/auth/google` | Google ID Token / Dev Mock login | No | Origin | 15/min |
| `POST` | `/api/auth/refresh` | Rotate 7-day refresh token | Cookie | No | 30/min |
| `POST` | `/api/auth/logout` | Revoke session & clear cookies | Cookie | **Yes** | None |
| `GET` | `/api/users/me` | Fetch authenticated student profile | Yes | No | None |
| `PATCH` | `/api/users/me` | Update student profile (username, bio, etc.)| Yes | **Yes** | None |
| `DELETE`| `/api/users/me` | Delete account and all student data | Yes | **Yes** | None |
| `GET` | `/api/users/{username}/profile`| Public student profile & badges | Yes | No | None |
| `GET` | `/api/users/me/quiz-stats` | Global quiz statistics for current student | Yes | No | None |
| `GET` | `/api/bookmarks` | List all bookmarked note IDs | Yes | No | None |
| `PUT` | `/api/bookmarks/{note_id}` | Bookmark a note | Yes | **Yes** | None |
| `DELETE`| `/api/bookmarks/{note_id}`| Remove bookmark | Yes | **Yes** | None |
| `GET` | `/api/notes/{note_id}/comments`| List threaded comments for note | Yes | No | None |
| `POST` | `/api/notes/{note_id}/comments`| Create comment or reply | Yes | **Yes** | 10/min |
| `POST` | `/api/comments/{id}/vote` | Upvote or downvote comment | Yes | **Yes** | None |
| `DELETE`| `/api/comments/{id}` | Delete comment (author/moderator)| Yes | **Yes** | None |
| `POST` | `/api/comments/{id}/report` | Report comment for moderation | Yes | **Yes** | None |
| `GET` | `/api/moderation/queue` | Moderation queue (Moderator/Admin)| Moderator| No | None |
| `POST` | `/api/moderation/queue/{id}/resolve`| Approve or delete reported comment| Moderator| **Yes** | None |
| `GET` | `/api/moderation/audit-log` | View moderation audit trail | Moderator| No | None |
| `GET` | `/api/notifications` | List notifications & unread count | Yes | No | None |
| `PATCH`| `/api/notifications/{id}/read`| Mark notification as read | Yes | **Yes** | None |
| `POST` | `/api/notifications/mark-all-read`| Mark all notifications as read | Yes | **Yes** | None |
| `GET` | `/api/notes/{note_id}/quiz/attempt`| Get saved quiz attempt | Yes | No | None |
| `PUT` | `/api/notes/{note_id}/quiz/attempt`| Save/update quiz attempt | Yes | **Yes** | None |
| `DELETE`| `/api/notes/{note_id}/quiz/attempt`| Reset quiz attempt | Yes | **Yes** | None |
| `GET` | `/api/scratchpads/summary` | Get note IDs with active scratchpads | Yes | No | None |
| `GET` | `/api/notes/{note_id}/scratchpad`| Get scratchpad for note | Yes | No | None |
| `PUT` | `/api/notes/{note_id}/scratchpad`| Save scratchpad content | Yes | **Yes** | None |
| `GET` | `/data/notes-index.json` | Static note catalogue index | Edge JWT | No | Edge CDN |
| `GET` | `/data/notes/{id}.json` | Static lecture note payload | Edge JWT | No | Edge CDN |

---

## 12. Environment Variables & Configuration Reference

Configured in `.env` (loaded via `api/config.py`):

| Variable Name | Type | Default Value | Description |
|---|---|---|---|
| `ENVIRONMENT` | string | `"development"` | Active environment (`"development"`, `"production"`, `"test"`) |
| `GOOGLE_CLIENT_ID` | string | `""` | Google OAuth Web Client ID |
| `GOOGLE_ALLOWED_HD` | string | `"sst.scaler.com"` | Permitted Google Workspace hosted domain |
| `ALLOW_DEV_MOCK_LOGIN` | boolean | `false` | Enables `mock:student@sst.scaler.com` dev bypass |
| `SPECIAL_EMAILS` | string | `"acca3402@gmail.com"`| Comma-separated emails bypassing roll-number checks |
| `JWT_PRIVATE_KEY_B64` | base64 | `""` | RSA-2048 private key in base64 (for token signing) |
| `JWT_PUBLIC_KEY_B64` | base64 | `""` | RSA-2048 public key in base64 (for edge verification) |
| `JWT_ISSUER` | string | `"sst-study-platform"`| Registered JWT issuer (`iss`) claim |
| `JWT_AUDIENCE` | string | `"sst-students"` | Registered JWT audience (`aud`) claim |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| int | `15` | RS256 access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | int | `7` | Refresh token lifetime |
| `MONGODB_URI` | string | `""` | MongoDB Atlas connection string (falls back to memory if empty) |
| `MONGODB_DB_NAME` | string | `"sst_study"` | MongoDB database name |
| `UPSTASH_REDIS_REST_URL` | string | `""` | Upstash Redis REST endpoint (falls back to memory if empty) |
| `UPSTASH_REDIS_REST_TOKEN` | string | `""` | Upstash Redis REST authentication token |
| `APP_ORIGIN` | string | `"http://localhost:5173"` | Approved frontend origin for CORS and CSRF validation |
| `COOKIE_SECURE` | boolean | `false` | Sets `Secure` flag on cookies (`true` in production) |
| `AUTO_QUARANTINE_REPORT_THRESHOLD`| int | `5` | Report count threshold to auto-quarantine comments |
| `AUTO_QUARANTINE_WINDOW_HOURS` | int | `2` | Rolling window hours for report velocity |

---

## 13. How to Run, Test & Build the Codebase

### Prerequisites:
- **Node.js**: $\ge 18.0$ (Node 22 recommended)
- **Python**: $\ge 3.10$ (Python 3.12 recommended)

### 1. Unified Development Command:
```bash
npm run dev
```
Launches `tooling/dev.js`, which concurrently:
1. Compiles notes via `tooling/build_notes.py`.
2. Starts FastAPI backend on `http://127.0.0.1:8000` with hot-reload.
3. Starts Vite frontend on `http://localhost:5173`.

### 2. Individual Commands:
- **Run Backend Only**:
  ```bash
  npm run dev:api
  # Or: python -m uvicorn api.index:app --reload --port 8000
  ```
- **Run Frontend Only**:
  ```bash
  npm run dev:web
  # Or: cd web && npm run dev
  ```
- **Recompile Static Notes**:
  ```bash
  npm run build:notes
  # Or: python tooling/build_notes.py
  ```
- **Run Backend Acceptance Tests (39 tests)**:
  ```bash
  pytest
  ```
- **Run Frontend Component Tests (16 tests)**:
  ```bash
  npm --prefix web run test
  ```
- **Build Full Production Bundle**:
  ```bash
  npm run build
  ```

---

## 14. Essential Invariants & Guidelines for AI Models Modifying This Codebase

When writing code or assisting with features in this repository, **you must observe the following invariants**:

1. **Never Break RS256 Dynamic `kid`**:
   The edge middleware expects the access JWT header to contain `kid` matching the SHA-256 fingerprint of the public key. Never switch to HS256 or omit the `kid` header in `api/auth.py`.
2. **Never Bypass CSRF on State Mutations**:
   All new `POST`, `PUT`, `PATCH`, or `DELETE` endpoints must call `validate_csrf(request)` unless specifically exempted (e.g., initial login).
3. **Always Preserve Dual-Persistence Parity**:
   Whenever you add or modify a database operation in `api/`, you **must** update both the MongoDB query block AND the `in_memory_store` fallback block in `api/database.py`. If you update one without the other, local dev or production will break.
4. **Never Parse Raw HTML in Markdown**:
   In `MarkdownViewer.tsx` and `CommentSection.tsx`, always maintain `skipHtml={true}` with `rehype-sanitize`. Scaler notes and comments must never be exposed to stored XSS vectors.
5. **Always Use `QuizMarkdown` for Quiz Content**:
   Quiz question prompts, options, and explanations must be rendered through `QuizMarkdown.tsx` (not standard Markdown viewer) so that inline mathematical expressions $\LaTeX$ are properly tokenized and rendered via KaTeX.
6. **Preserve Term Access Restrictions**:
   Students can only access terms where $\text{term\_number} \le \text{max\_allowed\_term}$. Never remove or bypass this restriction in `TermsPage.tsx` or `api/auth.py`.
7. **Maintain Vanilla CSS Token Architecture**:
   Theme colors are driven by CSS custom properties in `web/src/index.css`. Avoid hardcoding arbitrary hex colors or utility classes that do not adapt to `clean-light`, `oled-slate`, and `minimalist-midnight`.
8. **Optimistic UI Updates with Rollback**:
   When implementing student interaction states (bookmarks, comment votes, quiz answers), always apply changes optimistically to React state and provide automatic rollback in the `.catch()` handler if the network request fails.
