
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    report_name = Column(String, index=True, nullable=False)
    file_path = Column(String, nullable=False)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    analysis_result_json = Column(Text)
    doctor_notes = Column(Text)
    review_status = Column(String, default="pending") # e.g., 'pending', 'reviewed'

    # Extracted Health Markers
    hemoglobin = Column(Float)
    wbc = Column(Float)
    platelets = Column(Float)
    rbc = Column(Float)

    owner = relationship("User", back_populates="reports")
    doctor = relationship("Doctor", back_populates="reviewed_reports")

    def __repr__(self):
        return f"<Report(id={self.id}, report_name='{self.report_name}', user_id={self.user_id})>"
