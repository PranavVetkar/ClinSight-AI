from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.local_db import init_db
from auth.routes import router as auth_router
from documents.routes import router as documents_router
from qa.routes import router as qa_router
from patients.routes import router as patients_router
from seed import seed_data

app = FastAPI(
    title="MedQuery AI API",
    description="Intelligent API for unstructured medical/patient records RAG and document insight extraction.",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    init_db()
    seed_data()
    # Pre-load the local embedding model into RAM so first upload is instant
    from documents.embeddings import get_model
    get_model()



# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(patients_router)
app.include_router(documents_router)
app.include_router(qa_router)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": "MedQuery AI API"}
