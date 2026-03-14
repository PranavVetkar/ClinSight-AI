from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth.models import TokenData
from auth.utils import get_current_user
from db.local_db import create_query, get_document
from documents.embeddings import query_chunks
from qa.gemini import generate_answer

router = APIRouter(prefix="/qa", tags=["qa"])


class AskRequest(BaseModel):
    doc_id: str
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    doc_id: str
    question: str


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    payload: AskRequest,
    current_user: TokenData = Depends(get_current_user),
):
    doc = get_document(payload.doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.get("user_id") != current_user.uid:
        raise HTTPException(status_code=403, detail="Access denied")

    chunks = query_chunks(current_user.uid, payload.doc_id, payload.question, top_k=5)
    answer = generate_answer(payload.question, chunks)

    create_query({
        "user_id": current_user.uid,
        "doc_id": payload.doc_id,
        "question": payload.question,
        "answer": answer,
        "asked_at": datetime.now(timezone.utc).isoformat(),
    })

    return AskResponse(
        answer=answer,
        sources=chunks,
        doc_id=payload.doc_id,
        question=payload.question,
    )
