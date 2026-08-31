import logging
import time
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.demo import SimulateCallRequest
from app.services.llm_service import LLMService
from app.services.crm_service import CRMService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/demo", tags=["Demo Simulator"])

# Simple in-memory rate limiter store: {client_ip: timestamp}
_rate_limit_store = {}


@router.post("/simulate-call", status_code=status.HTTP_200_OK)
async def simulate_call(
    payload: SimulateCallRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Simulate an inbound AI voice call for the in-app demo simulator.
    Does not require Vapi signature verification.
    Runs LLM extraction and CRM automation, marking records as simulated.
    """
    # Basic rate limiting (max 1 request every 2 seconds per IP)
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    last_time = _rate_limit_store.get(client_ip, 0.0)
    if now - last_time < 2.0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many simulation requests. Please wait a moment before trying again."
        )
    _rate_limit_store[client_ip] = now

    lang = (payload.language or "english").lower()

    # Default demo fixtures
    if "urdu" in lang:
        default_name = "Bilal Ahmed"
        default_phone = "+923005554433"
        default_transcript = (
            "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? "
            "Bilal: Urdu mein baat karte hain. Mujhe software development outsourced karni hai apni company ke liye. "
            "Budget around 300k PKR hai aur timeline next month hai."
        )
        default_summary = "Bilal Ahmed wants software development services in Urdu. Budget 300k PKR, timeline next month."
        default_duration = 72
    else:
        default_name = "Jessica Taylor"
        default_phone = "+14155559988"
        default_transcript = (
            "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? "
            "Jessica: Hi, English. We are looking for an AI voice sales agent for our e-commerce store. "
            "Very interested, budget is $5,000, need it by end of week."
        )
        default_summary = "Jessica Taylor interested in AI voice sales agent for e-commerce store. Budget $5k, urgent timeline end of week."
        default_duration = 58

    caller_name = payload.caller_name or default_name
    caller_phone = payload.caller_phone or default_phone
    transcript = payload.transcript or default_transcript
    summary = payload.summary or default_summary

    call_id = f"call-demo-{int(time.time() * 1000)}"

    # Mark records clearly as demo / simulated
    marked_caller_name = f"[Demo] {caller_name}" if not caller_name.startswith("[Demo]") else caller_name

    parsed_vapi_data = {
        "valid": True,
        "event_type": "end-of-call-report",
        "call_id": call_id,
        "phone_number": caller_phone,
        "caller_name": marked_caller_name,
        "transcript": transcript,
        "summary": f"[Simulated Demo] {summary}",
        "duration_seconds": default_duration,
    }

    logger.info(f"Running simulated demo call for {caller_phone} ({lang})")

    # 1. LLM Extraction
    llm_extraction = None
    try:
        llm_extraction = LLMService.extract_lead_insights(
            transcript=transcript,
            caller_phone=caller_phone,
            caller_name=marked_caller_name,
        )
        if llm_extraction and llm_extraction.leadName and not llm_extraction.leadName.startswith("[Demo]"):
            llm_extraction.leadName = f"[Demo] {llm_extraction.leadName}"
    except Exception as e:
        logger.error(f"Demo LLM extraction failed: {e}")

    # 2. CRM Sync
    crm_result = CRMService.process_call_and_sync_crm(
        db=db,
        parsed_vapi_data=parsed_vapi_data,
        llm_extraction=llm_extraction,
    )

    return {
        "status": "success",
        "message": "Simulated call processed and synced to CRM successfully",
        "call_id": call_id,
        "crm_result": crm_result,
    }
