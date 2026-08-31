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

## 🛠️ Tech Stack
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

### 6. Frontend Setup
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
