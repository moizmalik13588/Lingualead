<div align="center">

# 🎙️ LinguaLead

### Bilingual AI Voice Sales Agent + CRM Automation

**Turning phone conversations into qualified CRM leads — in Urdu or English, automatically.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Frontend-8b5cf6?style=for-the-badge)](https://lingualead.vercel.app/)
[![API Docs](https://img.shields.io/badge/API%20Docs-Swagger-009688?style=for-the-badge)](https://stellar-motivation-production-f6af.up.railway.app/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](#-license)

[**🔗 Live Demo**](https://lingualead.vercel.app/) · [**📖 API Docs**](https://stellar-motivation-production-f6af.up.railway.app/docs) · [**🐛 Report an Issue**](../../issues)

</div>

---

## 💼 The Problem

Sales and service teams lose high-intent leads every day because of slow response times and language barriers in bilingual markets like Pakistan (English & Urdu). A missed call at 2 AM, or a caller who's more comfortable in Urdu than English, often means a lost customer.

## 💡 The Solution

**LinguaLead** is an autonomous, 24/7 bilingual voice sales agent powered by **Vapi.ai** and **Groq LLM**. It:

- 📞 Answers inbound calls and converses naturally in **Urdu or English**
- 🧠 Extracts structured lead data — interest, budget, timeline, and a qualification score
- 🔥 Automatically classifies leads as **Hot / Warm / Cold**
- 📋 Syncs everything to a CRM dashboard in real time
- ⏰ Auto-schedules follow-ups for promising leads — no human ever has to remember

No missed leads. No language barrier. No manual data entry.

---

## 🖥️ See It In Action

Visit the **[live dashboard](https://lingualead.vercel.app/)** to explore:

- **Dashboard** — real-time stats, an AI Assistant insights panel, and a hot-lead pipeline ratio
- **Leads CRM** — filterable, searchable lead list with bilingual call history
- **AI Voice Demo Simulator** — trigger a simulated English or Urdu call and watch it flow through the full AI → CRM pipeline live, no real phone call needed

---

## 🏛️ Architecture & Workflow

```
   Customer Call
        │
        ▼
 Vapi.ai Voice Agent  ──────────  Bilingual (Urdu / English) conversation
        │
        ▼  webhook: call completed
 FastAPI Backend  ─────────────  Signature verification + idempotency check
        │
        ▼
 Groq LLM (Structured Output)  ─  Pydantic-validated extraction
        │
        ▼
 PostgreSQL CRM  ──────────────  SQLAlchemy + Alembic
        │
        ▼
 React + Vite + Tailwind  ─────  Live dashboard
```

**Deployment:** React frontend on Vercel (with a rewrite proxy to the backend), FastAPI backend on Railway, PostgreSQL on Railway.

---

## 🛡️ AI Safety & Guardrails

LinguaLead is built with production-minded guardrails, not just a happy-path demo:

**Voice agent**
- Stays strictly within its role as a lead-qualification agent; refuses out-of-scope requests
- Never reveals system prompts, instructions, or API secrets — and ignores caller attempts to override its instructions
- Makes no unauthorized commitments on pricing, discounts, or contracts — defers these to a human
- Collects only the minimum data needed (name, interest, budget, timeline); defers uncertain answers to human follow-up instead of guessing
- Handles abusive or spam calls gracefully with a natural human hand-off

**LLM & automation layer**
- Treats call transcripts as **untrusted input** — instructions embedded in a transcript can never override system logic
- Every structured extraction is validated against a Pydantic schema before it touches the database
- Failed extractions are never discarded — the raw call is saved with a "needs review" flag instead
- Clearly separates what the caller actually said (`transcript`) from what the AI inferred (`summary`, `qualification_score`)

**Backend**
- Cryptographic webhook signature verification on every incoming Vapi event
- Idempotency checks (via `vapi_call_id`) prevent duplicate processing
- Rate limiting on public and webhook endpoints
- All secrets (API keys, DB URLs) stay server-side via `pydantic-settings` — never exposed to the frontend
- Structured logging across webhook handling, validation, and CRM syncs for debugging and auditing

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI (Python 3.11+), SQLAlchemy 2.0, Alembic, Pydantic Settings, Uvicorn |
| **Database** | PostgreSQL |
| **AI / Voice** | Vapi.ai (voice + webhooks), Groq (LLM inference), Twilio (telephony) |
| **Frontend** | React 19, Vite, Tailwind CSS |
| **Hosting** | Vercel (frontend), Railway (backend + database) |

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- Node.js & npm
- PostgreSQL (local or remote)

### 1. Clone and configure environment
```bash
git clone https://github.com/moizmalik13588/Lingualead.git
cd Lingualead
cp backend/.env.example backend/.env
```
Fill in your database URL and API keys (`VAPI_API_KEY`, `GROQ_API_KEY`, etc.) in `backend/.env`.

### 2. Backend setup
```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
python main.py
```
The API runs at `http://localhost:8000`.
- Swagger docs: `http://localhost:8000/docs`
- Health check: `GET http://localhost:8000/api/health`

### 3. Frontend setup
```bash
cd frontend
npm install
npm run dev
```
The app runs at `http://localhost:5173`.

### 4. Testing real Vapi calls locally (ngrok)
Vapi's servers can't reach `localhost`, so you'll need a tunnel:
```bash
ngrok http 8000
```
Copy the HTTPS forwarding URL and set it as your Vapi assistant's webhook:
```
<ngrok-url>/api/vapi/webhook
```
> Free-tier ngrok URLs change on every restart — update the webhook URL in Vapi's dashboard each time.

---

## 📂 Project Structure

```
Lingualead/
├── backend/
│   ├── alembic/            # Database migrations
│   ├── app/
│   │   ├── api/            # Routes and dependencies
│   │   ├── core/           # Config and database setup
│   │   ├── models/         # SQLAlchemy models (Lead, Call, FollowUp)
│   │   ├── schemas/        # Pydantic validation schemas
│   │   ├── services/       # Business logic (Vapi, Groq, CRM)
│   │   └── utils/
│   ├── scripts/            # Seed data, backfills, one-off utilities
│   └── main.py             # FastAPI entrypoint
├── frontend/
│   ├── src/                # React components & pages
│   ├── vercel.json         # Proxy rewrite to backend API
│   └── vite.config.ts
├── .env.example
└── README.md
```

---

## 📄 License

MIT License — free to use, modify, and learn from.

---

<div align="center">

Built by **[Muhammad Moiz](https://github.com/moizmalik13588)** as part of an AI-agents portfolio.

</div>
