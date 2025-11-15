
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ForecastCreate(BaseModel):
    report_id: int
    forecast_type: str = "health_trends"  # health_trends, risk_assessment, recommendations
    forecast_data: str  # JSON string
    confidence_score: float = Field(..., ge=0.0, le=1.0)

class ForecastResponse(BaseModel):
    id: int
    report_id: int
    patient_id: int
    forecast_type: str
    forecast_data: str
    confidence_score: float
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True

