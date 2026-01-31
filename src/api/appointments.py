"""API routes for appointment management."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from src.database import SessionLocal
from src.schemas.appointment import AppointmentCreate, AppointmentRead
from src.services.appointment_service import create_appointment, list_appointments

router = APIRouter()


def get_db():
    """Provide a database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=AppointmentRead, status_code=201)
def create_appointment_endpoint(appt: AppointmentCreate, db: Session = Depends(get_db)):
    """Create a new appointment."""
    return create_appointment(db, appt)


@router.get("/", response_model=list[AppointmentRead])
def list_appointments_endpoint(
    date: datetime, doctor_id: int | None = None, db: Session = Depends(get_db)
):
    """List appointments for a given date and optional doctor."""
    return list_appointments(db, date, doctor_id)
