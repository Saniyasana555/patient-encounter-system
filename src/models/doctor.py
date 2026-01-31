"""SQLAlchemy model for doctors."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database import Base


class Doctor(Base):  # pylint: disable=too-few-public-methods
    """Database model representing a doctor."""

    __tablename__ = "saniya_doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")
