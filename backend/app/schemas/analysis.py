from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


def to_camel(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class CamelBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class DetectedIndicator(CamelBaseModel):
    rule_id: str
    title: str
    description: str
    category: Literal["urgency", "financial", "impersonation", "credentials", "technical", "bait"]
    severity: Literal["low", "medium", "high", "critical"]
    impact_percent: int
    matched_snippet: Optional[str] = None


class CategoryScores(CamelBaseModel):
    urgency: int = 0
    financial: int = 0
    impersonation: int = 0
    credentials: int = 0
    technical: int = 0
    bait: int = 0


class ThreatExplanation(CamelBaseModel):
    summary: str
    psychological_trigger: str
    action_items: List[str]
    source: Literal["ollama_local", "engine", "deterministic_engine"]


class AnalyzeRequest(CamelBaseModel):
    text: str = Field(..., min_length=1, description="Message text, URL, or OCR extracted text")
    type: Literal["message", "url", "screenshot"] = "message"
    model: Optional[str] = "gemma4:e2b"
    skip_ai_synthesis: bool = False


class AnalyzeResponse(CamelBaseModel):
    risk_score: int
    risk_level: Literal["SAFE", "LOW_RISK", "SUSPICIOUS", "HIGH_RISK", "CRITICAL_THREAT"]
    risk_label: str
    summary: str
    indicators: List[DetectedIndicator]
    category_scores: CategoryScores
    explanation: Optional[ThreatExplanation] = None
    analyzed_at: str
    type: Literal["message", "url", "screenshot"]
