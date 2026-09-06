from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, SessionLocal
from app.models import Base
from app.models.lead import Lead
from app.api.routes.vapi import router as vapi_router
from app.api.routes.crm import router as crm_router
from app.api.routes.demo import router as demo_router
from scripts.seed_demo_data import seed_database

app = FastAPI(
    title="LinguaLead API",
    description="Bilingual AI Voice Calling Agent & CRM Automation System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.on_event("startup")
def startup_event():
    import traceback
    try:
        print(f"Connecting to database URL: {settings.DATABASE_URL[:30]}...")
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        lead_count = db.query(Lead).count()
        db.close()
        print(f"Database connected successfully. Lead count: {lead_count}")
        if lead_count == 0:
            print("Database is empty on startup. Auto-seeding demo data...")
            seed_database(reset=False)
    except Exception as e:
        print(f"CRITICAL: Startup database initialization error: {e}")
        traceback.print_exc()
        raise e

# Configure standard FastAPI CORSMiddleware with wildcard origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(vapi_router)
app.include_router(crm_router)
app.include_router(demo_router)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "LinguaLead API",
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
