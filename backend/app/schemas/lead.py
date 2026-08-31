from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.lead import LanguageEnum, LeadStatusEnum


class LeadBase(BaseModel):
    name: str = Field(..., example="Ali Khan")
    phone: str = Field(..., example="+923001234567")
    language: LanguageEnum = Field(default=LanguageEnum.english)
    status: LeadStatusEnum = Field(default=LeadStatusEnum.new)


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[LanguageEnum] = None
    status: Optional[LeadStatusEnum] = None


class LeadResponse(LeadBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
