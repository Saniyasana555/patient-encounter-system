"""Service layer for patient-related operations."""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.patient import Patient
from src.schemas.patient import PatientCreate


def create_patient(db: Session, patient: PatientCreate) -> Patient:
    """Create a new patient record in the database."""
    existing = db.query(Patient).filter(Patient.email == patient.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_patient = Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


def get_patient(db: Session, patient_id: int) -> Patient:
    """Retrieve a patient by ID, or raise 404 if not found."""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
