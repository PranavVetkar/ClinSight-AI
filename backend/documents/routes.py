import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from auth.models import TokenData
from auth.utils import get_current_user
from db.local_db import create_document, delete_document, get_document, list_patient_documents, get_patient
from documents.embeddings import add_document_chunks, delete_document_chunks
from documents.models import DocumentList, DocumentOut
from documents.processor import chunk_text, extract_text_from_pdf

router = APIRouter(prefix="/documents", tags=["documents"])

MAX_FILE_SIZE_MB = 20


@router.post("/upload", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def upload_document(
    patient_id: str,
    file: UploadFile = File(...),
    current_user: TokenData = Depends(get_current_user),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    pdf_bytes = await file.read()
    if len(pdf_bytes) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400, detail=f"File exceeds {MAX_FILE_SIZE_MB} MB limit"
        )

    full_text, page_count = extract_text_from_pdf(pdf_bytes)
    if not full_text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from this PDF")

    chunks = chunk_text(full_text)
    doc_id = str(uuid.uuid4())
    chunk_count = add_document_chunks(patient_id, doc_id, chunks)

    doc_meta = {
        "doc_id": doc_id,
        "user_id": current_user.uid,
        "patient_id": patient_id,
        "filename": file.filename,
        "page_count": page_count,
        "chunk_count": chunk_count,
        "size_bytes": len(pdf_bytes),
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }
    create_document(doc_meta)
    return DocumentOut(**doc_meta)


@router.get("/", response_model=DocumentList)
async def list_documents(patient_id: str, current_user: TokenData = Depends(get_current_user)):
    # Basic check to ensure patient exists before listing
    patient = get_patient(patient_id)
    if not patient or patient["user_id"] != current_user.uid:
        raise HTTPException(status_code=403, detail="Not authorized for this patient")

    docs = list_patient_documents(patient_id)
    return DocumentList(documents=[DocumentOut(**d) for d in docs])


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document_endpoint(
    doc_id: str, current_user: TokenData = Depends(get_current_user)
):
    doc = get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.get("user_id") != current_user.uid:
        raise HTTPException(status_code=403, detail="Access denied")

    delete_document_chunks(doc.get("patient_id"), doc_id)
    delete_document(doc_id)
