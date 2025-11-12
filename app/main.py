
import os
import sys
from fastapi import FastAPI

# Add project root directory to sys.path within main.py
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)  # Project root is the parent of 'app' directory
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from db.database import create_db_tables
from api.router import api_router

app = FastAPI(title="Aivara Backend API")

@app.on_event("startup")
def on_startup():
    create_db_tables() # Create database tables on startup

app.include_router(api_router)
