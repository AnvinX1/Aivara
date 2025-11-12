
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class ReportBase(BaseModel):
    report_name: str

class ReportCreate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int
    user_id: int
    doctor_id: int | None = None
    file_path: str
    upload_timestamp: datetime
    analysis_result_json: str | None = None
    doctor_notes: str | None = None
    review_status: str
    hemoglobin: float | None = None
    wbc: float | None = None
    platelets: float | None = None
    rbc: float | None = None

    class Config:
        from_attributes = True

class ReportReview(BaseModel):
    doctor_notes: str
    review_status: str # e.g., 'reviewed', 'pending'
