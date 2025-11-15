
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ReportSharingCreate(BaseModel):
    doctor_id: int
    patient_message: Optional[str] = None

class ReportSharingResponse(BaseModel):
    id: int
    report_id: int
    patient_id: int
    doctor_id: int
    status: str
    patient_message: Optional[str] = None
    sent_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

