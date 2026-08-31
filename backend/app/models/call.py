import enum
from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, Index
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.lead import LanguageEnum


class QualificationScoreEnum(str, enum.Enum):
    hot = "hot"
    warm = "warm"
    cold = "cold"


class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    qualification_score = Column(Enum(QualificationScoreEnum), nullable=True)
    duration_seconds = Column(Integer, default=0, nullable=False)
    language = Column(Enum(LanguageEnum), default=LanguageEnum.english, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)

    # Relationships
    lead = relationship("Lead", back_populates="calls")

    __table_args__ = (
        Index("idx_call_lead_id", "lead_id"),
        Index("idx_call_created_at", "created_at"),
    )
