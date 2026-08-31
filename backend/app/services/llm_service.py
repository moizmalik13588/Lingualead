import json
import logging
from typing import Any, Dict, Optional
from groq import Groq

from app.core.config import settings
from app.schemas.llm_extraction import LLMExtractionResult

logger = logging.getLogger(__name__)


class LLMService:
    @staticmethod
    def extract_lead_insights(transcript: str, caller_phone: str = "", caller_name: str = "") -> Optional[LLMExtractionResult]:
        """
        Calls Groq API with a deterministic prompt to extract structured lead qualification data
        from a phone call transcript. Validates output against LLMExtractionResult Pydantic schema.
        """
        if not settings.GROQ_API_KEY or settings.GROQ_API_KEY == "your_groq_api_key_here":
            logger.warning("GROQ_API_KEY not configured. Using heuristic/fallback LLM extraction.")
            return LLMService._fallback_extraction(transcript, caller_phone, caller_name)

        prompt = f"""
You are an expert AI sales analyst for LinguaLead, a bilingual AI voice calling agent system.
Analyze the following phone conversation transcript between our AI agent and a caller/lead.
Extract structured information and return ONLY valid JSON matching this exact schema:
{{
  "leadName": "string (caller name or Unknown)",
  "phone": "string (phone number if mentioned or provided)",
  "language": "string (urdu or english)",
  "interest": "string (product or service of interest)",
  "budget": "string (budget mentioned or Unknown)",
  "timeline": "string (timeline mentioned or Unknown)",
  "qualification": "hot" | "warm" | "cold",
  "summary": "string (concise conversation summary)",
  "followUpReason": "string (reason for follow-up)",
  "confidence": float (0.0 to 1.0)
}}

Qualification criteria:
- HOT: Immediate buyer, high budget, urgent timeline (within days), explicit intent.
- WARM: Interested, moderate budget/timeline (weeks/months), asking relevant questions.
- COLD: Just browsing, no budget, unclear timeline, or uninterested.

Transcript:
""" + transcript

        try:
            client = Groq(api_key=settings.GROQ_API_KEY)
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise JSON-only data extraction engine. Always output valid JSON with no markdown formatting or commentary if possible, or valid JSON block."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
            )

            content = completion.choices[0].message.content
            data = json.loads(content)
            
            # Ensure phone is populated if empty from LLM
            if not data.get("phone") and caller_phone:
                data["phone"] = caller_phone
            if not data.get("leadName") and caller_name and caller_name != "Unknown Caller":
                data["leadName"] = caller_name

            # Validate against Pydantic schema
            result = LLMExtractionResult(**data)
            return result

        except Exception as e:
            logger.error(f"Error calling Groq LLM or parsing response: {e}")
            return LLMService._fallback_extraction(transcript, caller_phone, caller_name)

    @staticmethod
    def _fallback_extraction(transcript: str, caller_phone: str, caller_name: str) -> LLMExtractionResult:
        """
        Fallback heuristic extraction when Groq API key is missing or LLM call fails.
        Ensures the system never crashes on LLM failure.
        """
        lower_text = transcript.lower()
        
        # Heuristic qualification
        qualification = "warm"
        if any(w in lower_text for w in ["urgent", "ready", "buy", "price", "kitna", "jaldi", "immediately"]):
            qualification = "hot"
        elif any(w in lower_text for w in ["not sure", "thinking", "maybe", "bad mein", "sochenge"]):
            qualification = "cold"

        language = "urdu" if any(w in lower_text for w in ["mein", "hai", "kya", "aap", "sukriya", "khuda", "hain", "ji"]) else "english"

        return LLMExtractionResult(
            leadName=caller_name if caller_name and caller_name != "Unknown Caller" else "Valued Caller",
            phone=caller_phone if caller_phone else "+923000000000",
            language=language,
            interest="General Inquiry / Software Solutions",
            budget="Moderate / Unspecified",
            timeline="Within 2-4 weeks",
            qualification=qualification,
            summary=transcript[:200] + "..." if len(transcript) > 200 else transcript,
            followUpReason="Review call transcript and provide requested information.",
            confidence=0.75,
        )
