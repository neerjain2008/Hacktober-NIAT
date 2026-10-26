import re
from typing import Callable, List, Literal, Optional
from dataclasses import dataclass


@dataclass
class HeuristicRule:
    id: str
    name: str
    description: str
    category: Literal["urgency", "financial", "impersonation", "credentials", "technical", "bait"]
    probability: float  # Probabilistic threat factor (0.10 to 0.45)
    test: Callable[[str, Optional[dict]], bool]


MESSAGE_RULES: List[HeuristicRule] = [
    # 1. Urgency & Time Pressure Tactics
    HeuristicRule(
        id="urgency_tactic",
        name="Urgency Pressure Tactic",
        description="Pressures recipient with immediate countdowns, deadlines, or rapid compliance language.",
        category="urgency",
        probability=0.34,
        test=lambda text, context=None: any(
            re.search(p, text, re.IGNORECASE)
            for p in [
                r"\b(urgent|immediately|act now|click now|limited time|hurry|rush|expires today|valid for \d+|within \d+ (hours?|hrs?|minutes?|days?)|do not delay|last chance|final notice)\b",
                r"\b(account (blocked|suspended|disabled|deactivated|frozen|terminated))\b",
                r"\b(legal action|police complaint|arrest warrant|court notice)\b",
            ]
        ),
    ),
    # 2. Call-to-Action / Click Baits
    HeuristicRule(
        id="cta_bait",
        name="Coerced Call-To-Action (Click Lure)",
        description="Aggressive instructions urging victim to click links or tap unverified portals.",
        category="urgency",
        probability=0.30,
        test=lambda text, context=None: any(
            re.search(p, text, re.IGNORECASE)
            for p in [
                r"\b(click now|click here|click below|click link|tap now|tap here|open link|follow link|visit link)\b",
            ]
        ),
    ),
    # 3. Prize Bait & Lottery Lures
    HeuristicRule(
        id="prize_bait",
        name="Prize & Lottery Bait",
        description="Lures victim with unexpected cash prizes, lotteries, lucky draws, or giveaways.",
        category="bait",
        probability=0.40,
        test=lambda text, context=None: any(
            re.search(p, text, re.IGNORECASE)
            for p in [
                r"\b(congratulations|congrats|you('ve| have)? won|winner of|lucky draw|lottery prize|cash reward|jackpot|free gift|unclaimed prize|selected winner)\b",
                r"\b(won ₹|won rs|won \$|won 50,00,0|won 50,000|won 10,000|won 1,00,000|won cash|claim prize|claim reward|claim bonus)\b",
                r"₹\s*[0-9,]+",
            ]
        ),
    ),
    # 4. Financial & Payment Demands
    HeuristicRule(
        id="financial_demand",
        name="Payment / Advance Fee Demand",
        description="Instructs victim to send money, pay processing charges, or settle alleged dues.",
        category="financial",
        probability=0.36,
        test=lambda text, context=None: any(
            re.search(p, text, re.IGNORECASE)
            for p in [
                r"\b(send money|send funds|pay now|deposit fee|processing fee|registration fee|security fee|gas fee|advance fee|transfer amount)\b",
                r"\b(unpaid bill|pending bill|pay bill|clear dues|overdue bill|settle bill)\b",
                r"\b(pay ₹|pay rs|pay \$|deposit ₹|deposit \$|send ₹|send \$)\b",
                r"\b(wire transfer|western union|moneygram|gift card|google play card|apple gift card)\b",
                r"\b(usdt|crypto|bitcoin|ethereum|btc wallet|binance pay)\b",
            ]
        ),
    ),
    # 5. Authority & Brand Impersonation
    HeuristicRule(
        id="impersonation_authority",
        name="Brand / Bank / Authority Impersonation",
        description="Impersonates banks, tech giants, utility providers, couriers, or government agencies.",
        category="impersonation",
        probability=0.35,
        test=lambda text, context=None: (
            False
            if (context and context.get("is_url"))
            else any(
                re.search(p, text, re.IGNORECASE)
                for p in [
                    r"\b(sbi|state bank|hdfc|icici|axis bank|punjab national|pnb|paytm|phonepe|gpay|google pay)\b",
                    r"\b(rbi|reserve bank|income tax department|incometax|customs department|cbi|police department|cyber cell|trai)\b",
                    r"\b(amazon|netflix|microsoft|apple|geek squad|fedex|dhl|india post|courier parcel|delivery pending)\b",
                    r"\b(electricity board|bescom|mseb|tneb|bses|uppcl|power corp)\b",
                    r"\b(kyc (update|expired|pending|verification|document)|link aadhaar|pan card update)\b",
                ]
            )
        ),
    ),
    # 6. Credential & Identity Theft Harvesting
    HeuristicRule(
        id="credentials_harvesting",
        name="Credential & Identity Harvesting",
        description="Solicits sensitive authentication secrets, passwords, OTPs, or government IDs.",
        category="credentials",
        probability=0.38,
        test=lambda text, context=None: any(
            re.search(p, text, re.IGNORECASE)
            for p in [
                r"\b(verify account|verify details|confirm identity|update kyc|update details)\b",
                r"\b(share otp|enter otp|provide pin|atm pin|cvv|netbanking password|secret code|seed phrase)\b",
                r"\b(aadhaar|pan card|ssn|credit card number)\b",
            ]
        ),
    ),
    # 7. Work-From-Home / Daily Task Scam
    HeuristicRule(
        id="job_investment_scam",
        name="Task-Based Job / Daily Income Scam",
        description="Promises unrealistic guaranteed daily earnings for trivial online tasks.",
        category="bait",
        probability=0.35,
        test=lambda text, context=None: any(
            re.search(p, text, re.IGNORECASE)
            for p in [
                r"\b(part-time job|work from home|earn daily|earn ₹[0-9]+|earn \$[0-9]+|daily income)\b",
                r"\b(like youtube|subscribe channel|telegram task|rate hotels|rating task|order grabbing)\b",
                r"\b(double your money|guaranteed return|100% profit|zero risk investment)\b",
            ]
        ),
    ),
    # 8. Suspicious / Unverified Channels
    HeuristicRule(
        id="suspicious_channel",
        name="Off-Platform Redirection (WhatsApp / Telegram / Shortlinks)",
        description="Directs victim off-platform to unmoderated messaging or URL shorteners.",
        category="technical",
        probability=0.24,
        test=lambda text, context=None: any(
            re.search(p, text, re.IGNORECASE)
            for p in [
                r"\b(t\.me\/|wa\.me\/|whatsapp (us|at)|telegram @|chat on telegram|join telegram)\b",
                r"\b(bit\.ly|tinyurl|is\.gd|cutt\.ly|rb\.gy|goo\.gl|t\.co|v\.gd)\b",
                r"@(gmail|yahoo|hotmail|outlook)\.com",
            ]
        ),
    ),
    # 9. Utility & Disconnection Threat / Fake Official Notice
    HeuristicRule(
        id="utility_disconnection",
        name="Utility / Service Disconnection Threat",
        description="Threatens immediate shutoff of electricity, water, gas, or telecom to trigger panic.",
        category="urgency",
        probability=0.35,
        test=lambda text, context=None: any(
            re.search(p, text, re.IGNORECASE)
            for p in [
                r"\b(electricity bill|power supply|electric meter|water bill|gas bill|power cutoff|line disconnected)\b",
                r"\b((will be|is) disconnected (today|tonight|immediately|at \d+))\b",
                r"\b(call (officer|helpline|electricity)|contact (officer|technician))\b",
            ]
        ),
    ),
    # 10. Fake Tech Support / Antivirus Scareware
    HeuristicRule(
        id="tech_support_scareware",
        name="Tech Support Scareware / Device Infection Threat",
        description="Falsely claims device is compromised with trojans or spyware to coerce remote access or phone calls.",
        category="technical",
        probability=0.36,
        test=lambda text, context=None: any(
            re.search(p, text, re.IGNORECASE)
            for p in [
                r"\b(infected with|virus detected|trojan detected|spyware detected|malware alert|security alert)\b",
                r"\b(windows defender alert|apple security alert|system warning|critical alert)\b",
                r"\b(call support|call microsoft|call apple|call toll[- ]?free|call technician)\b",
            ]
        ),
    ),
    # 11. High-Yield Investment & Crypto Doubling Lure
    HeuristicRule(
        id="crypto_investment_lure",
        name="High-Yield Investment / Crypto Doubling Bait",
        description="Promises impossible guaranteed daily profits, automated crypto trading, or airdrop claims.",
        category="bait",
        probability=0.36,
        test=lambda text, context=None: any(
            re.search(p, text, re.IGNORECASE)
            for p in [
                r"\b(crypto trading|guaranteed daily profit|1000x|airdrop claim|trading bot|forex signal|mining returns?)\b",
                r"\b(invest ₹[0-9]+|invest \$[0-9]+|receive \$[0-9]+ daily|receive ₹[0-9]+ daily)\b",
                r"\b(passive daily income|automated profit)\b",
            ]
        ),
    ),
]
