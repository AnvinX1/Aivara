
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, write_only=True)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    hashed_password: str

class DoctorBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    specialization: str | None = None

class DoctorCreate(DoctorBase):
    password: str = Field(..., min_length=8, write_only=True)
    hospital_id: int | None = None
    phone: str | None = None
    registration_number: str | None = None

class DoctorResponse(DoctorBase):
    id: int
    hospital_id: int | None = None
    phone: str | None = None
    registration_number: str | None = None
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True
