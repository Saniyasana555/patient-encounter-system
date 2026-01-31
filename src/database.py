"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Connection string to your MySQL database
DATABASE_URL = "mysql+pymysql://mongouhd_evernorth:U*dgQkKRuEHe@cp-15.webhostbox.net:3306/mongouhd_evernorth"

# Create engine with connection health checks
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_pre_ping=True,  # ensures stale connections are revalidated
    pool_recycle=3600,  # recycle connections every hour to avoid timeouts
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False
)  # pylint: disable=invalid-name

# Base class for models
Base = declarative_base()
