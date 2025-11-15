
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
from services.text_chunking_service import chunk_text_for_vector_store
from app.services.vector_store import upsert_docs

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

    # Store/update extracted text in vector store (upsert handles updates)
    try:
        # Chunk the extracted text for vector storage
        chunks = chunk_text_for_vector_store(
            text=extracted_text,
            report_id=report.id,
            patient_id=str(report.user_id),
            report_name=report.report_name,
            upload_timestamp=report.upload_timestamp.isoformat() if report.upload_timestamp else None
        )
        
        if chunks:
            # Store/update chunks in ChromaDB (upsert handles existing chunks)
            upsert_docs(chunks)
            print(f"Successfully stored/updated {len(chunks)} chunks for report {report.id} in vector store.")
        else:
            print(f"Warning: No chunks created for report {report.id} during re-analysis.")
    except Exception as e:
        # Log error but don't fail re-analysis if vectorization fails
        print(f"Warning: Failed to store/update report {report.id} in vector store during re-analysis: {e}")

    # Generate query from markers for RAG context retrieval
    marker_query_parts = []
    for marker, value in health_markers.items():
        if value is not None:
            marker_query_parts.append(f"{marker.replace('_', ' ')} {value}")
    
    query = None
    if marker_query_parts:
        query = f"Previous reports with {', '.join(marker_query_parts)}"

    # Perform analysis with RAG context (if available)
    analysis_results = analyze_health_markers(
        markers=health_markers,
        patient_id=str(report.user_id),
        query=query
    )

    # Update report with new analysis results
    report.analysis_result_json = json.dumps(analysis_results)
    report.hemoglobin = health_markers.get('hemoglobin')
    report.wbc = health_markers.get('wbc')
    report.platelets = health_markers.get('platelets')
    report.rbc = health_markers.get('rbc')

    db.add(report)
    db.commit()
    db.refresh(report)

    return report
