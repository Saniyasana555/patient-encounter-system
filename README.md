# Patient Encounter System

A backend system built with **FastAPI**, **SQLAlchemy**, and **Pydantic** to manage patients, doctors, and appointments.  


## Features
- Manage patients and doctors
- Create and list appointments
- Conflict detection for overlapping appointments
- RESTful API with interactive Swagger UI

## Requirements
- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- Pytest (for testing)

## Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/Saniyasana555/patient-encounter-system.git
   cd patient-encounter-system
2. Install dependencies:
   pip install -r requirements.txt
3. Run the server
   uvicorn src.main:app --reload
4. Open the API docs in your browser:
   http://127.0.0.1:8000/docs

   Run the test suite with:
   pytest