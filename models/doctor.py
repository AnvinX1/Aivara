
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    specialization = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    reviewed_reports = relationship("Report", back_populates="doctor")

    def __repr__(self):
        return f"<Doctor(id={self.id}, email='{self.email}')>"
