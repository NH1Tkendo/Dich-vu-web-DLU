"""
database.py – SQLAlchemy engine & session factory stubs.

NOTE (Phase 1): The engine and SessionLocal are defined here but the
connection is NOT established at startup.  Do NOT import `Base.metadata.create_all`
anywhere until the DB infrastructure is ready.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    """Shared declarative base for all SQLAlchemy models."""
    pass


# ---------------------------------------------------------------------------
# Engine & session factory – wired but NOT connected during Phase 1.
# Uncomment `create_all` only after PostgreSQL is provisioned.
# ---------------------------------------------------------------------------
engine = create_engine(
    settings.DATABASE_URL,
    # pool_pre_ping=True,  # enable when DB is live
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """FastAPI dependency that yields a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
