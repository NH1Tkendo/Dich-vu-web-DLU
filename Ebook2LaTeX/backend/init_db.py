"""
Initialize database - Create all tables
Run this script once before starting the application
"""
from app.core.database import engine
from app.models import Base

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
