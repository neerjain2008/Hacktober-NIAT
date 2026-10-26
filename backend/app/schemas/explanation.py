from typing import List, Optional
from pydantic import Field
from .analysis import CamelBaseModel, DetectedIndicator, ThreatExplanation


class ExplainRequest(CamelBaseModel):
    text: str = Field(..., description="Original user text or URL analyzed")
    risk_score: int = Field(50, description="Risk score calculated by the heuristic engine")
    risk_level: str = Field("SUSPICIOUS", description="Calculated threat level tier")
    indicators: List[DetectedIndicator] = Field(default_factory=list, description="Detected indicators")
    model: Optional[str] = Field("gemma4:e2b", description="Target local Ollama model")


class ExplainResponse(CamelBaseModel):
    success: bool = True
    explanation: ThreatExplanation
    model_used: Optional[str] = None
    source: Optional[str] = None
    notice: Optional[str] = None
