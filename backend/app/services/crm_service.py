import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session

from app.models.lead import Lead, LanguageEnum, LeadStatusEnum
from app.models.call import Call, QualificationScoreEnum
from app.models.follow_up import FollowUp
from app.schemas.llm_extraction import LLMExtractionResult

logger = logging.getLogger(__name__)


class CRMService:
    @staticmethod
    def process_call_and_sync_crm(
        db: Session,
        parsed_vapi_data: Dict[str, Any],
        llm_extraction: Optional[LLMExtractionResult] = None,
    ) -> Dict[str, Any]:
        """
        In a single DB transaction:
        1. Create or update Lead record (matched by phone number).
        2. Create Call record linked to lead.
        3. If qualification is 'hot' or 'warm', auto-create a FollowUp record scheduled 24 hours later.
        4. Handle fallback/needing review records if LLM extraction is missing or failed.
        """
        phone = parsed_vapi_data.get("phone_number", "Unknown")
        caller_name = parsed_vapi_data.get("caller_name", "Unknown Caller")
        transcript = parsed_vapi_data.get("transcript", "")
        summary = parsed_vapi_data.get("summary", "")
        duration = parsed_vapi_data.get("duration_seconds", 0.0)
        call_id = parsed_vapi_data.get("call_id")

        try:
            # 1. Determine Lead details from LLM extraction or Vapi payload
            if llm_extraction:
                lead_name = llm_extraction.leadName if llm_extraction.leadName != "Unknown" else caller_name
                lead_phone = llm_extraction.phone if llm_extraction.phone else phone
                lang_str = llm_extraction.language.lower()
                language = LanguageEnum.urdu if "urdu" in lang_str else LanguageEnum.english
                
                # Map LLM qualification to Lead status and Call score
                qual_lower = llm_extraction.qualification.lower()
                if qual_lower == "hot":
                    lead_status = LeadStatusEnum.hot
                    call_score = QualificationScoreEnum.hot
                elif qual_lower == "warm":
                    lead_status = LeadStatusEnum.warm
                    call_score = QualificationScoreEnum.warm
                else:
                    lead_status = LeadStatusEnum.cold
                    call_score = QualificationScoreEnum.cold
                
                call_summary = llm_extraction.summary or summary
            else:
                # Fallback when LLM extraction failed
                lead_name = caller_name
                lead_phone = phone
                language = LanguageEnum.english
                lead_status = LeadStatusEnum.new
                call_score = QualificationScoreEnum.warm
                call_summary = summary or "[Needs Review - LLM Extraction Failed]"

            # Normalize phone for lookup
            if not lead_phone or lead_phone == "Unknown":
                lead_phone = "+923000000000"

            # 2. Check if Lead already exists by phone number (prevent duplicate leads)
            lead = db.query(Lead).filter(Lead.phone == lead_phone).first()

            if lead:
                # Update existing lead name/status if appropriate
                if lead_name and lead_name != "Unknown Caller":
                    lead.name = lead_name
                lead.status = lead_status
                lead.language = language
                db.flush()
            else:
                # Create new lead
                lead = Lead(
                    name=lead_name,
                    phone=lead_phone,
                    language=language,
                    status=lead_status,
                )
                db.add(lead)
                db.flush()  # flush to get lead.id

            # 3. Create Call record linked to lead
            call = Call(
                lead_id=lead.id,
                transcript=transcript,
                summary=call_summary,
                qualification_score=call_score,
                duration_seconds=int(duration),
                language=language,
            )
            db.add(call)

            # 4. If qualification is 'hot' or 'warm', auto-create a FollowUp record scheduled for 24 hours later
            follow_up_created = False
            if lead_status in [LeadStatusEnum.hot, LeadStatusEnum.warm]:
                scheduled_time = datetime.utcnow() + timedelta(hours=24)
                follow_up_notes = (
                    llm_extraction.followUpReason
                    if llm_extraction and llm_extraction.followUpReason
                    else f"Follow up with {lead_name} regarding recent inquiry."
                )
                
                follow_up = FollowUp(
                    lead_id=lead.id,
                    scheduled_for=scheduled_time,
                    notes=follow_up_notes,
                    completed=False,
                )
                db.add(follow_up)
                follow_up_created = True

            db.commit()
            db.refresh(lead)
            db.refresh(call)

            logger.info(f"Successfully processed CRM sync for call {call_id}, lead ID {lead.id}")
            return {
                "success": True,
                "lead_id": lead.id,
                "call_id": call.id,
                "lead_status": lead.status,
                "qualification": call_score,
                "follow_up_created": follow_up_created,
            }

        except Exception as e:
            db.rollback()
            logger.error(f"Error in CRM transaction processing: {e}")
            
            # Even if CRM transaction fails or LLM extraction errors, save raw Call record marked as needing review
            try:
                # Fallback rescue save
                fallback_lead = db.query(Lead).filter(Lead.phone == phone).first()
                if not fallback_lead:
                    fallback_lead = Lead(
                        name=caller_name,
                        phone=phone if phone and phone != "Unknown" else "+923000000000",
                        language=LanguageEnum.english,
                        status=LeadStatusEnum.new,
                    )
                    db.add(fallback_lead)
                    db.flush()

                rescue_call = Call(
                    lead_id=fallback_lead.id,
                    transcript=transcript,
                    summary=f"[ERROR/REVIEW REQUIRED] {summary} | Error: {str(e)}",
                    qualification_score=QualificationScoreEnum.warm,
                    duration_seconds=int(duration),
                    language=LanguageEnum.english,
                )
                db.add(rescue_call)
                db.commit()
                logger.warning(f"Saved rescue raw call record for call {call_id} due to CRM error.")
            except Exception as rescue_err:
                logger.error(f"Failed to save rescue call record: {rescue_err}")

            return {
                "success": False,
                "error": str(e),
            }
