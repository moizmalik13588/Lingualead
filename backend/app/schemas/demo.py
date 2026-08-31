from typing import Optional
from pydantic import BaseModel, Field


class SimulateCallRequest(BaseModel):
    language: str = Field("english", description="Language of simulation: 'english' or 'urdu'")
    transcript: Optional[str] = Field(None, description="Optional custom transcript text")
    caller_name: Optional[str] = Field(None, description="Optional custom caller name")
    caller_phone: Optional[str] = Field(None, description="Optional custom caller phone number")
    summary: Optional[str] = Field(None, description="Optional custom call summary")
