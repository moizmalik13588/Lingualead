from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FollowUpBase(BaseModel):
    lead_id: int
    scheduled_for: datetime
    notes: Optional[str] = None
    completed: bool = False


class FollowUpCreate(FollowUpBase):
    pass


class FollowUpUpdate(BaseModel):
    scheduled_for: Optional[datetime] = None
    notes: Optional[str] = None
    completed: Optional[bool] = None


class FollowUpResponse(FollowUpBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
