"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Connection string to your MySQL database
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")


# Create engine with connection health checks
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True,  # ensures stale connections are revalidated
    pool_recycle=3600,  # recycle connections every hour to avoid timeouts
)

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)  # pylint: disable=invalid-name

# Base class for models
Base = declarative_base()
