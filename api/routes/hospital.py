
import os
import sys
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from dependencies import get_db
from models.hospital import Hospital
from models.doctor import Doctor
from schemas.hospital import HospitalResponse
from schemas.user import DoctorResponse

router = APIRouter()

@router.get("/", response_model=List[HospitalResponse])
def list_hospitals(
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    List all hospitals with optional filtering by city/state.
    Supports pagination.
    """
    query = db.query(Hospital).filter(Hospital.is_active == True)
    
    if city:
        query = query.filter(Hospital.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(Hospital.state.ilike(f"%{state}%"))
    
    hospitals = query.offset(skip).limit(limit).all()
    return hospitals

@router.get("/{hospital_id}", response_model=HospitalResponse)
def get_hospital(hospital_id: int, db: Session = Depends(get_db)):
    """
    Get hospital details by ID.
    """
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
    if not hospital.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital is inactive")
    return hospital

@router.get("/{hospital_id}/doctors", response_model=List[DoctorResponse])
def get_hospital_doctors(
    hospital_id: int,
    specialization: Optional[str] = Query(None, description="Filter by specialization"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all doctors in a hospital, optionally filtered by specialization.
    """
    hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
    if not hospital.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital is inactive")
    
    query = db.query(Doctor).filter(
        Doctor.hospital_id == hospital_id,
        Doctor.is_active == True
    )
    
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    
    doctors = query.offset(skip).limit(limit).all()
    return doctors

