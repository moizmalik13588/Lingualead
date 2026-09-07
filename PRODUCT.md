# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Sales and service teams in bilingual markets (English & Urdu), specifically businesses receiving inbound phone inquiries (e.g., Pakistan market).

## Product Purpose
LinguaLead is an autonomous, 24/7 bilingual voice sales agent and CRM automation tool. It turns phone conversations into qualified CRM leads in Urdu or English automatically, preventing missed leads, overcoming language barriers, and eliminating manual data entry.

## Positioning
An autonomous bilingual voice sales agent that handles real-time conversational qualification in both Urdu and English, seamlessly syncing structured lead data and call history to a real-time CRM dashboard.

## Operating Context
Inbound phone calls from customers speaking English or Urdu inquiring about sales or services, processed via Vapi.ai voice agents, analyzed by Groq LLM, stored in PostgreSQL, and managed via a React + Vite + Tailwind dashboard.

## Capabilities and Constraints
- Inbound call handling in Urdu or English via Vapi.ai
- Structured lead data extraction (interest, budget, timeline, qualification score) using Groq LLM with Pydantic validation
- Lead classification (Hot / Warm / Cold) and automated follow-up scheduling
- Real-time CRM dashboard with bilingual call history and statistics
- AI Voice Demo Simulator for testing call flows
- Backend built with FastAPI, SQLAlchemy, Alembic; Frontend built with React, Vite, Tailwind CSS (hosted on Vercel)

## Brand Commitments
- Name: LinguaLead
- Color theme: Purple / Violet brand accent (`#8b5cf6` / violet-500)
- Bilingual capability (Urdu & English)

## Evidence on Hand
- README.md
- Frontend codebase in `frontend/src/`
- Backend codebase in `backend/app/`

## Product Principles
1. **Reliability & Guardrails**: Strict cryptographic verification, idempotency, and robust Pydantic validation on all untrusted webhook inputs and transcripts.
2. **Bilingual Fluidity**: Equal first-class support for English and Urdu across voice agent and CRM records.
3. **Actionable Clarity**: Instant classification (Hot/Warm/Cold) and pipeline metrics without manual data entry.
4. **Refined Craft**: Clean, intentional visual hierarchy preserving the violet brand identity while eliminating generic AI UI patterns.
