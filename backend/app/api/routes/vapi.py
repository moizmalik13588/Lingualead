import logging
from fastapi import APIRouter, Depends, status
from app.api.dependencies.vapi_auth import verify_vapi_webhook
from app.services.vapi_service import VapiWebhookPayload, VapiService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/vapi", tags=["Vapi Webhook"])


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def handle_vapi_webhook(
    payload: VapiWebhookPayload,
    _: bool = Depends(verify_vapi_webhook),
):
    """
    Receive Vapi webhook events (e.g. end-of-call-report),
    validate payload via Pydantic, verify signature, and log call details.
    """
    logger.info("Received Vapi webhook event")
    
    parsed_data = VapiService.parse_end_of_call_report(payload)
    
    logger.info(f"Vapi Webhook Parsed Data: {parsed_data}")
    print("\n--- VAPI WEBHOOK EVENT RECEIVED ---")
    print(f"Event Type: {parsed_data.get('event_type')}")
    print(f"Call ID: {parsed_data.get('call_id')}")
    print(f"Caller Phone: {parsed_data.get('phone_number')}")
    print(f"Caller Name: {parsed_data.get('caller_name')}")
    print(f"Duration: {parsed_data.get('duration_seconds')}s")
    print(f"Summary: {parsed_data.get('summary')}")
    print(f"Transcript: {parsed_data.get('transcript')}")
    print("------------------------------------\n")

    return {
        "status": "success",
        "message": "Vapi webhook processed successfully",
        "call_id": parsed_data.get("call_id"),
    }
