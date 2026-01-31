# reset_db.py
from src.database import Base, engine
import src.models.patient
import src.models.doctor
import src.models.appointment


def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database reset complete!")


if __name__ == "__main__":
    reset_database()
