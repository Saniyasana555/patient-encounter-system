"""Service layer for doctor-related operations."""

from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.doctor import Doctor
from src.schemas.doctor import DoctorCreate


def create_doctor(db: Session, doctor: DoctorCreate) -> Doctor:
    """Create a new doctor record in the database."""
    new_doctor = Doctor(**doctor.model_dump())  # Pydantic v2 style
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor


def get_doctor(db: Session, doctor_id: int) -> Doctor:
    """Retrieve a doctor by ID, or raise 404 if not found."""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


def activate_doctor(db: Session, doctor_id: int) -> Doctor:
    """Activate a doctor (set active=True)."""
    doctor = get_doctor(db, doctor_id)
    doctor.active = True
    db.commit()
    db.refresh(doctor)
    return doctor


def deactivate_doctor(db: Session, doctor_id: int) -> Doctor:
    """Deactivate a doctor (set active=False)."""
    doctor = get_doctor(db, doctor_id)
    doctor.active = False
    db.commit()
    db.refresh(doctor)
    return doctor
