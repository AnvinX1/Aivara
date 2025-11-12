
import sys
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

# Add project root directory to sys.path within database.py for its own imports.
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir) # Corrected to project root
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Define the path for the SQLite database (relative to project_dir)
DATABASE_URL = "sqlite:///./aivara.db"

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class
Base = declarative_base()

# Import models here to ensure they are registered with Base.metadata
# These imports MUST happen *after* Base is defined in this module.
from models.user import User
from models.doctor import Doctor
from models.report import Report

# Function to create all tables
def create_db_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    create_db_tables()
