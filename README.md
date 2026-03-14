# ClinSight-AI

> Stage 1 MVP — AI-powered document Q&A with JWT auth, PDF processing, vector search, and Gemini.

```
Angular ──► FastAPI ──► PyMuPDF ──► sentence-transformers ──► ChromaDB ──► Gemini
```

## Quick Start

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in your credentials
uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 2. Frontend
```bash
cd frontend
npm install
ng serve
```

App: http://localhost:4200

---

## Project Structure

```
AI-Knowledge-OS/
├── backend/
│   ├── main.py             # FastAPI entry point
│   ├── config.py           # Env var settings
│   ├── requirements.txt
│   ├── .env                # Your credentials (fill in!)
│   ├── .env.example        # Credential template
│   ├── auth/               # JWT auth (register, login)
│   ├── documents/          # PDF upload, extraction, embeddings
│   ├── qa/                 # Gemini Q&A
│   └── db/                 # Firestore client
│
└── frontend/
    └── src/app/
        ├── pages/          # login, register, dashboard, document-detail
        ├── services/       # auth, document, qa services
        ├── guards/         # authGuard
        └── interceptors/   # JWT interceptor
```

## Required Credentials

| Key | Where to get |
|-----|-------------|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) |
| `FIREBASE_SERVICE_ACCOUNT_PATH` | Firebase Console → Project Settings → Service Accounts |
| `JWT_SECRET_KEY` | Run: `openssl rand -hex 32` |

### Firestore Setup
In Firebase Console, create a database with these collections:
- `users` — user accounts
- `documents` — PDF metadata  
- `queries` — Q&A history

## API Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/health` | ❌ | Health check |
| POST | `/auth/register` | ❌ | Register user |
| POST | `/auth/login` | ❌ | Login, get JWT |
| POST | `/documents/upload` | ✅ | Upload PDF |
| GET | `/documents/` | ✅ | List documents |
| DELETE | `/documents/{id}` | ✅ | Delete document |
| POST | `/qa/ask` | ✅ | Ask a question |
