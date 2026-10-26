import sys
import os

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.engine import analyze_scam_content

BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"

TEST_CASES = [
    {
        "name": 'User Hackathon Message: "Congratulations! You\'ve won ₹50,000. Click now."',
        "type": "message",
        "input": "Congratulations! You've won ₹50,000. Click now.",
        "expected_min": 70,
        "expected_max": 89,
    },
    {
        "name": 'User Hackathon URL: "amazon-prize-2026.net"',
        "type": "url",
        "input": "amazon-prize-2026.net",
        "expected_min": 72,
        "expected_max": 84,
    },
    {
        "name": "Fake SBI KYC Urgent SMS",
        "type": "message",
        "input": "Dear SBI User, your account will be suspended within 24 hours due to pending KYC. Click immediately: http://sbi-kyc-verify.xyz",
        "expected_min": 85,
        "expected_max": 96,
    },
    {
        "name": 'Mild Urgency Single Word: "Please note this is urgent for our meeting"',
        "type": "message",
        "input": "Please note this is urgent for our meeting tomorrow.",
        "expected_min": 22,
        "expected_max": 40,
    },
    {
        "name": "Telegram Work-From-Home Scam",
        "type": "message",
        "input": "Part-time job offer! Earn ₹8,000 daily by liking YouTube videos. Deposit ₹1,500 security fee to start. Join t.me/fast_earn",
        "expected_min": 80,
        "expected_max": 92,
    },
    {
        "name": "Clean Legitimate Notification: GitHub Alert",
        "type": "message",
        "input": "GitHub Security: A new personal access token was generated. Review your active sessions at https://github.com/settings/tokens",
        "expected_min": 2,
        "expected_max": 10,
    },
    {
        "name": "Clean Personal Message: Lunch Invitation",
        "type": "message",
        "input": "Hey Neer, are we still meeting for lunch at 1pm tomorrow near the cafe?",
        "expected_min": 4,
        "expected_max": 12,
    },
    {
        "name": "Clean Corporate Email: Quarterly Report",
        "type": "message",
        "input": "Dear Team, Please find attached the quarterly analytics report for your review. Regards, Neer",
        "expected_min": 3,
        "expected_max": 10,
    },
]


def test_all_calibrated_scenarios():
    for tc in TEST_CASES:
        res = analyze_scam_content(tc["input"], tc["type"])
        assert tc["expected_min"] <= res.risk_score <= tc["expected_max"], (
            f"Failed on '{tc['name']}': score {res.risk_score}% not in range [{tc['expected_min']}, {tc['expected_max']}]"
        )


def run_cli_suite():
    print(f"{BOLD}{CYAN}================================================================{RESET}")
    print(f"{BOLD}{CYAN}🛡️  SCAMSHIELD PYTHON - CALIBRATED RISK SCORING VERIFICATION  🛡️{RESET}")
    print(f"{BOLD}{CYAN}================================================================{RESET}\n")

    all_passed = True

    for idx, tc in enumerate(TEST_CASES):
        print(f"{BOLD}Test #{idx + 1}: {tc['name']}{RESET}")
        print(f'Input: "{tc["input"]}"')

        res = analyze_scam_content(tc["input"], tc["type"])

        print(f"Calculated Score: {BOLD}{res.risk_score}%{RESET} | Tier: {res.risk_label}")
        print(f"Detected Indicators ({len(res.indicators)}):")
        for ind in res.indicators:
            print(f"  ✓ [{ind.severity.upper()}] {ind.title} (+{ind.impact_percent}%)")

        if res.risk_score < tc["expected_min"] or res.risk_score > tc["expected_max"]:
            print(
                f"{RED}❌ FAILED: Score {res.risk_score}% is outside expected range [{tc['expected_min']}% - {tc['expected_max']}%]{RESET}"
            )
            all_passed = False
        else:
            print(
                f"{GREEN}✅ PASSED (Within realistic target range {tc['expected_min']}%-{tc['expected_max']}%){RESET}"
            )
        print()

    print(f"{BOLD}{CYAN}----------------------------------------------------------------{RESET}")
    if all_passed:
        print(f"{BOLD}{GREEN}🎉 ALL CALIBRATED PYTHON RISK SCORING TESTS PASSED PERFECTLY!{RESET}")
    else:
        print(f"{BOLD}{RED}⚠️ SOME CALIBRATION TESTS FAILED!{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    run_cli_suite()
