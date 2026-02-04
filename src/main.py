from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from src.database import SessionLocal, engine, Base
from src.schemas.patient import PatientCreate
from src.schemas.doctor import DoctorCreate
from src.schemas.appointment import AppointmentCreate, AppointmentRead
from src.models.patient import Patient
from src.models.doctor import Doctor
from src.models.appointment import Appointment

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medical Encounter Management System")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Patients ----------------
@app.post("/patients")
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@app.get("/patients/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# ---------------- Doctors ----------------
@app.post("/doctors")
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@app.put("/doctors/{doctor_id}/deactivate")
def deactivate_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor.active = False
    db.commit()
    db.refresh(doctor)
    return doctor


@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# ---------------- Appointments ----------------
@app.post("/appointments")
@app.post("/appointments", response_model=AppointmentRead, status_code=201)
def create_appointment(appt: AppointmentCreate, db: Session = Depends(get_db)):
    if appt.start_time <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400, detail="Appointment must be scheduled in the future"
        )

    if appt.duration_minutes < 15 or appt.duration_minutes > 180:
        raise HTTPException(
            status_code=400, detail="Duration must be between 15 and 180 minutes"
        )

    doctor = db.query(Doctor).filter(Doctor.id == appt.doctor_id).first()
    if not doctor or not doctor.active:
        raise HTTPException(status_code=400, detail="Doctor not available")

    new_end = appt.start_time + timedelta(minutes=appt.duration_minutes)
    existing_appts = (
        db.query(Appointment).filter(Appointment.doctor_id == appt.doctor_id).all()
    )

    for existing in existing_appts:
        existing_start = existing.start_time
        if existing_start.tzinfo is None:
            existing_start = existing_start.replace(tzinfo=timezone.utc)
        existing_end = existing_start + timedelta(minutes=existing.duration_minutes)
        if existing_start < new_end and existing_end > appt.start_time:
            raise HTTPException(
                status_code=409, detail="Doctor already has an overlapping appointment"
            )

    db_appt = Appointment(**appt.model_dump())  # ✅ use model_dump
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt


@app.get("/appointments", response_model=list[AppointmentRead])
@app.get("/appointments")
def list_appointments(date: datetime, doctor_id: int, db: Session = Depends(get_db)):
    start_day = datetime(date.year, date.month, date.day, tzinfo=timezone.utc)
    end_day = start_day + timedelta(days=1)

    results = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.start_time >= start_day,
            Appointment.start_time < end_day,
        )
        .all()
    )
    return results
