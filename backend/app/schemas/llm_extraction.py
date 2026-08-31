from typing import Literal, Optional
from pydantic import BaseModel, Field


class LLMExtractionResult(BaseModel):
    leadName: str = Field(..., description="Extracted full name of the caller/lead")
    phone: str = Field(..., description="Extracted phone number of the caller")
    language: str = Field(..., description="Detected conversation language: urdu or english")
    interest: str = Field(..., description="What product, service, or solution the lead is interested in")
    budget: str = Field(..., description="Rough budget or price tier mentioned by lead")
    timeline: str = Field(..., description="Timeline or urgency for purchase/decision")
    qualification: Literal["hot", "warm", "cold"] = Field(..., description="Lead qualification score: hot, warm, or cold")
    summary: str = Field(..., description="Concise summary of the sales conversation")
    followUpReason: str = Field(..., description="Reason and action items for follow-up")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0 for the extraction")
