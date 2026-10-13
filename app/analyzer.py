"""
Core analysis engine.
Hybrid approach:
1. Keyword-based service mapping (always available)
2. LLM structured extraction when API key is present
"""

import json
import os
import re
from typing import List, Dict, Optional

from openai import OpenAI
from dotenv import load_dotenv

from .models import AnalysisResult, ServiceSuggestion
from .services_catalog import ALL_SERVICES, ENTERPRISE_SERVICES, EXPRESS_SERVICES

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
MODEL_NAME = os.getenv("MODEL_NAME")


def _get_client() -> Optional[OpenAI]:
    if LLM_PROVIDER == "none":
        return None

    if LLM_PROVIDER == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return None
        return OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

    if LLM_PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        return OpenAI(api_key=api_key)

    if LLM_PROVIDER == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return OpenAI(
            api_key="ollama",
            base_url=f"{base_url}/v1",
        )

    return None


def _default_model() -> str:
    if MODEL_NAME:
        return MODEL_NAME
    if LLM_PROVIDER == "groq":
        return "llama-3.3-70b-versatile"
    if LLM_PROVIDER == "openai":
        return "gpt-4o-mini"
    if LLM_PROVIDER == "ollama":
        return "llama3.2"
    return "llama-3.3-70b-versatile"


SYSTEM_PROMPT = """You are a senior solutions architect at TechAbout, an enterprise technology company.

Your job is to analyse a client's project brief and produce a structured JSON response with exactly these keys:

{
  "requirements": ["list of clear, actionable requirements extracted from the brief"],
  "risks": ["list of realistic risks: technical, scope, timeline, data quality, compliance, integration, team, budget"],
  "clarifying_questions": ["list of precise open questions that must be answered before accurate scoping and pricing"],
  "summary": "2-3 sentence executive summary of what the client actually needs"
}

Rules:
- Be specific and professional.
- Requirements should be concrete (not vague marketing language).
- Risks should be realistic and prioritised.
- Clarifying questions should be high-value (budget range, timeline, existing systems, compliance, user volume, success metrics, data readiness, etc.).
- Do NOT invent requirements that are not implied by the brief.
- Output ONLY valid JSON. No markdown, no commentary.
"""


def _keyword_service_match(brief: str) -> List[ServiceSuggestion]:
    """Always-available keyword matcher against the TechAbout catalogue."""
    brief_lower = brief.lower()
    scores: Dict[str, int] = {}

    for service in ALL_SERVICES:
        score = 0
        for kw in service["keywords"]:
            # whole-word-ish match
            if re.search(rf"\b{re.escape(kw.lower())}\b", brief_lower):
                score += 2
            elif kw.lower() in brief_lower:
                score += 1
        if score > 0:
            scores[service["id"]] = score

    # Sort by score descending
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    suggestions = []
    for sid, score in ranked[:5]:  # top 5
        svc = next(s for s in ALL_SERVICES if s["id"] == sid)
        confidence = "high" if score >= 4 else "medium" if score >= 2 else "low"
        suggestions.append(
            ServiceSuggestion(
                service=svc["name"],
                explanation=svc["description"],
                confidence=confidence,
                service_id=sid,
            )
        )

    # If nothing matched, suggest a safe default
    if not suggestions:
        suggestions.append(
            ServiceSuggestion(
                service="Enterprise Software Development",
                explanation="No strong keyword match. Default recommendation for custom software work; discovery call recommended.",
                confidence="low",
                service_id="enterprise-software",
            )
        )

    return suggestions


def _llm_analyze(brief: str) -> Optional[dict]:
    client = _get_client()
    if not client:
        return None

    try:
        response = client.chat.completions.create(
            model=_default_model(),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Project brief:\n\n{brief}"},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
            max_tokens=1500,
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"[analyzer] LLM call failed: {e}")
        return None


def analyze_brief(brief: str) -> AnalysisResult:
    brief = brief.strip()
    if len(brief) < 10:
        return AnalysisResult(
            requirements=[],
            risks=["Brief is too short to analyse meaningfully."],
            clarifying_questions=["Please provide a more detailed project description."],
            suggested_services=[],
            summary="Insufficient information.",
            mode="keyword_fallback",
            brief_length=len(brief),
        )

    # 1. Always run keyword service mapping
    service_suggestions = _keyword_service_match(brief)

    # 2. Try LLM for requirements / risks / questions
    llm_data = _llm_analyze(brief)

    if llm_data:
        return AnalysisResult(
            requirements=llm_data.get("requirements", [])[:12],
            risks=llm_data.get("risks", [])[:10],
            clarifying_questions=llm_data.get("clarifying_questions", [])[:10],
            suggested_services=service_suggestions,
            summary=llm_data.get("summary", "")[:500],
            mode="llm",
            brief_length=len(brief),
        )

    # 3. Keyword-only fallback (very lightweight heuristics)
    requirements = _heuristic_requirements(brief)
    risks = _heuristic_risks(brief)
    questions = _heuristic_questions(brief)

    return AnalysisResult(
        requirements=requirements,
        risks=risks,
        clarifying_questions=questions,
        suggested_services=service_suggestions,
        summary="Analysis performed with keyword heuristics only (no LLM key configured).",
        mode="keyword_fallback",
        brief_length=len(brief),
    )


def _heuristic_requirements(brief: str) -> List[str]:
    reqs = []
    lower = brief.lower()
    if any(w in lower for w in ["mobile", "ios", "android", "app"]):
        reqs.append("Mobile application (iOS/Android or cross-platform)")
    if any(w in lower for w in ["web", "website", "portal", "dashboard"]):
        reqs.append("Web application or portal")
    if any(w in lower for w in ["ai", "ml", "machine learning", "llm", "chatbot"]):
        reqs.append("AI / Machine Learning capability")
    if any(w in lower for w in ["cloud", "aws", "azure", "kubernetes"]):
        reqs.append("Cloud infrastructure / DevOps")
    if any(w in lower for w in ["saas", "multi-tenant", "subscription"]):
        reqs.append("Multi-tenant SaaS platform")
    if any(w in lower for w in ["data", "analytics", "dashboard", "reporting"]):
        reqs.append("Data pipelines or analytics / reporting layer")
    if any(w in lower for w in ["security", "compliance", "gdpr", "soc 2"]):
        reqs.append("Security hardening or compliance readiness")
    if not reqs:
        reqs.append("Custom software development (details insufficient for finer classification)")
    return reqs


def _heuristic_risks(brief: str) -> List[str]:
    risks = [
        "Scope may be under-specified; discovery workshop recommended.",
        "Timeline and budget not stated – risk of misaligned expectations.",
    ]
    lower = brief.lower()
    if "legacy" in lower or "existing system" in lower:
        risks.append("Legacy system integration or data migration complexity.")
    if any(w in lower for w in ["ai", "ml", "llm"]):
        risks.append("Data quality / labelled data availability for AI work.")
    if any(w in lower for w in ["compliance", "gdpr", "hipaa", "pci", "soc 2"]):
        risks.append("Regulatory / compliance requirements may extend timeline.")
    return risks


def _heuristic_questions(brief: str) -> List[str]:
    return [
        "What is the target go-live date or hard deadline?",
        "What is the approximate budget range for this engagement?",
        "Are there existing systems or data sources that must be integrated?",
        "How many concurrent users / daily active users are expected?",
        "Are there specific compliance, security or data-residency requirements?",
        "Who will own product decisions and provide feedback during the project?",
    ]
