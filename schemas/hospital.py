
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class HospitalBase(BaseModel):
    name: str
    address: str
    city: str
    state: str
    pincode: str = Field(..., min_length=6, max_length=6)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class HospitalCreate(HospitalBase):
    pass

class HospitalResponse(HospitalBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

