
import os
import sys
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from dependencies import get_db, get_current_user
from models.user import User
from models.report import Report
from models.forecast import Forecast
from schemas.forecast import ForecastCreate, ForecastResponse
from services.forecasting_service import generate_forecast

router = APIRouter()

@router.post("/{report_id}/predict", response_model=ForecastResponse, status_code=status.HTTP_201_CREATED)
def generate_forecast_for_report(
    report_id: int,
    forecast_type: str = Query("health_trends", description="Type of forecast: health_trends, risk_assessment, recommendations"),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a health forecast for a specific report using patient's historical data.
    Requires authentication (patient or doctor can access).
    """
    # Get current report
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    
    # Verify access: patient owns report, or doctor has reviewed it
    if current_user and hasattr(current_user, 'id'):
        if report.user_id != current_user.id:
            # Check if doctor has reviewed this report
            from models.report_sharing import ReportSharing
            sharing = db.query(ReportSharing).filter(
                ReportSharing.report_id == report_id
            ).first()
            if not sharing:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to generate forecast for this report"
                )
    
    # Check if forecast already exists and is not expired
    existing_forecast = db.query(Forecast).filter(
        Forecast.report_id == report_id,
        Forecast.forecast_type == forecast_type,
        Forecast.expires_at > datetime.utcnow()
    ).first()
    
    if existing_forecast:
        return existing_forecast
    
    # Get historical reports for the patient
    historical_reports = db.query(Report).filter(
        Report.user_id == report.user_id,
        Report.id != report_id,
        Report.upload_timestamp < report.upload_timestamp
    ).order_by(Report.upload_timestamp.asc()).all()
    
    # Convert reports to dict format
    historical_data = []
    for hist_report in historical_reports:
        historical_data.append({
            "id": hist_report.id,
            "upload_timestamp": hist_report.upload_timestamp,
            "hemoglobin": hist_report.hemoglobin,
            "wbc": hist_report.wbc,
            "platelets": hist_report.platelets,
            "rbc": hist_report.rbc,
            "analysis_result_json": hist_report.analysis_result_json,
        })
    
    # Current report data
    current_report_data = {
        "id": report.id,
        "upload_timestamp": report.upload_timestamp,
        "hemoglobin": report.hemoglobin,
        "wbc": report.wbc,
        "platelets": report.platelets,
        "rbc": report.rbc,
        "analysis_result_json": report.analysis_result_json,
    }
    
    # Generate forecast
    forecast_result = generate_forecast(
        patient_id=str(report.user_id),
        current_report=current_report_data,
        historical_reports=historical_data
    )
    
    # Create forecast record
    forecast = Forecast(
        report_id=report_id,
        patient_id=report.user_id,
        forecast_type=forecast_type,
        forecast_data=forecast_result["forecast_data"],
        confidence_score=forecast_result["confidence_score"],
        expires_at=datetime.utcnow() + timedelta(days=90)
    )
    
    db.add(forecast)
    db.commit()
    db.refresh(forecast)
    
    return forecast

@router.get("/{report_id}", response_model=ForecastResponse)
def get_forecast_for_report(
    report_id: int,
    forecast_type: Optional[str] = Query(None, description="Type of forecast"),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get existing forecast for a report.
    """
    report = db.query(Report).filter(Report.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    
    # Verify access
    if current_user and hasattr(current_user, 'id'):
        if report.user_id != current_user.id:
            from models.report_sharing import ReportSharing
            sharing = db.query(ReportSharing).filter(
                ReportSharing.report_id == report_id
            ).first()
            if not sharing:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to access this forecast"
                )
    
    query = db.query(Forecast).filter(
        Forecast.report_id == report_id,
        Forecast.expires_at > datetime.utcnow()
    )
    
    if forecast_type:
        query = query.filter(Forecast.forecast_type == forecast_type)
    
    forecast = query.order_by(Forecast.created_at.desc()).first()
    
    if forecast is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No valid forecast found for this report"
        )
    
    return forecast

@router.get("/patient/{patient_id}/trends")
def get_patient_forecast_trends(
    patient_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all forecasts for a patient to analyze trends.
    Only accessible by the patient themselves.
    """
    if not current_user or current_user.id != patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own forecast trends"
        )
    
    forecasts = db.query(Forecast).filter(
        Forecast.patient_id == patient_id,
        Forecast.expires_at > datetime.utcnow()
    ).order_by(Forecast.created_at.desc()).all()
    
    return forecasts

