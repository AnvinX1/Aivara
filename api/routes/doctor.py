
import os
import sys # Added
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from jose import JWTError, jwt # Added after initial implementation

_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from dependencies import get_db, get_password_hash, verify_password, create_access_token, oauth2_scheme
from models.doctor import Doctor
from models.user import User
from models.report import Report
from models.report_sharing import ReportSharing
from models.hospital import Hospital
from schemas.report import ReportResponse, ReportReview
from schemas.user import DoctorCreate, DoctorResponse
from schemas.auth import Token
from datetime import datetime
from typing import Optional
from fastapi import Query
import config
import json
from services.notification_service import notify_patient_doctor_review

def get_current_doctor(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Doctor:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate doctor credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role != "doctor":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    doctor = db.query(Doctor).filter(Doctor.email == email).first()
    if doctor is None:
        raise credentials_exception
    return doctor

router = APIRouter()

@router.post("/register_doctor", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def register_doctor(doctor_data: DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.email == doctor_data.email).first()
    if db_doctor:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doctor email already registered")

    hashed_password = get_password_hash(doctor_data.password)
    
    # Get hospital if hospital_id is provided
    hospital_id = getattr(doctor_data, 'hospital_id', None)
    if hospital_id:
        hospital = db.query(Hospital).filter(Hospital.id == hospital_id).first()
        if not hospital:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")
        if not hospital.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Hospital is inactive")
    
    db_doctor = Doctor(
        email=doctor_data.email,
        hashed_password=hashed_password,
        full_name=doctor_data.full_name,
        specialization=doctor_data.specialization,
        hospital_id=hospital_id,
        phone=getattr(doctor_data, 'phone', None),
        registration_number=getattr(doctor_data, 'registration_number', None),
        is_active=True
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


@router.post("/token_doctor", response_model=Token)
def login_for_access_token_doctor(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.email == form_data.username).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Doctor account not found. Please check your email or register.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not doctor.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Doctor account is inactive. Please contact administrator.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, doctor.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password. Default password is 'Doctor@123' if not changed.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": doctor.email, "role": "doctor"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/reports/pending")
def get_pending_reports(
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db),
    status_filter: Optional[str] = Query(None, description="Filter by status: sent, under_review")
):
    """
    Get all reports sent to the current doctor that are pending review.
    Returns reports with patient information.
    """
    query = db.query(ReportSharing).filter(
        ReportSharing.doctor_id == current_doctor.id
    )
    
    if status_filter:
        query = query.filter(ReportSharing.status == status_filter)
    else:
        # Default: show sent and under_review
        query = query.filter(ReportSharing.status.in_(["sent", "under_review"]))
    
    sharings = query.order_by(ReportSharing.sent_at.desc()).all()
    
    # Build response with report and patient details
    result = []
    for sharing in sharings:
        report = db.query(Report).filter(Report.id == sharing.report_id).first()
        patient = db.query(User).filter(User.id == sharing.patient_id).first()
        
        if report and patient:
            report_dict = {
                "report": {
                    "id": report.id,
                    "report_name": report.report_name,
                    "upload_timestamp": report.upload_timestamp,
                    "hemoglobin": report.hemoglobin,
                    "wbc": report.wbc,
                    "platelets": report.platelets,
                    "rbc": report.rbc,
                    "analysis_result_json": report.analysis_result_json,
                    "review_status": report.review_status,
                    "ai_approval_status": report.ai_approval_status if hasattr(report, 'ai_approval_status') else "pending",
                },
                "patient": {
                    "id": patient.id,
                    "full_name": patient.full_name,
                    "email": patient.email,
                },
                "sharing": {
                    "id": sharing.id,
                    "status": sharing.status,
                    "patient_message": sharing.patient_message,
                    "sent_at": sharing.sent_at,
                    "created_at": sharing.created_at,
                }
            }
            result.append(report_dict)
    
    return result

@router.get("/reports/{report_id}")
def get_report_for_doctor(
    report_id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    Get detailed report information with patient data for doctor review.
    Only returns reports that have been shared to this doctor.
    """
    # Verify report is shared to this doctor
    sharing = db.query(ReportSharing).filter(
        ReportSharing.report_id == report_id,
        ReportSharing.doctor_id == current_doctor.id
    ).first()
    
    if sharing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found or not shared to this doctor"
        )
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    
    patient = db.query(User).filter(User.id == sharing.patient_id).first()
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    # Build detailed response
    report_dict = {
        "id": report.id,
        "user_id": report.user_id,
        "doctor_id": report.doctor_id,
        "report_name": report.report_name,
        "file_path": report.file_path,
        "upload_timestamp": report.upload_timestamp,
        "analysis_result_json": report.analysis_result_json,
        "doctor_notes": report.doctor_notes,
        "review_status": report.review_status,
        "ai_approval_status": report.ai_approval_status if hasattr(report, 'ai_approval_status') else "pending",
        "doctor_approval_timestamp": report.doctor_approval_timestamp if hasattr(report, 'doctor_approval_timestamp') else None,
        "hemoglobin": report.hemoglobin,
        "wbc": report.wbc,
        "platelets": report.platelets,
        "rbc": report.rbc,
        "patient": {
            "id": patient.id,
            "full_name": patient.full_name,
            "email": patient.email,
        },
        "sharing": {
            "id": sharing.id,
            "status": sharing.status,
            "patient_message": sharing.patient_message,
            "sent_at": sharing.sent_at,
            "created_at": sharing.created_at,
        }
    }
    
    return report_dict

@router.post("/reports/{report_id}/review", response_model=ReportResponse)
def review_report(
    report_id: int,
    review_data: ReportReview,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    Enhanced: Allows a doctor to review a report, approve/reject AI analysis, and add notes.
    Updates both the Report and ReportSharing records.
    """
    # Verify report is shared to this doctor
    sharing = db.query(ReportSharing).filter(
        ReportSharing.report_id == report_id,
        ReportSharing.doctor_id == current_doctor.id
    ).first()
    
    if sharing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found or not shared to this doctor"
        )
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

    # Update report with doctor's review
    report.doctor_id = current_doctor.id
    report.doctor_notes = review_data.doctor_notes
    report.review_status = review_data.review_status
    report.ai_approval_status = review_data.ai_approval_status
    report.doctor_approval_timestamp = datetime.utcnow()

    # Update sharing status
    sharing.status = "reviewed"
    sharing.reviewed_at = datetime.utcnow()

    db.add(report)
    db.add(sharing)
    db.commit()
    db.refresh(report)
    
    # Notify patient (async notification)
    try:
        notify_patient_doctor_review(report_id, report.user_id)
    except Exception as e:
        print(f"Warning: Failed to send notification: {e}")

    return report

@router.get("/reports/reviewed")
def get_reviewed_reports(
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """
    Get all reports reviewed by the current doctor.
    """
    sharings = db.query(ReportSharing).filter(
        ReportSharing.doctor_id == current_doctor.id,
        ReportSharing.status == "reviewed"
    ).order_by(ReportSharing.reviewed_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for sharing in sharings:
        report = db.query(Report).filter(Report.id == sharing.report_id).first()
        patient = db.query(User).filter(User.id == sharing.patient_id).first()
        
        if report and patient:
            result.append({
                "report": {
                    "id": report.id,
                    "report_name": report.report_name,
                    "review_status": report.review_status,
                    "ai_approval_status": report.ai_approval_status if hasattr(report, 'ai_approval_status') else "pending",
                    "doctor_approval_timestamp": report.doctor_approval_timestamp if hasattr(report, 'doctor_approval_timestamp') else None,
                },
                "patient": {
                    "id": patient.id,
                    "full_name": patient.full_name,
                    "email": patient.email,
                },
                "reviewed_at": sharing.reviewed_at,
            })
    
    return result

@router.get("/profile", response_model=DoctorResponse)
def get_doctor_profile(
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    Get current doctor's profile with hospital information.
    """
    return current_doctor
