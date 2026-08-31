import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies.vapi_auth import verify_vapi_webhook
from app.services.vapi_service import VapiWebhookPayload, VapiService
from app.services.llm_service import LLMService
from app.services.crm_service import CRMService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/vapi", tags=["Vapi Webhook"])


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def handle_vapi_webhook(
    payload: VapiWebhookPayload,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_vapi_webhook),
):
    """
    Receive Vapi webhook events (e.g. end-of-call-report),
    validate payload, extract structured LLM insights via Groq,
    and persist Lead, Call, and FollowUp records in a single DB transaction.
    """
    logger.info("Received Vapi webhook event")
    
    parsed_data = VapiService.parse_end_of_call_report(payload)
    if not parsed_data.get("valid"):
        logger.warning(f"Invalid Vapi webhook payload: {parsed_data.get('reason')}")
        return {
            "status": "ignored",
            "message": f"Webhook event received but not processed: {parsed_data.get('reason')}",
        }

    event_type = parsed_data.get("event_type")
    # Process only end-of-call-report or generic call completion events
    if event_type and event_type != "end-of-call-report":
        logger.info(f"Received Vapi event type '{event_type}', acknowledging without CRM sync.")
        return {"status": "success", "message": f"Event {event_type} acknowledged."}

    transcript = parsed_data.get("transcript", "")
    phone_number = parsed_data.get("phone_number", "")
    caller_name = parsed_data.get("caller_name", "")

    logger.info(f"Processing transcript for call {parsed_data.get('call_id')} from {phone_number}")

    # 1. Call Groq LLM service to extract structured JSON insights
    llm_extraction = None
    try:
        llm_extraction = LLMService.extract_lead_insights(
            transcript=transcript,
            caller_phone=phone_number,
            caller_name=caller_name,
        )
    except Exception as e:
        logger.error(f"LLM extraction failed, proceeding with fallback rescue: {e}")

    # 2. Persist Lead, Call, and FollowUp via CRM service in a single DB transaction
    crm_result = CRMService.process_call_and_sync_crm(
        db=db,
        parsed_vapi_data=parsed_data,
        llm_extraction=llm_extraction,
    )

    logger.info(f"Vapi webhook successfully processed and synced to CRM: {crm_result}")

    return {
        "status": "success",
        "message": "Vapi webhook processed, LLM extracted, and CRM updated successfully",
        "call_id": parsed_data.get("call_id"),
        "crm_result": crm_result,
    }
