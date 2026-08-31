import enum
from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, Integer, String, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class LanguageEnum(str, enum.Enum):
    urdu = "urdu"
    english = "english"


class LeadStatusEnum(str, enum.Enum):
    new = "new"
    hot = "hot"
    warm = "warm"
    cold = "cold"
    follow_up = "follow_up"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, default="Unknown Caller")
    phone = Column(String, unique=True, index=True, nullable=False)
    language = Column(Enum(LanguageEnum), default=LanguageEnum.english, nullable=False)
    status = Column(Enum(LeadStatusEnum), default=LeadStatusEnum.new, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)

    # Relationships
    calls = relationship("Call", back_populates="lead", cascade="all, delete-orphan")
    follow_ups = relationship("FollowUp", back_populates="lead", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_lead_phone", "phone"),
        Index("idx_lead_created_at", "created_at"),
    )
