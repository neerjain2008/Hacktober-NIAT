import re
from datetime import datetime, timezone
from typing import List, Literal
from app.schemas.analysis import (
    DetectedIndicator,
    CategoryScores,
    AnalyzeResponse,
)
from app.core.rules import MESSAGE_RULES
from app.core.url_analyzer import analyze_url
from app.core.fallback_engine import generate_deterministic_explanation


def analyze_scam_content(
    raw_input: str,
    content_type: Literal["message", "url", "screenshot"] = "message",
) -> AnalyzeResponse:
    text = raw_input.strip()
    now_iso = datetime.now(timezone.utc).isoformat()

    if not text:
        return AnalyzeResponse(
            risk_score=0,
            risk_level="SAFE",
            risk_label="No Content Provided",
            summary="Please enter text, a URL, or upload a screenshot to begin analysis.",
            indicators=[],
            category_scores=CategoryScores(),
            analyzed_at=now_iso,
            type=content_type,
        )

    detected_indicators: List[DetectedIndicator] = []
    probabilities: List[float] = []

    cat_scores = {
        "urgency": 0,
        "financial": 0,
        "impersonation": 0,
        "credentials": 0,
        "technical": 0,
        "bait": 0,
    }

    # Determine if text is a direct URL
    first_token = text.split()[0] if text.split() else ""
    is_direct_url = (
        content_type == "url"
        or bool(re.match(r"^(https?://|[a-z0-9-]+\.[a-z]{2,})", first_token, re.IGNORECASE))
    )

    if is_direct_url:
        url_inds, url_probs = analyze_url(text)
        detected_indicators.extend(url_inds)
        probabilities.extend(url_probs)
        cat_scores["technical"] += min(45, len(url_probs) * 15)

    # Check for embedded URLs in message/screenshot text
    embedded_match = re.search(
        r"(https?://[^\s]+|[a-z0-9-]+\.(xyz|top|net|com|org|tk|ml|info)[^\s]*)",
        text,
        re.IGNORECASE,
    )
    if embedded_match and not is_direct_url:
        embedded_url = embedded_match.group(0)
        url_inds, url_probs = analyze_url(embedded_url)
        for ind in url_inds:
            detected_indicators.append(
                DetectedIndicator(
                    rule_id=ind.rule_id,
                    title=f"Embedded Link: {ind.title}",
                    description=ind.description,
                    category=ind.category,
                    severity=ind.severity,
                    impact_percent=ind.impact_percent,
                    matched_snippet=ind.matched_snippet,
                )
            )
            # Dampened probability for embedded links inside messages
            probabilities.append((ind.impact_percent / 100.0) * 0.75)
        cat_scores["technical"] += min(35, len(url_probs) * 12)

    # Run Message Rules
    for rule in MESSAGE_RULES:
        if rule.test(text, {"is_url": is_direct_url}):
            probabilities.append(rule.probability)
            cat_scores[rule.category] += round(rule.probability * 100)

            severity: Literal["low", "medium", "high", "critical"] = (
                "critical"
                if rule.probability >= 0.36
                else "high"
                if rule.probability >= 0.30
                else "medium"
                if rule.probability >= 0.22
                else "low"
            )

            detected_indicators.append(
                DetectedIndicator(
                    rule_id=rule.id,
                    title=rule.name,
                    description=rule.description,
                    category=rule.category,
                    severity=severity,
                    impact_percent=round(rule.probability * 100),
                )
            )

    # ---------------------------------------------------------
    # CONTINUOUS MULTI-FACTOR PROBABILISTIC SCORING ENGINE
    # Eliminates flat numbers and static ceilings (no artificial 96% cap).
    # Evaluates stylistic coercion (caps, exclamations, density) and
    # continuous non-linear attack synergy.
    # ---------------------------------------------------------
    letters = [c for c in text if c.isalpha()]
    caps_count = sum(1 for c in letters if c.isupper())
    caps_ratio = (caps_count / len(letters)) if len(letters) > 8 else 0.0
    exclamations = len(re.findall(r"[!?]", text))
    words = text.split()
    word_count = len(words)

    final_score = 0
    if len(detected_indicators) == 0:
        has_legit_domain = bool(
            re.search(
                r"\b(google\.com|github\.com|microsoft\.com|apple\.com|linkedin\.com|amazon\.com)\b",
                text,
                re.IGNORECASE,
            )
        )
        has_formal_greeting = bool(
            re.search(r"\b(dear|hello|hi|sincerely|regards|team|cheers|best)\b", text, re.IGNORECASE)
        )
        avg_word_len = sum(len(w) for w in words) / max(1, len(words))

        clean_score = 6.0
        if has_legit_domain:
            clean_score = 3.2 + (len(text) % 3) * 0.9
        elif has_formal_greeting:
            clean_score = 4.5 + (len(words) % 4) * 0.8
        else:
            clean_score = 6.0 + (len(text) % 5) * 1.0

        if avg_word_len > 5 and clean_score > 3:
            clean_score -= 0.6
        if "?" in text:
            clean_score += 0.4
        final_score = int(round(max(2, min(12, clean_score))))
    else:
        # 1. Uncombined survival probability
        non_threat_prob = 1.0
        for p in probabilities:
            non_threat_prob *= 1.0 - min(0.85, max(0.08, p))

        combined_risk = 1.0 - non_threat_prob

        # 2. Continuous Multi-Category Attack Synergy Factor
        active_categories = {ind.category for ind in detected_indicators}
        category_count = len(active_categories)

        synergy_boost = 0.0
        if category_count >= 5:
            synergy_boost = 0.125
        elif category_count == 4:
            synergy_boost = 0.090
        elif category_count == 3:
            synergy_boost = 0.058
        elif category_count == 2:
            synergy_boost = 0.028

        boosted_risk = 1.0 - (1.0 - combined_risk) * (1.0 - synergy_boost)

        # 3. Dynamic Stylistic & Threat-Density Fine-Tuning
        dynamic_delta = 0.0
        if caps_ratio > 0.35:
            dynamic_delta += 0.022
        elif caps_ratio > 0.20:
            dynamic_delta += 0.010

        if exclamations >= 2:
            dynamic_delta += 0.016
        elif exclamations == 1:
            dynamic_delta += 0.006

        if word_count > 0 and word_count < 18 and category_count >= 3:
            dynamic_delta += 0.018

        boosted_risk += dynamic_delta

        # Natural continuous bounds from 18% up to 98% (no artificial 96% ceiling!)
        final_score = int(round(min(0.98, max(0.18, boosted_risk)) * 100))

    # Determine Risk Tier
    risk_level: Literal["SAFE", "LOW_RISK", "SUSPICIOUS", "HIGH_RISK", "CRITICAL_THREAT"] = "SAFE"
    risk_label = "Safe / Low Threat"

    if final_score >= 80:
        risk_level = "CRITICAL_THREAT"
        risk_label = "Critical Threat Detected"
    elif final_score >= 60:
        risk_level = "HIGH_RISK"
        risk_label = "High Scam Risk"
    elif final_score >= 35:
        risk_level = "SUSPICIOUS"
        risk_label = "Suspicious / Caution Advised"
    elif final_score >= 18:
        risk_level = "LOW_RISK"
        risk_label = "Low Risk / Minor Warnings"

    fallback_explanation = generate_deterministic_explanation(
        final_score, risk_level, detected_indicators
    )

    return AnalyzeResponse(
        risk_score=final_score,
        risk_level=risk_level,
        risk_label=risk_label,
        summary=fallback_explanation.summary,
        indicators=detected_indicators,
        category_scores=CategoryScores(**cat_scores),
        explanation=fallback_explanation,
        analyzed_at=now_iso,
        type=content_type,
    )
