"""Pydantic schemas for doctor data."""

from pydantic import BaseModel, Field
from datetime import datetime


class DoctorCreate(BaseModel):
    """Schema for creating a new doctor."""

    full_name: str
    specialization: str


class DoctorRead(BaseModel):
    """Schema for reading doctor details."""

    id: int = Field(..., gt=0)
    full_name: str
    specialization: str
    active: bool
    created_at: datetime

    class Config:
        orm_mode = True
