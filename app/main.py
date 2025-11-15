
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
# Get project root directory (parent of 'app' directory)
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)
load_dotenv(os.path.join(_project_root, '.env'))

# Add project root directory to sys.path within main.py
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from db.database import create_db_tables
from api.router import api_router

app = FastAPI(title="Aivara Backend API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],  # Frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
def on_startup():
    create_db_tables() # Create database tables on startup

app.include_router(api_router)
