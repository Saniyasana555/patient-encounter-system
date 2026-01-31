"""FastAPI application entry point."""

from fastapi import FastAPI
from src.api import patients, doctors, appointments
from src.database import Base, engine

# Temporary: create tables directly before Alembic

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
app.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
