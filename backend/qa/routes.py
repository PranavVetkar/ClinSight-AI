from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth.models import TokenData
from auth.utils import get_current_user
from db.local_db import create_query, get_patient
from documents.embeddings import query_patient_knowledge_base
from qa.gemini import generate_answer

router = APIRouter(prefix="/qa", tags=["qa"])


class AskRequest(BaseModel):
    patient_id: str
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    patient_id: str
    question: str


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    payload: AskRequest,
    current_user: TokenData = Depends(get_current_user),
):
    patient = get_patient(payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if patient.get("user_id") != current_user.uid:
        raise HTTPException(status_code=403, detail="Access denied")

    chunks = query_patient_knowledge_base(payload.patient_id, payload.question, top_k=8)
    answer = generate_answer(payload.question, chunks)

    create_query({
        "user_id": current_user.uid,
        "patient_id": payload.patient_id,
        "question": payload.question,
        "answer": answer,
        "asked_at": datetime.now(timezone.utc).isoformat(),
    })

    return AskResponse(
        answer=answer,
        sources=chunks,
        patient_id=payload.patient_id,
        question=payload.question,
    )
