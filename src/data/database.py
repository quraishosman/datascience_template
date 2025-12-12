"""
SQLAlchemy database connection and session management.
Works with PostgreSQL, SQLite, etc. via .env or environment variables.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from urllib.parse import quote_plus
import os
from src.utils import logger

# Read from .env or environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://analyst:supersecretpassword@localhost:5432/analytics"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False  # set True for SQL logging
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


def get_engine():
    return engine


def get_session():
    """Dependency for FastAPI or manual use"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


logger.info(f"Database connected → {DATABASE_URL.split('@')[-1]}")
