import os
import sys
from datetime import datetime, timedelta

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal, engine
from app.models import Base
from app.models.lead import Lead, LanguageEnum, LeadStatusEnum
from app.models.call import Call, QualificationScoreEnum
from app.models.follow_up import FollowUp


def seed_database(reset: bool = False):
    print("Seeding LinguaLead database with demo data...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if reset or "--reset" in sys.argv:
        print("Resetting database (clearing existing leads, calls, follow-ups)...")
        db.query(FollowUp).delete()
        db.query(Call).delete()
        db.query(Lead).delete()
        db.commit()

    demo_leads_data = [
        {
            "name": "Sarah Jenkins",
            "phone": "+14155552671",
            "language": LanguageEnum.english,
            "status": LeadStatusEnum.hot,
            "calls": [
                {
                    "transcript": "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? Sarah: Hi, English please. I'm extremely interested in deploying your AI voice calling agent for our real estate firm across 3 offices. We need inbound lead qualification ready to start immediately this week. Budget is $6,500, timeline is urgent within 5 days.",
                    "summary": "Sarah Jenkins wants AI voice calling agent for real estate firm across 3 offices. High budget $6,500, urgent timeline within 5 days.",
                    "qualification_score": QualificationScoreEnum.hot,
                    "duration_seconds": 85,
                    "language": LanguageEnum.english,
                    "hours_ago": 2,
                }
            ],
            "follow_ups": [
                {
                    "notes": "Send enterprise contract and schedule onboarding call with Sarah Jenkins.",
                    "scheduled_hours_from_now": 22,
                    "completed": False,
                }
            ]
        },
        {
            "name": "Ahmed Raza",
            "phone": "+923009876543",
            "language": LanguageEnum.urdu,
            "status": LeadStatusEnum.hot,
            "calls": [
                {
                    "transcript": "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? Ahmed Raza: Bhai Urdu mein baat karte hain. Mujhe apni chain of auto parts stores ke liye AI receptionist chahiye jo Urdu aur English dono mein 24/7 calls attend kare. Budget 6 lakh rupay mahina hai aur humein fauran agle do din mein setup chahiye.",
                    "summary": "Ahmed Raza wants bilingual AI receptionist for auto parts store chain in Urdu. High budget 600,000 PKR/month, urgent setup within 2 days.",
                    "qualification_score": QualificationScoreEnum.hot,
                    "duration_seconds": 110,
                    "language": LanguageEnum.urdu,
                    "hours_ago": 5,
                }
            ],
            "follow_ups": [
                {
                    "notes": "Call Ahmed Raza to finalize Urdu voice model configuration and payment terms.",
                    "scheduled_hours_from_now": 19,
                    "completed": False,
                }
            ]
        },
        {
            "name": "Michael Chang",
            "phone": "+14155558899",
            "language": LanguageEnum.english,
            "status": LeadStatusEnum.warm,
            "calls": [
                {
                    "transcript": "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? Michael: English. I'm exploring voice agents for customer support. We are evaluating options for Q3. Budget is around $1,500 monthly.",
                    "summary": "Michael Chang exploring voice agents for customer support, evaluating for Q3 with $1.5k/mo budget.",
                    "qualification_score": QualificationScoreEnum.warm,
                    "duration_seconds": 54,
                    "language": LanguageEnum.english,
                    "hours_ago": 26,
                }
            ],
            "follow_ups": [
                {
                    "notes": "Send case studies on customer support AI automation.",
                    "scheduled_hours_from_now": 12,
                    "completed": False,
                }
            ]
        },
        {
            "name": "Fatima Noor",
            "phone": "+923214567890",
            "language": LanguageEnum.urdu,
            "status": LeadStatusEnum.warm,
            "calls": [
                {
                    "transcript": "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? Fatima Noor: Jee Urdu. Main ek clinic chala rahi hoon, appointment booking ke liye koi system chahiye. Price thoda zyaada lag raha hai lekin soch sakti hoon.",
                    "summary": "Fatima Noor interested in appointment booking AI for clinic in Urdu. Price hesitant but considering.",
                    "qualification_score": QualificationScoreEnum.warm,
                    "duration_seconds": 68,
                    "language": LanguageEnum.urdu,
                    "hours_ago": 48,
                }
            ],
            "follow_ups": [
                {
                    "notes": "Follow up with Fatima regarding clinic discount package.",
                    "scheduled_hours_from_now": 36,
                    "completed": False,
                }
            ]
        },
        {
            "name": "David Smith",
            "phone": "+14155551122",
            "language": LanguageEnum.english,
            "status": LeadStatusEnum.cold,
            "calls": [
                {
                    "transcript": "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? David: Just checking out what your pricing is. Not sure if we need this right now. Maybe next year.",
                    "summary": "David Smith browsing pricing, no immediate need, perhaps next year.",
                    "qualification_score": QualificationScoreEnum.cold,
                    "duration_seconds": 32,
                    "language": LanguageEnum.english,
                    "hours_ago": 72,
                }
            ],
            "follow_ups": []
        },
        {
            "name": "Zainab Malik",
            "phone": "+923337778899",
            "language": LanguageEnum.urdu,
            "status": LeadStatusEnum.cold,
            "calls": [
                {
                    "transcript": "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? Zainab: Hello, mujhe thori information chahiye thi. (Call disconnected before details).",
                    "summary": "Zainab Malik called for inquiry but call disconnected early.",
                    "qualification_score": QualificationScoreEnum.cold,
                    "duration_seconds": 15,
                    "language": LanguageEnum.urdu,
                    "hours_ago": 1,
                }
            ],
            "follow_ups": []
        }
    ]

    for lead_data in demo_leads_data:
        existing_lead = db.query(Lead).filter(Lead.phone == lead_data["phone"]).first()
        if existing_lead:
            print(f"Updating existing lead: {lead_data['name']}...")
            existing_lead.name = lead_data["name"]
            existing_lead.language = lead_data["language"]
            existing_lead.status = lead_data["status"]
            lead = existing_lead
            # Clear old calls for clean seeding
            db.query(Call).filter(Call.lead_id == lead.id).delete()
            db.query(FollowUp).filter(FollowUp.lead_id == lead.id).delete()
        else:
            print(f"Creating new lead: {lead_data['name']}...")
            lead = Lead(
                name=lead_data["name"],
                phone=lead_data["phone"],
                language=lead_data["language"],
                status=lead_data["status"],
                created_at=datetime.utcnow() - timedelta(hours=30),
            )
            db.add(lead)
            db.flush()

        for call_data in lead_data["calls"]:
            call = Call(
                lead_id=lead.id,
                transcript=call_data["transcript"],
                summary=call_data["summary"],
                qualification_score=call_data["qualification_score"],
                duration_seconds=call_data["duration_seconds"],
                language=call_data["language"],
                created_at=datetime.utcnow() - timedelta(hours=call_data["hours_ago"]),
            )
            db.add(call)

        for fu_data in lead_data["follow_ups"]:
            fu = FollowUp(
                lead_id=lead.id,
                scheduled_for=datetime.utcnow() + timedelta(hours=fu_data["scheduled_hours_from_now"]),
                notes=fu_data["notes"],
                completed=fu_data["completed"],
            )
            db.add(fu)

    db.commit()
    db.close()
    print("Demo data successfully seeded into database with guaranteed Hot leads!")


if __name__ == "__main__":
    reset_flag = "--reset" in sys.argv
    seed_database(reset=reset_flag)
