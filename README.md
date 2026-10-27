# Scaler School of Technology (SST) Study Platform

A modern, high-performance academic platform engineered for undergraduate computer science students at Scaler School of Technology (SST). The platform provides centralized access to curriculum lecture notes, sequential term gating, interactive threaded discussion forums, student scratchpads, and a dedicated markdown note authoring studio.

---

## Key Features

- **Academic Seniority Term Access Gating**: Automatically extracts the student's admission year from their institutional roll number (e.g., `surya.25bcs10632@sst.scaler.com` → Class of 2025) and enforces curriculum access corresponding strictly to their year of study:
  - **Year 1 (Freshmen)**: Terms 1 – 4
  - **Year 2 (Sophomores)**: Terms 1 – 8
  - **Year 3 (Juniors)**: Terms 1 – 12
  - **Year 4 (Seniors & Admins)**: Terms 1 – 16 (Full Catalogue Access)
- **Institutional Single Sign-On (SSO)**: Secure Google OAuth 2.0 restricted to `@sst.scaler.com` accounts with configurable administrator bypasses.
- **Asymmetric RS256 Token Authentication**: Ephemeral 15-minute access tokens signed via RSA-2048 private key and verified via public keys, accompanied by sliding 7-day refresh tokens stored as cryptographic SHA-256 hashes in `HttpOnly`, `SameSite=Lax` cookies.
- **CSRF & Edge Protection**: Per-session double-submit CSRF tokens required on all mutating HTTP requests (`POST`, `PUT`, `PATCH`, `DELETE`).
- **Distributed Rate Limiting**: Upstash Redis sliding-window limiters with fail-closed production semantics and automatic in-memory fallback for local development.
- **3-Panel Desktop & Mobile Reader**: Clean reading environment featuring a collapsible navigation tree, responsive table-of-contents sidebar, code syntax highlighting, and `Ctrl+K` metadata search.
- **Threaded Community Discussions**: Reddit-style 3-state voting (+1 / neutral / -1), nested reply threads with parent redaction (`[Deleted]`) to preserve child replies, and automated content safety screening.
- **Note Studio**: Authoring workspace for instructors to draft, preview, publish, and manage lecture notes in real time using GitHub-Flavored Markdown.
- **Student Productivity Tools**: Personal markdown scratchpads with auto-saving, course note bookmarking, and custom student profiles.

---

## Architecture & Technology Stack

```text
[ Client: React 19 + Vite ] <--- HTTPS / HttpOnly Cookies ---> [ API: FastAPI (Python 3.12) ]
                                                                             │
        ┌────────────────────────────┬───────────────────────────────────────┴─────────────────────────┐
        ▼                            ▼                                       ▼                         ▼
[ MongoDB Atlas ]           [ Upstash Redis ]                 [ Automated Moderation ]      [ Google OAuth 2.0 ]
(Core Persistence)       (Distributed Limiter)                  (Content Safety)           (Institutional SSO)
```

### Frontend
- **Framework**: React 19 + TypeScript
- **Bundler & Dev Server**: Vite
- **Styling**: Tailwind CSS + Custom CSS Design Tokens (zero gradients, clean interface)
- **Icons**: Lucide React
- **Markdown Processing**: `react-markdown`, `remark-gfm` (tables, task lists), `rehype-highlight` (code syntax highlighting)
- **Routing**: React Router v6

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Server Interface**: Starlette / Uvicorn ASGI
- **Validation**: Pydantic v2 schemas
- **Sanitization**: Bleach HTML sanitization engine for stored XSS prevention
- **Database Engine**:
  - **Production**: MongoDB Atlas with connection pooling
  - **Offline/Testing**: Thread-safe in-memory store (`InMemoryStore`)

---

## Directory Structure

```text
├── api/
│   ├── core/                 # Core security, config, database & dependencies
│   │   ├── config.py         # Environment variables & RSA key loader
│   │   ├── database.py       # MongoDB Atlas connection & in-memory dev store
│   │   ├── dependencies.py   # Auth, CSRF & RBAC dependency injectors
│   │   └── security.py       # Asymmetric RS256 JWT, tokens & password hashing
│   ├── routes/               # Modular REST API endpoints
│   │   ├── auth.py           # Google SSO, session refresh & profile setup
│   │   ├── bookmarks.py      # User note bookmark management
│   │   ├── comments.py       # Threaded comments, voting & report handling
│   │   ├── moderation.py     # Moderation queue & audit log management
│   │   ├── notes.py          # Notes catalogue, term filtering & CRUD
│   │   ├── notifications.py  # User notifications feed
│   │   ├── quizzes.py        # Interactive quizzes & progress stats
│   │   └── scratchpad.py     # Student notes scratchpad
│   ├── schemas/              # Pydantic v2 request & response contracts
│   ├── index.py              # Application entrypoint & middleware pipeline
│   └── requirements.txt      # Python dependencies
├── content/
│   └── fixtures/             # 31 course lecture note JSON seed files
├── scripts/
│   ├── seed_db.py            # MongoDB Atlas database seeder
│   ├── clean_db.py           # Test database cleanup script
│   └── generate_keys.py      # Asymmetric RS256 keypair generator
├── tests/                    # 45 Pytest integration and security test cases
├── web/                      # React 19 + TypeScript web application
├── .github/workflows/ci.yml  # Automated CI build and test pipeline
├── vercel.json               # Serverless edge routing & deployment config
└── README.md
```

---

## Local Development Setup

### 1. Prerequisites
- **Node.js**: v20 or higher
- **Python**: v3.12 or higher
- **Package Managers**: `npm` and `pip`

### 2. Clone Repository & Setup Environment
```bash
git clone https://github.com/its-shadow7/SST-Study-Platform.git
cd SST-Study-Platform
```

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Ensure the following essential variables are populated:
```env
ENVIRONMENT=development
ALLOW_DEV_MOCK_LOGIN=true

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_ALLOWED_HD=sst.scaler.com

# Asymmetric RS256 Keypair (generated via python scripts/generate_keys.py)
JWT_PRIVATE_KEY_B64=...
JWT_PUBLIC_KEY_B64=...

# Persistence (leave MONGODB_URI empty to run on the in-memory fallback store)
MONGODB_URI=mongodb+srv://...
MONGODB_DB_NAME=sst_study
```

### 3. Generate RS256 Keypair (Optional)
If you need fresh asymmetric RSA keys:
```bash
python scripts/generate_keys.py
```

### 4. Start the Backend API Server
```bash
# Install Python dependencies
pip install -r api/requirements.txt

# Start FastAPI with hot reload
uvicorn api.index:app --reload --port 8000
```
- Health check: `http://localhost:8000/api/health`
- OpenAPI Documentation: `http://localhost:8000/docs`

### 5. Start the Frontend Application
In a separate terminal:
```bash
cd web
npm install
npm run dev
```
Navigate to `http://localhost:5173`. The Vite development server automatically proxies all `/api` requests to port `8000`.

### 6. Seed the Database
To populate the MongoDB database with all 31 course lecture notes from `content/fixtures/`:
```bash
python scripts/seed_db.py
```

---

## Automated Testing

The platform includes a test suite covering authentication, domain enforcement, CSRF protection, rate limiting, and RBAC:

```bash
# Run all 45 automated backend tests
pytest tests/ -v
```

---

## Production Deployment

The platform is optimized for deployment on **Vercel**:
1. Connect the GitHub repository to Vercel.
2. Configure environment variables in the Vercel Dashboard under **Settings → Environment Variables**.
3. Deploy directly via Git push to `main` or through the CLI:
   ```bash
   npx vercel --prod
   ```

---

## License

Internal academic resource platform for students and faculty of Scaler School of Technology. All rights reserved.
