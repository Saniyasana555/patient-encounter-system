"""SQLAlchemy model for appointments."""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import timedelta

from src.database import Base


class Appointment(Base):
    """Database model representing an appointment."""

    __tablename__ = "saniya_appointments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("saniya_patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("saniya_doctors.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    duration_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

    @property
    def end_time(self):
        if not self.start_time or not self.duration_minutes:
            return None

        return self.start_time + timedelta(minutes=self.duration_minutes)
