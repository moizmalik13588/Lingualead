import json
import os
import sys

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal, engine
from app.models import Base
from app.services.vapi_service import VapiWebhookPayload, VapiService
from app.services.llm_service import LLMService
from app.services.crm_service import CRMService


def run_simulation():
    print("Starting Vapi Webhook & CRM Automation Simulation...\n")

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    fixtures_dir = os.path.join(os.path.dirname(__file__), "../tests/fixtures")
    fixture_files = ["vapi_call_english.json", "vapi_call_urdu.json"]

    for filename in fixture_files:
        filepath = os.path.join(fixtures_dir, filename)
        print(f"--- Processing Fixture: {filename} ---")
        
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        # 1. Parse payload into Pydantic model
        payload = VapiWebhookPayload(**raw_data)
        parsed_data = VapiService.parse_end_of_call_report(payload)
        print(f"Parsed Vapi Data: Call ID={parsed_data.get('call_id')}, Phone={parsed_data.get('phone_number')}, Name={parsed_data.get('caller_name')}")

        # 2. Extract LLM insights
        print("Extracting LLM structured insights...")
        llm_extraction = LLMService.extract_lead_insights(
            transcript=parsed_data.get("transcript", ""),
            caller_phone=parsed_data.get("phone_number", ""),
            caller_name=parsed_data.get("caller_name", ""),
        )
        print(f"LLM Result: Name={llm_extraction.leadName}, Qualification={llm_extraction.qualification}, Language={llm_extraction.language}")
        print(f"Summary: {llm_extraction.summary}")
        print(f"Follow-up Reason: {llm_extraction.followUpReason}")

        # 3. Sync to CRM
        print("Syncing to CRM database...")
        crm_result = CRMService.process_call_and_sync_crm(
            db=db,
            parsed_vapi_data=parsed_data,
            llm_extraction=llm_extraction,
        )
        print(f"CRM Result: {crm_result}\n")

    db.close()
    print("Simulation completed successfully! All test fixtures processed and saved to database.")


if __name__ == "__main__":
    run_simulation()
