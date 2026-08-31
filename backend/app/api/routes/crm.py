import logging
from datetime import datetime, date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.models.lead import Lead, LanguageEnum, LeadStatusEnum
from app.models.call import Call, QualificationScoreEnum
from app.models.follow_up import FollowUp
from app.schemas.crm import (
    LeadListItem,
    LeadDetailOut,
    CallOut,
    FollowUpOut,
    DashboardStatsOut,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["CRM"])


@router.get("/leads", response_model=List[LeadListItem])
def get_leads(
    status: Optional[LeadStatusEnum] = None,
    language: Optional[LanguageEnum] = None,
    qualification: Optional[QualificationScoreEnum] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get all leads with optional filtering by status, language, qualification, or search query.
    """
    query = db.query(Lead)

    if status:
        query = query.filter(Lead.status == status)
    if language:
        query = query.filter(Lead.language == language)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Lead.name.ilike(search_term)) | (Lead.phone.ilike(search_term))
        )

    leads = query.order_by(Lead.created_at.desc()).all()

    result = []
    for lead in leads:
        # Get latest call info
        latest_call = (
            db.query(Call)
            .filter(Call.lead_id == lead.id)
            .order_by(Call.created_at.desc())
            .first()
        )
        total_calls = db.query(func.count(Call.id)).filter(Call.lead_id == lead.id).scalar() or 0

        if qualification and latest_call and latest_call.qualification_score != qualification:
            continue

        result.append(
            LeadListItem(
                id=lead.id,
                name=lead.name,
                phone=lead.phone,
                language=lead.language,
                status=lead.status,
                created_at=lead.created_at,
                last_call_at=latest_call.created_at if latest_call else None,
                total_calls=total_calls,
                latest_qualification=latest_call.qualification_score if latest_call else None,
            )
        )

    return result


@router.get("/leads/{lead_id}", response_model=LeadDetailOut)
def get_lead_detail(lead_id: int, db: Session = Depends(get_db)):
    """
    Get detailed lead information including calls history and follow-ups.
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

    calls = db.query(Call).filter(Call.lead_id == lead_id).order_by(Call.created_at.desc()).all()
    follow_ups = db.query(FollowUp).filter(FollowUp.lead_id == lead_id).order_by(FollowUp.scheduled_for.asc()).all()

    formatted_follow_ups = []
    for fu in follow_ups:
        formatted_follow_ups.append(
            FollowUpOut(
                id=fu.id,
                lead_id=fu.lead_id,
                scheduled_for=fu.scheduled_for,
                notes=fu.notes,
                completed=fu.completed,
                created_at=fu.created_at,
                lead_name=lead.name,
                lead_phone=lead.phone,
            )
        )

    return LeadDetailOut(
        id=lead.id,
        name=lead.name,
        phone=lead.phone,
        language=lead.language,
        status=lead.status,
        created_at=lead.created_at,
        calls=calls,
        follow_ups=formatted_follow_ups,
    )


@router.get("/followups", response_model=List[FollowUpOut])
def get_followups(
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    Get all follow-up tasks, optionally filtered by completion status.
    """
    query = db.query(FollowUp)
    if completed is not None:
        query = query.filter(FollowUp.completed == completed)

    follow_ups = query.order_by(FollowUp.scheduled_for.asc()).all()

    result = []
    for fu in follow_ups:
        lead = db.query(Lead).filter(Lead.id == fu.lead_id).first()
        result.append(
            FollowUpOut(
                id=fu.id,
                lead_id=fu.lead_id,
                scheduled_for=fu.scheduled_for,
                notes=fu.notes,
                completed=fu.completed,
                created_at=fu.created_at,
                lead_name=lead.name if lead else "Unknown",
                lead_phone=lead.phone if lead else "Unknown",
            )
        )

    return result


@router.patch("/followups/{follow_up_id}", response_model=FollowUpOut)
def update_followup(
    follow_up_id: int,
    completed: Optional[bool] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Update follow-up status (e.g. mark complete) or notes.
    """
    fu = db.query(FollowUp).filter(FollowUp.id == follow_up_id).first()
    if not fu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Follow-up not found")

    if completed is not None:
        fu.completed = completed
    if notes is not None:
        fu.notes = notes

    db.commit()
    db.refresh(fu)

    lead = db.query(Lead).filter(Lead.id == fu.lead_id).first()
    return FollowUpOut(
        id=fu.id,
        lead_id=fu.lead_id,
        scheduled_for=fu.scheduled_for,
        notes=fu.notes,
        completed=fu.completed,
        created_at=fu.created_at,
        lead_name=lead.name if lead else "Unknown",
        lead_phone=lead.phone if lead else "Unknown",
    )


@router.get("/dashboard/stats", response_model=DashboardStatsOut)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get summary stats for dashboard: total leads, hot leads, calls today, pending follow-ups, and recent calls.
    """
    total_leads = db.query(func.count(Lead.id)).scalar() or 0
    
    hot_leads_count = db.query(func.count(Lead.id)).filter(
        (Lead.status == LeadStatusEnum.hot)
    ).scalar() or 0

    today_start = datetime.combine(date.today(), datetime.min.time())
    calls_today_count = db.query(func.count(Call.id)).filter(
        Call.created_at >= today_start
    ).scalar() or 0

    pending_follow_ups_count = db.query(func.count(FollowUp.id)).filter(
        FollowUp.completed == False
    ).scalar() or 0

    recent_calls = db.query(Call).order_by(Call.created_at.desc()).limit(5).all()

    leads = db.query(Lead).order_by(Lead.created_at.desc()).limit(5).all()
    recent_leads = []
    for lead in leads:
        latest_call = (
            db.query(Call)
            .filter(Call.lead_id == lead.id)
            .order_by(Call.created_at.desc())
            .first()
        )
        total_calls = db.query(func.count(Call.id)).filter(Call.lead_id == lead.id).scalar() or 0
        recent_leads.append(
            LeadListItem(
                id=lead.id,
                name=lead.name,
                phone=lead.phone,
                language=lead.language,
                status=lead.status,
                created_at=lead.created_at,
                last_call_at=latest_call.created_at if latest_call else None,
                total_calls=total_calls,
                latest_qualification=latest_call.qualification_score if latest_call else None,
            )
        )

    return DashboardStatsOut(
        total_leads=total_leads,
        hot_leads_count=hot_leads_count,
        calls_today_count=calls_today_count,
        pending_follow_ups_count=pending_follow_ups_count,
        recent_calls=recent_calls,
        recent_leads=recent_leads,
    )
