
import os
import sys # Added
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from dependencies import get_db, get_current_user
from models.user import User
from models.report import Report
from schemas.report import ReportResponse
from services.ocr_service import extract_text_from_report
from services.parser_service import parse_health_markers
from services.ai_engine import analyze_health_markers

router = APIRouter()

@router.post("/analyze/{report_id}", response_model=ReportResponse)
def reanalyze_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Re-runs AI analysis for a specific report owned by the current user and updates the stored results.
    """
    report = db.query(Report).filter(Report.id == report_id, Report.user_id == current_user.id).first()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found or not owned by user")

    try:
        extracted_text = extract_text_from_report(report.file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed during re-analysis: {e}")

    health_markers = parse_health_markers(extracted_text)
    analysis_results = analyze_health_markers(health_markers)

    report.analysis_result_json = json.dumps(analysis_results)
    report.hemoglobin = health_markers.get('hemoglobin')
    report.wbc = health_markers.get('wbc')
    report.platelets = health_markers.get('platelets')
    report.rbc = health_markers.get('rbc')

    db.add(report)
    db.commit()
    db.refresh(report)

    return report
