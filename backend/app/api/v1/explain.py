from fastapi import APIRouter
from app.schemas.explanation import ExplainRequest, ExplainResponse
from app.services.threat_synthesizer import threat_synthesizer

router = APIRouter()


@router.post("/explain", response_model=ExplainResponse, summary="Generate AI Threat Explanation")
async def explain_content(payload: ExplainRequest):
    """
    Direct drop-in replacement for the Next.js /api/explain route.
    Synthesizes an authoritative executive breakdown, psychological manipulation trap,
    and 3 defensive actions using local Ollama or the deterministic engine.
    """
    explanation, model_used = await threat_synthesizer.synthesize(
        text=payload.text,
        risk_score=payload.risk_score,
        risk_level=payload.risk_level,
        indicators=payload.indicators,
        model=payload.model,
        skip_ai_synthesis=False,
    )

    return ExplainResponse(
        success=True,
        explanation=explanation,
        model_used=model_used,
        source=explanation.source,
        notice="100% Local Inference (Privacy Guaranteed)",
    )
