# LinguaLead

> **LinguaLead** is a bilingual AI voice sales agent that automatically turns phone conversations into qualified CRM leads and follow-up actions.

## 💼 Business Value
Sales and service teams lose high-intent leads due to slow response times and language barriers in bilingual markets (English & Urdu/Hindi). LinguaLead acts as an autonomous 24/7 bilingual voice sales agent powered by Vapi.ai and Groq LLM. It engages callers naturally in Urdu or English, extracts structured qualification data (Interest, Budget, Timeline, Qualification Score), and syncs qualified leads directly to the CRM with automated follow-up scheduling.

---

## 🏛️ Architecture & Workflow
```
[Customer Call] 
       │
       ▼
 [Vapi.ai Voice Agent] (Bilingual Urdu/English)
       │
       ▼ (Webhook / Call Completed)
 [FastAPI Backend] (Signature Verification & Idempotency)
       │
       ▼
 [Groq LLM / Structured Output] (Pydantic Validation)
       │
       ▼
 [PostgreSQL CRM + SQLAlchemy & Alembic]
       │
       ▼
 [React + Vite + Tailwind Dashboard]
```

---

## 🛡️ AI Safety & Guardrails

LinguaLead is engineered with production-minded guardrails to ensure robust, secure, and predictable operation:

1. **Voice Agent Prompt Guardrails**:
   - **Role Discipline**: Strictly operates as a sales lead-qualification agent and refuses out-of-scope queries.
   - **Confidentiality & Prompt Injection Defense**: Never reveals system prompts, internal instructions, or API secrets, and ignores caller attempts to override instructions via voice input.
   - **Policy & Pricing Boundaries**: Never makes unauthorized commitments regarding pricing, discounts, refunds, or contracts, deferring these to human sales reps.
   - **Minimal PII & Accuracy**: Collects only lead-qualification data (Name, Interest, Budget, Timeline) and defers uncertain details to human follow-up rather than hallucinating answers.
   - **Abuse & Handoff**: Gracefully handles spam or abusive calls and provides natural human handoff lines.

2. **LLM & Automation Layer Guardrails**:
   - **Untrusted Input Handling**: Treats call transcripts as untrusted input; embedded transcript instructions cannot alter CRM logic or prompt state.
   - **Pydantic Schema Validation**: Every structured extraction from Groq LLM is strictly validated against Pydantic models before touching the database.
   - **Fallback / "Needs Review" Rescue**: If LLM extraction or parsing fails, the raw call is saved securely with a review flag to prevent system crashes or unvalidated data pollution.
   - **Transcript vs Inference Separation**: Clearly distinguishes raw caller speech (`transcript`) from AI-inferred insights (`summary`, `qualification_score`).

3. **Backend Security & Reliability**:
   - **Webhook Signature Verification**: Cryptographically verifies all incoming Vapi webhooks using shared secrets.
   - **Idempotency**: Prevents duplicate webhook processing using unique Vapi call IDs (`vapi_call_id`).
   - **Rate Limiting**: Built-in rate limiting prevents API endpoint abuse.
   - **Secure Secret Management**: All credentials (API keys, webhook secrets, DB URLs) remain strictly server-side via `pydantic-settings`.
   - **Structured Logging**: Comprehensive event logging (webhooks received, validation results, CRM syncs, and errors) for debugging and auditing.

---
- **Backend**: FastAPI (Python 3.11+), SQLAlchemy 2.0, Alembic, Pydantic Settings, Uvicorn
- **Database**: PostgreSQL
- **AI / Voice**: Vapi.ai (Voice Calling / Webhooks), Groq (LLM Inference), Twilio (Telephony)
- **Frontend**: React 19, Vite, Tailwind CSS
- **Environment**: pydantic-settings, python-dotenv, httpx

---

## 🚀 Local Setup & Installation

### 1. Prerequisites
- Python 3.11+ installed
- Node.js & npm installed
- PostgreSQL running locally or accessible via connection string

### 2. Environment Configuration
Copy `.env.example` to `.env` in the root directory and configure your credentials:
```bash
cp .env.example .env
```
Fill in your database URL and API keys (`VAPI_API_KEY`, `GROQ_API_KEY`, etc.).

### 3. Backend Setup
Navigate to the `backend` directory, set up virtual environment, install dependencies, and run database migrations:
```bash
cd backend
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 4. Database Migrations (Alembic)
Ensure PostgreSQL is running and the database is created (`lingualead`). Run migrations:
```bash
alembic upgrade head
```

### 5. Running the Backend Server
```bash
python main.py
```
The FastAPI server will start on `http://localhost:8000`.
- **API Docs (Swagger)**: Explore available endpoints at `http://localhost:8000/docs`
- **Health Check**: `GET http://localhost:8000/api/health`

### 6. Local Webhook Testing with ngrok (for Real Vapi Calls)
Since Vapi's servers cannot reach `localhost:8000` directly, you need a tunnel like ngrok to test live Vapi webhooks locally:
1. **Install ngrok** (if not already installed):
   - Via Windows Package Manager:
     ```bash
     winget install ngrok.ngrok
     ```
   - Or download directly from [ngrok.com/download](https://ngrok.com/download).
2. **Expose your local FastAPI backend**:
   ```bash
   ngrok http 8000
   ```
3. **Configure Vapi Assistant Webhook**:
   - Copy the HTTPS forwarding URL generated by ngrok (e.g., `https://xxxx.ngrok-free.app`).
   - Update your Vapi assistant settings / dashboard webhook URL to:
     `<ngrok-url>/api/vapi/webhook`
   - *Note*: Free tier ngrok URLs change every time ngrok is restarted, so you will need to update the webhook URL in Vapi if you restart ngrok.

### 7. Frontend Setup
Navigate to the `frontend` directory and start the development server:
```bash
cd frontend
npm install
npm run dev
```
The frontend will start on `http://localhost:5173`.

---

## 📂 Project Structure
```
Lingualead/
├── backend/
│   ├── alembic/            # Database migrations
│   ├── app/
│   │   ├── api/            # API routes and dependencies
│   │   ├── core/           # Config and database setup
│   │   ├── models/         # SQLAlchemy models (Lead, Call, FollowUp)
│   │   ├── schemas/        # Pydantic validation schemas
│   │   ├── services/       # Business logic (Vapi, Groq, CRM)
│   │   └── utils/          # Utilities
│   └── main.py             # FastAPI entrypoint
├── frontend/
│   ├── src/                # React components & pages
│   ├── package.json
│   └── vite.config.ts
├── .env.example
└── README.md
```

---

## 📄 License
MIT License
