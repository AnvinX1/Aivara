
import os
import sys # Added
import json

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from dependencies import get_db, get_current_user
from models.user import User
from models.report import Report
from schemas.report import ReportCreate, ReportResponse
from services.ocr_service import extract_text_from_report
from services.parser_service import parse_health_markers
from services.ai_engine import analyze_health_markers
from services.storage_service import save_report_file

router = APIRouter()

@router.post("/upload", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def upload_report(
    report_name: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Uploads a new report, processes it, and stores the data.
    """
    if not file.filename.endswith(('.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and image files are allowed.")

    try:
        file_location = save_report_file(file, current_user.id)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        extracted_text = extract_text_from_report(file_location)
    except Exception as e:
        os.remove(file_location)
        raise HTTPException(status_code=500, detail=f"OCR failed: {e}")

    health_markers = parse_health_markers(extracted_text)
    analysis_results = analyze_health_markers(health_markers)

    db_report = Report(
        user_id=current_user.id,
        report_name=report_name,
        file_path=file_location,
        analysis_result_json=json.dumps(analysis_results),
        hemoglobin=health_markers.get('hemoglobin'),
        wbc=health_markers.get('wbc'),
        platelets=health_markers.get('platelets'),
        rbc=health_markers.get('rbc')
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return db_report

@router.get("/", response_model=list[ReportResponse])
def get_user_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves all reports for the current authenticated user.
    """
    reports = db.query(Report).filter(Report.user_id == current_user.id).all()
    return reports

@router.get("/{report_id}", response_model=ReportResponse)
def get_report_by_id(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves a specific report by its ID for the current authenticated user.
    """
    report = db.query(Report).filter(Report.id == report_id, Report.user_id == current_user.id).first()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return report
