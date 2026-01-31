"""Pydantic schemas for patient data."""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class PatientCreate(BaseModel):
    """Schema for creating a new patient."""

    first_name: str
    last_name: str
    email: EmailStr
    phone: str


class PatientRead(BaseModel):
    """Schema for reading patient details."""

    id: int = Field(..., gt=0)
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
