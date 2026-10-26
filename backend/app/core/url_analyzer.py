import re
from urllib.parse import urlparse
from typing import List, Tuple
from app.schemas.analysis import DetectedIndicator


def analyze_url(raw_url: str) -> Tuple[List[DetectedIndicator], List[float]]:
    indicators: List[DetectedIndicator] = []
    probabilities: List[float] = []
    normalized = raw_url.strip().lower()

    # Clean hostname extraction
    try:
        with_proto = normalized if (normalized.startswith("http://") or normalized.startswith("https://")) else f"https://{normalized}"
        parsed = urlparse(with_proto)
        hostname = parsed.hostname or normalized.replace("https://", "").replace("http://", "").split("/")[0]
    except Exception:
        hostname = re.sub(r"^https?://", "", normalized).split("/")[0]

    # 1. Hyphen abuse check (e.g., amazon-login-update-2026.net)
    hyphen_count = hostname.count("-")
    if hyphen_count >= 1:
        prob = 0.24 if hyphen_count >= 2 else 0.16
        probabilities.append(prob)
        indicators.append(
            DetectedIndicator(
                rule_id="url_hyphens",
                title="Hyphen-Spammed Domain Pattern",
                description=f"Domain contains {hyphen_count} hyphen(s). Scammers frequently use hyphens to mimic authentic brand names.",
                category="technical",
                severity="high" if hyphen_count > 2 else "medium",
                impact_percent=round(prob * 100),
                matched_snippet=hostname,
            )
        )

    # 2. High-risk keywords in URL
    suspicious_keywords = [
        {"word": "login", "prob": 0.22, "title": 'Credential Trap Keyword ("login")'},
        {"word": "verify", "prob": 0.22, "title": 'Phishing Keyword ("verify")'},
        {"word": "update", "prob": 0.18, "title": 'Fake Update Keyword ("update")'},
        {"word": "secure", "prob": 0.18, "title": 'False Security Keyword ("secure")'},
        {"word": "banking", "prob": 0.25, "title": 'Bank Impersonation Keyword ("banking")'},
        {"word": "kyc", "prob": 0.28, "title": 'KYC Bait Keyword ("kyc")'},
        {"word": "prize", "prob": 0.25, "title": 'Lottery Trap Keyword ("prize")'},
        {"word": "winner", "prob": 0.25, "title": 'Winner Lure Keyword ("winner")'},
        {"word": "bonus", "prob": 0.18, "title": 'Bonus Bait Keyword ("bonus")'},
        {"word": "claim", "prob": 0.20, "title": 'Reward Claim Keyword ("claim")'},
        {"word": "wallet", "prob": 0.22, "title": 'Crypto Wallet Target ("wallet")'},
    ]

    for item in suspicious_keywords:
        if item["word"] in normalized:
            prob = item["prob"]
            probabilities.append(prob)
            indicators.append(
                DetectedIndicator(
                    rule_id=f"url_kw_{item['word']}",
                    title=item["title"],
                    description=f"URL contains phishing-associated keyword \"{item['word']}\".",
                    category="credentials",
                    severity="high" if prob >= 0.24 else "medium",
                    impact_percent=round(prob * 100),
                    matched_snippet=item["word"],
                )
            )

    # 3. Numbers in domain (e.g. sbi2026, amazon99, verify01)
    if re.search(r"[0-9]", hostname):
        prob = 0.18
        probabilities.append(prob)
        indicators.append(
            DetectedIndicator(
                rule_id="url_numeric",
                title="Suspicious Numerics in Hostname",
                description="Contains numeric characters in domain name (common in disposable phishing campaign domains).",
                category="technical",
                severity="medium",
                impact_percent=round(prob * 100),
                matched_snippet=hostname,
            )
        )

    # 4. Brand Impersonation in domain
    brands = [
        "amazon", "paypal", "sbi", "hdfc", "icici", "apple", "netflix", "google",
        "microsoft", "whatsapp", "binance", "coinbase", "paytm", "phonepe", "facebook", "instagram"
    ]
    for brand in brands:
        if brand in hostname:
            is_official = (
                hostname == f"{brand}.com"
                or hostname == f"{brand}.co.in"
                or hostname == f"{brand}.in"
                or hostname == f"{brand}.org"
                or hostname.endswith(f".{brand}.com")
                or hostname.endswith(f".{brand}.co.in")
            )

            if not is_official:
                prob = 0.42
                probabilities.append(prob)
                indicators.append(
                    DetectedIndicator(
                        rule_id=f"brand_impersonation_{brand}",
                        title=f"Brand Impersonation Target: {brand.upper()}",
                        description=f"Uses the brand name \"{brand}\" but is NOT hosted on the genuine official domain.",
                        category="impersonation",
                        severity="critical",
                        impact_percent=round(prob * 100),
                        matched_snippet=hostname,
                    )
                )

    # 5. High-risk TLDs
    suspicious_tlds = [
        ".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".gq", ".work",
        ".click", ".buzz", ".club", ".rest", ".icu", ".cam", ".live", ".monster"
    ]
    for tld in suspicious_tlds:
        if hostname.endswith(tld):
            prob = 0.30
            probabilities.append(prob)
            indicators.append(
                DetectedIndicator(
                    rule_id="suspicious_tld",
                    title=f"High-Risk Top-Level Domain ({tld})",
                    description=f"The \"{tld}\" TLD has an unusually high prevalence in malicious phishing campaigns.",
                    category="technical",
                    severity="high",
                    impact_percent=round(prob * 100),
                    matched_snippet=tld,
                )
            )
            break

    # 6. Naked IP address in URL
    if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", hostname):
        prob = 0.40
        probabilities.append(prob)
        indicators.append(
            DetectedIndicator(
                rule_id="naked_ip",
                title="Direct IP Address Host",
                description="URL targets a raw numeric IP address instead of an authenticated domain name.",
                category="technical",
                severity="critical",
                impact_percent=round(prob * 100),
                matched_snippet=hostname,
            )
        )

    return indicators, probabilities
