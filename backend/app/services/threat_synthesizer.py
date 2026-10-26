from typing import List, Optional, Tuple
from app.schemas.analysis import DetectedIndicator, ThreatExplanation
from app.core.fallback_engine import generate_deterministic_explanation
from app.services.ollama_client import ollama_client


class ThreatSynthesizer:
    @staticmethod
    def build_prompt(
        text: str,
        risk_score: int,
        risk_level: str,
        indicators: List[DetectedIndicator],
    ) -> str:
        indicators_str = "\n".join(
            [f"- {ind.title}: {ind.description}" for ind in indicators]
        ) or "- None"

        return f"""You are ScamShield AI, an elite cybersecurity and fraud intelligence agent running 100% locally.
Analyze the following user-submitted message or URL with calculated threat metrics:

Risk Score: {risk_score}%
Calculated Threat Level: {risk_level}
Detected Heuristic Indicators:
{indicators_str}

Raw User Input:
\"\"\"
{text}
\"\"\"

TASK:
1. Explain in 2 crisp, authoritative sentences why this content is suspicious or what deceptive strategy it uses.
2. Identify the specific psychological trigger or trap exploited (e.g. Fear of Account Loss, Greed / Prize Euphoria, Impersonation of Legitimate Authority, Urgency Pressure).
3. Provide exactly 3 actionable, bulleted defensive steps the user must take right now to protect themselves.

FORMAT YOUR RESPONSE IN STRICT JSON:
{{
  "summary": "2-sentence clear threat analysis...",
  "psychologicalTrigger": "Name & short description of the psychological manipulation...",
  "actionItems": [
    "Immediate action 1",
    "Immediate action 2",
    "Immediate action 3"
  ]
}}"""

    async def synthesize(
        self,
        text: str,
        risk_score: int,
        risk_level: str,
        indicators: List[DetectedIndicator],
        model: Optional[str] = None,
        skip_ai_synthesis: bool = False,
    ) -> Tuple[ThreatExplanation, Optional[str]]:
        """
        Synthesize threat explanation using Local Ollama if available,
        otherwise gracefully fall back to the deterministic heuristic engine.
        Returns (ThreatExplanation, model_used_or_None).
        """
        if not skip_ai_synthesis:
            prompt = self.build_prompt(text, risk_score, risk_level, indicators)
            parsed_json, model_used = await ollama_client.chat(prompt, preferred_model=model)

            if parsed_json:
                summary = parsed_json.get("summary") or "Content flagged as potentially deceptive."
                psych_trigger = (
                    parsed_json.get("psychologicalTrigger")
                    or parsed_json.get("psychological_trigger")
                    or "Urgency & Authority exploitation"
                )
                action_items = (
                    parsed_json.get("actionItems")
                    or parsed_json.get("action_items")
                )
                if not isinstance(action_items, list) or len(action_items) == 0:
                    action_items = [
                        "Do not click links or provide credentials.",
                        "Verify with the genuine organization via official contacts.",
                        "Report this incident to cybercrime authorities.",
                    ]

                return (
                    ThreatExplanation(
                        summary=summary,
                        psychological_trigger=psych_trigger,
                        action_items=action_items[:3],
                        source="ollama_local",
                    ),
                    model_used,
                )

        # Fallback to 100% Local Deterministic Heuristic Engine
        fallback = generate_deterministic_explanation(risk_score, risk_level, indicators)
        return (
            ThreatExplanation(
                summary=fallback.summary,
                psychological_trigger=fallback.psychological_trigger,
                action_items=fallback.action_items,
                source="deterministic_engine",
            ),
            "Deterministic Heuristic Engine",
        )


threat_synthesizer = ThreatSynthesizer()
