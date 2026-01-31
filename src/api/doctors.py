from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.schemas.doctor import DoctorCreate, DoctorRead
from src.services.doctor_service import create_doctor, get_doctor

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DoctorRead, status_code=201)
def create_doctor_endpoint(doctor: DoctorCreate, db: Session = Depends(get_db)):
    return create_doctor(db, doctor)


@router.get("/{doctor_id}", response_model=DoctorRead)
def get_doctor_endpoint(doctor_id: int, db: Session = Depends(get_db)):
    return get_doctor(db, doctor_id)
