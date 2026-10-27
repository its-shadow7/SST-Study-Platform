# Antigravity Study Platform (SST Study Site)

> 🤖 **AI Model & Agent Guide**: For complete technical specifications, architectural diagrams, dual-persistence mechanics, database schemas, and codebase invariants tailored for LLMs, see [AI_PROJECT_CONTEXT.md](AI_PROJECT_CONTEXT.md).

Private study platform for Scaler School of Technology (SST) students, implementing the **Antigravity Study Platform Technical Design Document (v1.1)**.

---

## Architecture Overview

- **Static Note Delivery**: Protected course notes served as static JSON files via Vercel CDN. Note reads require **zero database operations**.
- **Vercel Routing Middleware (`middleware.ts`)**: Node.js middleware verifying 15-minute asymmetric RS256 access JWTs on all `/data/**` paths **before** CDN cache lookup. Fails closed with `401 Unauthorized`.
- **FastAPI Backend (`api/`)**:
  - Google ID token verification (restricted strictly to `@sst.scaler.com` accounts and approved `GOOGLE_ALLOWED_HD`).
  - Asymmetric token signing with RSA private key.
  - Rotating 7-day refresh tokens stored as SHA-256 hashes in MongoDB Atlas.
  - CSRF header and Origin validation on state-changing endpoints.
  - Personal bookmarks CRUD with unique compound indexing (`user_id` + `note_id`).
- **Distributed Rate Limiting (`api/rate_limiter.py`)**: Upstash Redis sliding-window limiter on public auth endpoints (fails closed with `503` on Redis outage). Includes an in-memory sliding-window fallback for local development.
- **Frontend (`web/`)**: React 19 + Vite + TypeScript.
  - 3-Panel desktop reader (Navigation, Reader, Table of Contents) with responsive mobile drawer.
  - Spotlight metadata search modal (`Ctrl+K` / `Cmd+K`).
  - Themes: `oled-slate`, `minimalist-midnight`, `clean-light`.
  - Optimistic bookmarks with automatic rollback on network failure.
  - Strict Markdown safety: raw HTML disabled, KaTeX untrusted mode, Mermaid rendered as code blocks.

---

## Directory Structure

```text
├── api/                   # FastAPI backend application
│   ├── auth.py            # Token lifecycle, Google OAuth, CSRF & cookie helpers
│   ├── config.py          # Environment settings and RSA PEM loader
│   ├── database.py        # MongoDB Atlas & in-memory dev fallback store
│   ├── index.py           # FastAPI entrypoint and endpoints
│   ├── models.py          # Pydantic request/response schemas
│   ├── rate_limiter.py    # Upstash Redis & in-memory sliding-window limiter
│   └── requirements.txt   # Python dependencies
├── content/
│   └── fixtures/          # Source notes (schema version 1)
├── data/                  # Protected static assets (built by tooling)
│   ├── notes/             # Individual note JSON files
│   └── notes-index.json   # Search & navigation catalogue index
├── middleware.ts          # Vercel Routing Middleware protecting /data/**
├── tooling/
│   ├── build_notes.py     # Schema v1 validator and search index builder
│   └── generate_keys.py   # RS256 Base64 PEM keypair generator
├── tests/                 # Automated pytest suite
├── web/                   # React + Vite frontend
├── vercel.json            # Vercel deployment routes and rewrites
└── README.md
```

---

## Getting Started Locally

### 1. Prerequisites
- Node.js >= 18
- Python >= 3.10

### 2. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Key generation is already configured. If you wish to rotate keys:
```bash
python tooling/generate_keys.py
```

### 3. Build Notes Catalogue
```bash
python tooling/build_notes.py
```

### 4. Run the Backend API
```bash
# In project root:
uvicorn api.index:app --reload --port 8000
```
API health check: `http://localhost:8000/api/health`

### 5. Run the Frontend
```bash
cd web
npm install
npm run dev
```
Open `http://localhost:5173`. The Vite dev server proxies `/api` requests to port `8000` and serves protected notes from `data/`.

---

## Running Automated Tests

```bash
pytest tests/ -v
```

---

## Content Publishing Workflow

1. Add your note to `content/fixtures/` (or use the import script from `Original_Notes`).
2. Run validation and build:
   ```bash
   python tooling/build_notes.py
   ```
3. Commit and push. Vercel automatically runs `tooling/build_notes.py` during deployment before building the frontend.
