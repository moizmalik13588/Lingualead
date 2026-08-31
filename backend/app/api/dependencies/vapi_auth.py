from typing import Optional
from fastapi import Header, HTTPException, Request, status
from app.core.config import settings
from app.services.vapi_service import VapiService


async def verify_vapi_webhook(
    request: Request,
    x_vapi_secret: Optional[str] = Header(None, alias="X-Vapi-Secret"),
    x_vapi_signature: Optional[str] = Header(None, alias="X-Vapi-Signature"),
) -> bool:
    """
    FastAPI dependency to verify Vapi webhook signature/secret.
    Rejects unauthorized requests with 401/403.
    """
    if not settings.VAPI_WEBHOOK_SECRET:
        return True

    signature = x_vapi_secret or x_vapi_signature
    body = await request.body()

    is_valid = VapiService.verify_signature(signature, body, settings.VAPI_WEBHOOK_SECRET)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Vapi webhook signature/secret",
        )
    return True
