from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.lead import LanguageEnum, LeadStatusEnum
from app.models.call import QualificationScoreEnum


class CallOut(BaseModel):
    id: int
    lead_id: int
    transcript: Optional[str] = None
    summary: Optional[str] = None
    qualification_score: Optional[QualificationScoreEnum] = None
    duration_seconds: int
    language: LanguageEnum
    created_at: datetime

    class Config:
        from_attributes = True


class FollowUpOut(BaseModel):
    id: int
    lead_id: int
    scheduled_for: datetime
    notes: Optional[str] = None
    completed: bool
    created_at: datetime
    lead_name: Optional[str] = Field(None, description="Lead name for display")
    lead_phone: Optional[str] = Field(None, description="Lead phone for display")

    class Config:
        from_attributes = True


class LeadListItem(BaseModel):
    id: int
    name: str
    phone: str
    language: LanguageEnum
    status: LeadStatusEnum
    created_at: datetime
    last_call_at: Optional[datetime] = None
    total_calls: int = 0
    latest_qualification: Optional[QualificationScoreEnum] = None

    class Config:
        from_attributes = True


class LeadDetailOut(BaseModel):
    id: int
    name: str
    phone: str
    language: LanguageEnum
    status: LeadStatusEnum
    created_at: datetime
    calls: List[CallOut] = []
    follow_ups: List[FollowUpOut] = []

    class Config:
        from_attributes = True


class DashboardStatsOut(BaseModel):
    total_leads: int
    hot_leads_count: int
    calls_today_count: int
    pending_follow_ups_count: int
    recent_calls: List[CallOut] = []
    recent_leads: List[LeadListItem] = []
