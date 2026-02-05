"""Service layer for appointment-related operations."""

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.appointment import Appointment
from src.schemas.appointment import AppointmentCreate


def create_appointment(db: Session, appt: AppointmentCreate) -> Appointment:
    """Create a new appointment, checking for conflicts."""

    # Normalize new appointment times to UTC
    appt_start_utc = appt.start_time.astimezone(timezone.utc)
    new_end = appt_start_utc + timedelta(minutes=appt.duration_minutes)

    # Define day boundaries in UTC
    day_start = appt_start_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = appt_start_utc.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Fetch existing appointments for the same doctor on the same day
    existing_appts = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == appt.doctor_id,
            Appointment.start_time >= day_start,
            Appointment.start_time <= day_end,
        )
        .all()
    )

    # Conflict detection (normalize existing appointments to UTC too)
    for existing in existing_appts:
        if existing.start_time and existing.duration_minutes:
            existing_start = existing.start_time.astimezone(timezone.utc)
            existing_end = existing.end_time.astimezone(timezone.utc)
            overlap = existing_start < new_end and existing_end > appt_start_utc

            if overlap:
                raise HTTPException(status_code=409, detail="Appointment conflict")

    # Create and save the new appointment
    new_appt = Appointment(**appt.model_dump())
    db.add(new_appt)
    db.commit()
    db.refresh(new_appt)
    return new_appt


def list_appointments(
    db: Session, date: datetime, doctor_id: int | None = None
) -> list[Appointment]:
    """List appointments for a given date, optionally filtered by doctor."""

    # Normalize date to UTC
    date_utc = date.astimezone(timezone.utc)
    day_start = date_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = date_utc.replace(hour=23, minute=59, second=59, microsecond=999999)

    query = db.query(Appointment).filter(
        Appointment.start_time >= day_start,
        Appointment.start_time <= day_end,
    )

    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)

    return query.all()
