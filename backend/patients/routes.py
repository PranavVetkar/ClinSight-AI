from fastapi import APIRouter, Depends, HTTPException
from typing import List
import uuid
from datetime import datetime

from auth.utils import get_current_user
from auth.models import TokenData
from db import local_db
from patients.models import PatientCreate, PatientOut

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/", response_model=PatientOut)
async def create_patient(
    patient_in: PatientCreate, current_user: TokenData = Depends(get_current_user)
):
    """Create a new patient record assigned to the logged-in doctor."""
    patient_id = str(uuid.uuid4())
    
    patient_doc = {
        "patient_id": patient_id,
        "user_id": current_user.uid,
        "name": patient_in.name,
        "age": patient_in.age,
        "gender": patient_in.gender,
        "mrn": patient_in.mrn,
        "notes": patient_in.notes,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    
    local_db.create_patient(patient_doc)
    return patient_doc


@router.get("/", response_model=List[PatientOut])
async def list_patients(current_user: TokenData = Depends(get_current_user)):
    """List all patients assigned to the logged-in doctor."""
    patients = local_db.list_user_patients(current_user.uid)
    return patients


@router.get("/{patient_id}", response_model=PatientOut)
async def get_patient(patient_id: str, current_user: TokenData = Depends(get_current_user)):
    """Get a specific patient's details."""
    patient = local_db.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if patient["user_id"] != current_user.uid:
        raise HTTPException(status_code=403, detail="Not authorized to view this patient")
    return patient


@router.delete("/{patient_id}")
async def delete_patient(patient_id: str, current_user: TokenData = Depends(get_current_user)):
    """Delete a patient and all their associated documents and queries."""
    patient = local_db.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if patient["user_id"] != current_user.uid:
        raise HTTPException(status_code=403, detail="Not authorized to delete this patient")
    
    # Also delete vectors
    from documents.embeddings import delete_patient_collection
    delete_patient_collection(patient_id)
    
    local_db.delete_patient(patient_id)
    return {"message": "Patient records fully deleted"}
