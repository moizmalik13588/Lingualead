import os
import sys

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal, engine
from app.models.lead import Lead
from app.models.follow_up import FollowUp


def deduplicate_followups():
    print("Starting follow-up deduplication cleanup...")
    db = SessionLocal()

    try:
        leads = db.query(Lead).all()
        total_removed = 0

        for lead in leads:
            # Get all incomplete follow-ups for this lead
            incomplete_fus = (
                db.query(FollowUp)
                .filter(FollowUp.lead_id == lead.id, FollowUp.completed == False)
                .order_by(FollowUp.created_at.desc())
                .all()
            )

            if len(incomplete_fus) > 1:
                print(f"Lead '{lead.name}' (ID: {lead.id}) has {len(incomplete_fus)} incomplete follow-ups. Cleaning up duplicates...")
                # Keep the first (most recently created) and delete the rest
                keep_fu = incomplete_fus[0]
                duplicates = incomplete_fus[1:]

                for dup in duplicates:
                    print(f"  Deleting duplicate follow-up ID {dup.id} (scheduled: {dup.scheduled_for})")
                    db.delete(dup)
                    total_removed += 1

        db.commit()
        print(f"Deduplication complete! Removed {total_removed} duplicate follow-up record(s).")

    except Exception as e:
        db.rollback()
        print(f"Error during follow-up deduplication: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    deduplicate_followups()
