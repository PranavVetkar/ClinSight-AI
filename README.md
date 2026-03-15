# ClinSight-AI

> Modern AI-powered Clinical Document Q&A System — PDF processing, local vector search, and Gemini-driven insights.

```
Angular ──► FastAPI ──► PyMuPDF ──► sentence-transformers ──► ChromaDB ──► Gemini
```

## Overview
ClinSight-AI is a full-stack application designed for clinical document analysis. It allows users to upload PDF records, which are then processed, chunked, and embedded locally. The system utilizes RAG (Retrieval-Augmented Generation) with Google's Gemini to provide accurate answers based on the uploaded clinical data, all within a secure, authenticated environment using local SQLite and JWT.

## Quick Start

### 1. Backend
The backend uses FastAPI and a local SQLite database for user management and document metadata.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env       # Add your GEMINI_API_KEY
python seed_users.py       # Create demo accounts
uvicorn main:app --reload --port 8000
```
API docs: http://localhost:8000/docs

### 2. Frontend
The frontend is built with Angular and provides a premium, responsive dashboard for document management.

```bash
cd frontend
npm install
ng serve
```
App: http://localhost:4200

---

## Project Structure

```
ClinSight-AI/
├── backend/
│   ├── main.py             # FastAPI entry point
│   ├── config.py           # Settings & Env handling
│   ├── seed_users.py       # Demo data script
│   ├── requirements.txt
│   ├── .env                # Credentials & Config
│   ├── auth/               # JWT & Password hashing
│   ├── db/                 # Local SQLite (app.db) access
│   ├── documents/          # PDF processing & Embeddings
│   └── qa/                 # Gemini RAG integration
│
└── frontend/
    └── src/app/
        ├── pages/          # Login, Register, Dashboard, Detail
        ├── services/       # Auth, Document, QA API clients
        ├── guards/         # Route protection
        └── interceptors/   # Auth headers
```

## Required Credentials

| Key | Description | Where to get |
|-----|-------------|--------------|
| `GEMINI_API_KEY` | Power the RAG Q&A | [Google AI Studio](https://aistudio.google.com/apikey) |
| `JWT_SECRET_KEY` | Sign auth tokens | `openssl rand -hex 32` (or use default dev secret) |

## API Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | ❌ | Register a new user |
| POST | `/auth/login` | ❌ | Get JWT access token |
| POST | `/documents/upload` | ✅ | Upload & process PDF |
| GET | `/documents/` | ✅ | List user documents |
| DELETE | `/documents/{id}` | ✅ | Remove document & vectors |
| POST | `/qa/ask` | ✅ | Contextual Q&A via Gemini |

## Development
- **Database**: Local SQLite is stored in `backend/local_data/app.db`.
- **Vector Store**: ChromaDB persists in `backend/chroma_db/`.
- **Embeddings**: `sentence-transformers` runs locally for privacy and cost-efficiency.
