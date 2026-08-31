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


def seed_database():
    print("Seeding LinguaLead database with demo data...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data if any (optional, or check if already seeded)
    existing_leads_count = db.query(Lead).count()
    if existing_leads_count > 0:
        print(f"Database already has {existing_leads_count} leads. Appending demo data or skipping...")
        # Let's add demo leads if not present

    demo_leads_data = [
        {
            "name": "Sarah Jenkins",
            "phone": "+14155552671",
            "language": LanguageEnum.english,
            "status": LeadStatusEnum.hot,
            "calls": [
                {
                    "transcript": "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? Sarah: Hi, English please. I'm interested in your AI voice calling agent for our real estate firm. We need inbound lead qualification immediately. Budget is $3,500/month, timeline is next week.",
                    "summary": "Sarah Jenkins interested in AI voice calling agent for real estate firm. Budget $3.5k/mo, timeline next week.",
                    "qualification_score": QualificationScoreEnum.hot,
                    "duration_seconds": 78,
                    "language": LanguageEnum.english,
                    "hours_ago": 2,
                }
            ],
            "follow_ups": [
                {
                    "notes": "Send enterprise pricing proposal and schedule Zoom demo with Sarah.",
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
                    "transcript": "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? Ahmed Raza: Bhai Urdu mein baat karte hain. Mujhe apni auto parts store ke liye AI receptionist chahiye jo Urdu aur English dono mein calls attend kare. Budget 60 hazaar rupay mahina hai.",
                    "summary": "Ahmed Raza wants bilingual AI receptionist for auto parts store in Urdu. Budget 60k PKR/month.",
                    "qualification_score": QualificationScoreEnum.hot,
                    "duration_seconds": 95,
                    "language": LanguageEnum.urdu,
                    "hours_ago": 5,
                }
            ],
            "follow_ups": [
                {
                    "notes": "Call Ahmed back to discuss Urdu speech model tuning and integration timeline.",
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
                    "scheduled_hours_from_now": 2,
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
                    "scheduled_hours_from_now": -4, # Past due or completed
                    "completed": True,
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
            "status": LeadStatusEnum.new,
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
        # Check if lead already exists
        existing_lead = db.query(Lead).filter(Lead.phone == lead_data["phone"]).first()
        if existing_lead:
            print(f"Lead {lead_data['name']} already exists. Skipping...")
            continue

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
    print("Demo data successfully seeded into database!")


if __name__ == "__main__":
    seed_database()
