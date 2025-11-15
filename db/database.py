
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
from models.hospital import Hospital
from models.report_sharing import ReportSharing
from models.forecast import Forecast

# Function to create all tables
def create_db_tables():
    print("Creating database tables...")
    # Create any missing tables
    Base.metadata.create_all(bind=engine)

    # Perform lightweight migrations: add any missing columns to existing tables.
    # SQLite doesn't support ALTER TABLE ... ADD COLUMN with complex types, so we add simple compatible column declarations.
    from sqlalchemy import inspect, text
    inspector = inspect(engine)

    type_map = {
        'INTEGER': 'INTEGER',
        'String': 'TEXT',
        'TEXT': 'TEXT',
        'Float': 'REAL',
        'DateTime': 'TEXT',
        'Boolean': 'BOOLEAN'
    }

    for table_name, table in Base.metadata.tables.items():
        try:
            existing = [c['name'] for c in inspector.get_columns(table_name)]
        except Exception:
            existing = []

        for col in table.columns:
            col_name = col.name
            if col_name in existing:
                continue

            # Derive a simple SQLite-compatible type
            col_type = None
            if hasattr(col.type, 'python_type'):
                pytype = col.type.python_type
                if pytype is int:
                    col_type = 'INTEGER'
                elif pytype is float:
                    col_type = 'REAL'
                elif pytype is bool:
                    col_type = 'BOOLEAN'
                else:
                    col_type = 'TEXT'
            else:
                # Fallback based on type name
                tname = type(col.type).__name__
                col_type = type_map.get(tname, 'TEXT')

            default_clause = ''
            try:
                if col.default is not None and getattr(col.default, 'arg', None) is not None:
                    arg = col.default.arg
                    if isinstance(arg, str):
                        default_clause = f" DEFAULT '{arg}'"
                    else:
                        default_clause = f" DEFAULT {arg}"
            except Exception:
                default_clause = ''

            ddl = f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}{default_clause}"
            try:
                with engine.connect() as conn:
                    conn.execute(text(ddl))
                    conn.commit()
                print(f"Added column {col_name} to {table_name}")
            except Exception as e:
                print(f"Could not add column {col_name} to {table_name}: {e}")

    print("Database tables created and migrated successfully.")

if __name__ == "__main__":
    create_db_tables()
