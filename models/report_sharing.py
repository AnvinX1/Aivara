
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class ReportSharing(Base):
    __tablename__ = "report_sharings"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    status = Column(String, default="pending", index=True)  # pending, sent, under_review, reviewed, rejected
    patient_message = Column(Text, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    report = relationship("Report", foreign_keys=[report_id])
    patient = relationship("User", foreign_keys=[patient_id])
    doctor = relationship("Doctor", foreign_keys=[doctor_id])

    def __repr__(self):
        return f"<ReportSharing(id={self.id}, report_id={self.report_id}, doctor_id={self.doctor_id}, status='{self.status}')>"

