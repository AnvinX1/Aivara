
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from db.database import Base

class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    forecast_type = Column(String, default="health_trends")  # health_trends, risk_assessment, recommendations
    forecast_data = Column(Text, nullable=False)  # JSON string with LLM-generated forecast
    confidence_score = Column(Float, default=0.0)  # 0.0 to 1.0
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=90))  # 90 days validity

    # Relationships
    report = relationship("Report")
    patient = relationship("User")

    def __repr__(self):
        return f"<Forecast(id={self.id}, report_id={self.report_id}, forecast_type='{self.forecast_type}', confidence={self.confidence_score})>"

