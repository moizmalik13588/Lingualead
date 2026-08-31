from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.lead import LanguageEnum
from app.models.call import QualificationScoreEnum


class CallBase(BaseModel):
    lead_id: int
    transcript: Optional[str] = None
    summary: Optional[str] = None
    qualification_score: Optional[QualificationScoreEnum] = None
    duration_seconds: int = Field(default=0, ge=0)
    language: LanguageEnum = Field(default=LanguageEnum.english)


class CallCreate(CallBase):
    pass


class CallResponse(CallBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
