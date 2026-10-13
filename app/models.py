from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class ServiceSuggestion(BaseModel):
    service: str
    explanation: str
    confidence: Literal["high", "medium", "low"] = "medium"
    service_id: Optional[str] = None


class AnalysisResult(BaseModel):
    requirements: List[str] = Field(default_factory=list, description="Extracted functional and non-functional requirements")
    risks: List[str] = Field(default_factory=list, description="Identified risks (technical, scope, timeline, compliance, data)")
    clarifying_questions: List[str] = Field(default_factory=list, description="Open questions that need answers before accurate scoping")
    suggested_services: List[ServiceSuggestion] = Field(default_factory=list)
    summary: str = ""
    mode: Literal["llm", "keyword_fallback"] = "keyword_fallback"
    brief_length: int = 0


class AnalyzeRequest(BaseModel):
    brief: str = Field(..., min_length=10, max_length=15000, description="Client project brief text")


class HealthResponse(BaseModel):
    status: str = "ok"
    llm_provider: str
    model: Optional[str] = None
