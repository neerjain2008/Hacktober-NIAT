from typing import List
from app.schemas.analysis import DetectedIndicator, ThreatExplanation


def generate_deterministic_explanation(
    score: int,
    risk_level: str,
    indicators: List[DetectedIndicator],
) -> ThreatExplanation:
    if risk_level == "SAFE" or len(indicators) == 0:
        return ThreatExplanation(
            summary="No recognized malicious scam patterns, urgency traps, or phishing indicators were found in this content.",
            psychological_trigger="None identified. The message appears informational or standard correspondence.",
            action_items=[
                "Always verify sender email addresses or domain origins independently before taking action.",
                "Never enter passwords or OTPs on pages opened via unverified third-party notifications.",
                "Keep standard security precautions active (2-Factor Authentication).",
            ],
            source="engine",
        )

    indicator_titles = ", ".join([ind.title for ind in indicators[:3]])

    psych_trap = "Artificial urgency combined with fear of loss or excitement of an unexpected reward."
    if any(ind.category == "bait" for ind in indicators):
        psych_trap = "Greed & Curiosity Bait: Exploiting excitement around unearned prizes, cash rewards, or quick income."
    elif any(ind.category == "urgency" for ind in indicators):
        psych_trap = "Panic & Fear Manipulation: Manufacturing a crisis (account closure, legal threat) to bypass critical thinking."
    elif any(ind.category == "impersonation" for ind in indicators):
        psych_trap = "Authority Mimicry: Preying on deference to established financial institutions, government, or courier services."

    summary = (
        f"This content scored a {score}% risk rating due to detected threat patterns including: {indicator_titles}. "
        f"Genuine institutions never demand immediate payments or credential verification via unsolicited links."
    )

    action_items = [
        "DO NOT click any links, scan QR codes, or download attachments provided in this message.",
        "DO NOT disclose OTP, bank details, passwords, or personal identity numbers.",
        "Block the sender immediately and report the incident to your local Cyber Crime portal (e.g. 1930 / cybercrime.gov.in) or your banking institution.",
    ]

    return ThreatExplanation(
        summary=summary,
        psychological_trigger=psych_trap,
        action_items=action_items,
        source="engine",
    )
