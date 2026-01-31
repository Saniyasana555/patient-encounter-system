from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.schemas.patient import PatientCreate, PatientRead
from src.services.patient_service import create_patient, get_patient
from src.models.patient import Patient  # <-- add this import

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PatientRead, status_code=201)
def create_patient_endpoint(patient: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db, patient)


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient_endpoint(patient_id: int, db: Session = Depends(get_db)):
    return get_patient(db, patient_id)


# NEW: list all patients
@router.get("/", response_model=list[PatientRead])
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()
