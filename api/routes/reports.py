
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
from services.text_chunking_service import chunk_text_for_vector_store
from app.services.vector_store import upsert_docs

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

    # Create report in database first to get report ID for vector store
    db_report = Report(
        user_id=current_user.id,
        report_name=report_name,
        file_path=file_location,
        hemoglobin=health_markers.get('hemoglobin'),
        wbc=health_markers.get('wbc'),
        platelets=health_markers.get('platelets'),
        rbc=health_markers.get('rbc')
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    # Store extracted text in vector store (with error handling - don't fail upload if this fails)
    try:
        # Chunk the extracted text for vector storage
        chunks = chunk_text_for_vector_store(
            text=extracted_text,
            report_id=db_report.id,
            patient_id=str(current_user.id),
            report_name=report_name,
            upload_timestamp=db_report.upload_timestamp.isoformat() if db_report.upload_timestamp else None
        )
        
        if chunks:
            # Store chunks in ChromaDB
            upsert_docs(chunks)
            print(f"Successfully stored {len(chunks)} chunks for report {db_report.id} in vector store.")
        else:
            print(f"Warning: No chunks created for report {db_report.id}.")
    except Exception as e:
        # Log error but don't fail the upload if vectorization fails
        print(f"Warning: Failed to store report {db_report.id} in vector store: {e}")
        # Continue with analysis even if vectorization failed

    # Analyze health markers with RAG context (if available)
    # Generate query from markers for context retrieval
    marker_query_parts = []
    for marker, value in health_markers.items():
        if value is not None:
            marker_query_parts.append(f"{marker.replace('_', ' ')} {value}")
    
    query = None
    if marker_query_parts:
        query = f"Previous reports with {', '.join(marker_query_parts)}"
    
    # Perform analysis with RAG context
    analysis_results = analyze_health_markers(
        markers=health_markers,
        patient_id=str(current_user.id),
        query=query
    )

    # Update report with analysis results
    db_report.analysis_result_json = json.dumps(analysis_results)
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
