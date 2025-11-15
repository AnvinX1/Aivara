"""
Migration script to update the doctors table with new columns.
This will drop and recreate the doctors table with the updated schema.
WARNING: This will delete all existing doctor data!
"""

import os
import sys
import sqlite3

_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = _current_dir
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from db.database import engine, Base
from models.doctor import Doctor
from models.hospital import Hospital

def migrate_database():
    """Drop and recreate the doctors table with new schema."""
    
    db_file = "aivara.db"
    
    if not os.path.exists(db_file):
        print("Database file not found. Creating new database...")
        Base.metadata.create_all(bind=engine)
        print("Database created successfully!")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    try:
        # Check if hospital_id column exists
        cursor.execute("PRAGMA table_info(doctors)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'hospital_id' in columns and 'phone' in columns and 'registration_number' in columns and 'is_active' in columns:
            print("Database already has the required columns. No migration needed.")
            return
        
        print("Migrating database...")
        print("WARNING: This will delete all existing doctor records!")
        
        # Drop the old doctors table
        cursor.execute("DROP TABLE IF EXISTS doctors")
        
        # Commit changes
        conn.commit()
        print("Old doctors table dropped.")
        
        # Recreate the table with new schema
        Base.metadata.create_all(bind=engine)
        print("New doctors table created with updated schema!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()

