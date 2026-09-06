import os
import sys

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.models.lead import Lead, LeadStatusEnum
from app.models.call import Call


def backfill_lead_status():
    print("Starting Lead.status backfill based on most recent call qualification...")
    db = SessionLocal()

    try:
        leads = db.query(Lead).all()
        updated_count = 0

        for lead in leads:
            # Find the most recent call for this lead
            latest_call = (
                db.query(Call)
                .filter(Call.lead_id == lead.id)
                .order_by(Call.created_at.desc())
                .first()
            )

            if latest_call and latest_call.qualification_score:
                score_str = latest_call.qualification_score.value.lower()
                if score_str == "hot":
                    new_status = LeadStatusEnum.hot
                elif score_str == "warm":
                    new_status = LeadStatusEnum.warm
                else:
                    new_status = LeadStatusEnum.cold

                if lead.status != new_status:
                    print(f"Updating Lead '{lead.name}' (ID: {lead.id}) status from '{lead.status}' to '{new_status}' (based on latest call ID {latest_call.id})")
                    lead.status = new_status
                    updated_count += 1

        db.commit()
        print(f"Backfill complete! Updated status for {updated_count} lead(s).")

    except Exception as e:
        db.rollback()
        print(f"Error during Lead.status backfill: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    backfill_lead_status()
