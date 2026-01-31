"""Pydantic schemas for appointment creation and reading."""

from pydantic import BaseModel, field_validator
from datetime import datetime, timezone


class AppointmentCreate(BaseModel):
    """Schema for creating an appointment with validation."""

    patient_id: int
    doctor_id: int
    start_time: datetime
    duration_minutes: int

    @field_validator("start_time")
    def validate_start_time(cls, v: datetime) -> datetime:
        """Ensure start time is in the future."""
        now = datetime.now(timezone.utc)
        if v < now:
            raise ValueError("Start time must be in the future")
        return v

    @field_validator("duration_minutes")
    def validate_duration(cls, v: int):
        """Ensure duration is at least 10 minutes."""
        if v < 10:
            raise ValueError("Duration must be at least 10 minutes")
        return v

    model_config = {"from_attributes": True}


class AppointmentRead(BaseModel):
    """Schema for reading appointment details."""

    id: int
    patient_id: int
    doctor_id: int
    start_time: datetime
    duration_minutes: int

    model_config = {"from_attributes": True}
