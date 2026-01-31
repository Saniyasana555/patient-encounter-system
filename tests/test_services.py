"""Unit tests for patient, doctor, and appointment services."""

from datetime import datetime, timedelta, timezone
import pytest
from sqlalchemy.orm import Session
from pydantic import ValidationError

from src.database import Base, engine, SessionLocal
from src.schemas.patient import PatientCreate
from src.schemas.doctor import DoctorCreate
from src.schemas.appointment import AppointmentCreate
from src.services.patient_service import create_patient, get_patient
from src.services.doctor_service import create_doctor, deactivate_doctor, get_doctor
from src.services.appointment_service import create_appointment, list_appointments

# pylint: disable=redefined-outer-name,unused-argument


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test run."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def db_session():
    """Provide a fresh database session for each test."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_patient(db_session: Session):
    """Create a sample patient for testing."""
    patient_data = PatientCreate(
        first_name="Aman", last_name="A", email="Aman@example.com", phone="1234567890"
    )
    return create_patient(db_session, patient_data)


@pytest.fixture
def sample_doctor(db_session: Session):
    """Create a sample doctor for testing."""
    doctor_data = DoctorCreate(full_name="Dr. Swathi", specialization="Cardiology")
    return create_doctor(db_session, doctor_data)


def test_create_patient(db_session: Session):
    """Test patient creation."""
    patient_data = PatientCreate(
        first_name="Rahul",
        last_name="Shetty",
        email="Rahul@example.com",
        phone="9876543210",
    )
    patient = create_patient(db_session, patient_data)
    assert patient.id > 0
    assert patient.email == "Rahul@example.com"


def test_get_patient_not_found(db_session: Session):
    """Test patient lookup fails for non-existent ID."""
    with pytest.raises(Exception):
        get_patient(db_session, 999)


def test_create_doctor(db_session: Session):
    """Test doctor creation."""
    doctor_data = DoctorCreate(full_name="Dr. Jaya", specialization="Dermatology")
    doctor = create_doctor(db_session, doctor_data)
    assert doctor.id > 0
    assert doctor.active is True


def test_deactivate_doctor(db_session: Session):
    """Test doctor deactivation."""
    doctor_data = DoctorCreate(full_name="Dr. Mithali", specialization="Neurology")
    doctor = create_doctor(db_session, doctor_data)
    doctor = deactivate_doctor(db_session, doctor.id)
    assert doctor.active is False


def test_get_doctor_not_found(db_session: Session):
    """Test doctor lookup fails for non-existent ID."""
    with pytest.raises(Exception):
        get_doctor(db_session, 999)


def test_create_valid_appointment(db_session: Session, sample_patient, sample_doctor):
    """Test appointment creation succeeds."""
    start_time = datetime.now(timezone.utc) + timedelta(hours=1)
    appt_data = AppointmentCreate(
        patient_id=sample_patient.id,
        doctor_id=sample_doctor.id,
        start_time=start_time,
        duration_minutes=30,
    )
    appt = create_appointment(db_session, appt_data)
    assert appt.id > 0
    assert appt.duration_minutes == 30


def test_conflict_appointment(db_session: Session, sample_patient, sample_doctor):
    """Test appointment conflict detection."""
    start_time = datetime.now(timezone.utc) + timedelta(hours=2)
    appt1 = AppointmentCreate(
        patient_id=sample_patient.id,
        doctor_id=sample_doctor.id,
        start_time=start_time,
        duration_minutes=60,
    )
    create_appointment(db_session, appt1)

    appt2 = AppointmentCreate(
        patient_id=sample_patient.id,
        doctor_id=sample_doctor.id,
        start_time=start_time + timedelta(minutes=30),
        duration_minutes=30,
    )
    with pytest.raises(Exception):
        create_appointment(db_session, appt2)


def test_invalid_duration(sample_patient, sample_doctor):
    """Test appointment validation fails for short duration."""
    start_time = datetime.now(timezone.utc) + timedelta(hours=3)
    with pytest.raises(ValidationError):
        AppointmentCreate(
            patient_id=sample_patient.id,
            doctor_id=sample_doctor.id,
            start_time=start_time,
            duration_minutes=5,
        )


def test_list_appointments(db_session: Session, sample_patient, sample_doctor):
    """Test listing appointments for a doctor on a given date."""
    start_time = datetime.now(timezone.utc) + timedelta(hours=4)
    appt_data = AppointmentCreate(
        patient_id=sample_patient.id,
        doctor_id=sample_doctor.id,
        start_time=start_time,
        duration_minutes=30,
    )
    appt = create_appointment(db_session, appt_data)

    results = list_appointments(db_session, date=start_time, doctor_id=sample_doctor.id)
    assert len(results) == 1
    assert results[0].id == appt.id
