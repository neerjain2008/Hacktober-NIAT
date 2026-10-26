from fastapi import APIRouter
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.core.engine import analyze_scam_content
from app.services.threat_synthesizer import threat_synthesizer

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse, summary="Analyze Threat Content")
async def analyze_content(payload: AnalyzeRequest):
    """
    Evaluates raw message text, URL, or OCR snippet using the calibrated deterministic
    heuristic engine and attaches an AI threat synthesis explanation.
    """
    # 1. 0ms Deterministic Heuristic Evaluation
    res = analyze_scam_content(payload.text, payload.type)

    # 2. Local AI Threat Synthesis (with zero-latency fallback)
    explanation, _ = await threat_synthesizer.synthesize(
        text=payload.text,
        risk_score=res.risk_score,
        risk_level=res.risk_level,
        indicators=res.indicators,
        model=payload.model,
        skip_ai_synthesis=payload.skip_ai_synthesis,
    )

    res.explanation = explanation
    res.summary = explanation.summary
    return res
