from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    mrn: Optional[str] = None  # Medical Record Number
    notes: Optional[str] = None


class PatientOut(BaseModel):
    patient_id: str
    user_id: str
    name: str
    age: int
    gender: str
    mrn: Optional[str] = None
    notes: Optional[str] = None
    created_at: str


class PatientList(BaseModel):
    patients: List[PatientOut]
