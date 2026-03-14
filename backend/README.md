# AI Knowledge OS — Backend

FastAPI backend powering the AI Knowledge OS. Uses RAG (ChromaDB + sentence-transformers) and Gemini to answer questions from uploaded PDFs.

## Setup

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure environment
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | From [Google AI Studio](https://aistudio.google.com/apikey) |
| `FIREBASE_SERVICE_ACCOUNT_PATH` | Path to downloaded Firebase service account JSON |
| `JWT_SECRET_KEY` | Any long random string (e.g., `openssl rand -hex 32`) |

### 3. Run the server
```bash
uvicorn main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

## Project Structure

```
backend/
├── main.py               # FastAPI app, CORS, router registration
├── config.py             # Settings loaded from .env
├── requirements.txt
├── .env                  # Your credentials (gitignored)
├── .env.example          # Credential template
├── auth/
│   ├── models.py         # Pydantic models (UserCreate, Token, …)
│   ├── utils.py          # JWT encode/decode, password hashing
│   └── routes.py         # POST /auth/register, POST /auth/login
├── documents/
│   ├── models.py         # DocumentOut, DocumentList
│   ├── processor.py      # PyMuPDF text extraction + chunking
│   ├── embeddings.py     # sentence-transformers + ChromaDB
│   └── routes.py         # POST /documents/upload, GET /, DELETE /{id}
├── qa/
│   ├── gemini.py         # Gemini 1.5 Flash answer generation
│   └── routes.py         # POST /qa/ask
└── db/
    └── firestore.py      # Firebase Admin SDK + Firestore client
```

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/health` | ❌ | Health check |
| `POST` | `/auth/register` | ❌ | Register new user |
| `POST` | `/auth/login` | ❌ | Login, get JWT |
| `POST` | `/documents/upload` | ✅ | Upload PDF |
| `GET` | `/documents/` | ✅ | List user's documents |
| `DELETE` | `/documents/{doc_id}` | ✅ | Delete document |
| `POST` | `/qa/ask` | ✅ | Ask a question about a document |
