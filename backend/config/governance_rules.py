"""
Deterministic rules for evaluating governance maturity from audit responses.
"""

def evaluate_governance(responses: dict) -> dict:
    q4_1 = responses.get("q4_1", "e").lower()
    q4_2 = responses.get("q4_2", "e").lower()
    q4_3 = responses.get("q4_3", "e").lower()

    policy_status = "None"
    if q4_1 == "a":
        policy_status = "Comprehensive"
    elif q4_1 == "b":
        policy_status = "Basic"
    elif q4_1 == "c":
        policy_status = "Drafting"
    elif q4_1 == "d":
        policy_status = "Informal"

    privacy_status = "Weak"
    if q4_2 in ["a", "b"]:
        privacy_status = "Strong"
    elif q4_2 == "c":
        privacy_status = "Moderate"

    eu_ai_act = "Unaware"
    if q4_3 in ["a", "b"]:
        eu_ai_act = "Prepared"
    elif q4_3 == "c":
        eu_ai_act = "Aware"

    maturity = 0
    maturity += {"a": 40, "b": 30, "c": 20, "d": 10, "e": 0}.get(q4_1, 0)
    maturity += {"a": 30, "b": 25, "c": 15, "d": 5, "e": 0}.get(q4_2, 0)
    maturity += {"a": 30, "b": 20, "c": 10, "d": 5, "e": 0}.get(q4_3, 0)

    gaps = []
    if q4_1 in ["d", "e"]:
        gaps.append("Missing formal AI usage policy")
    if q4_2 in ["d", "e"]:
        gaps.append("Weak data privacy controls for AI inputs")
    if q4_3 in ["d", "e"]:
        gaps.append("Unprepared for upcoming AI regulations (EU AI Act)")

    return {
        "policy_status": policy_status,
        "privacy_status": privacy_status,
        "eu_ai_act_readiness": eu_ai_act,
        "maturity_score": maturity,
        "gaps": gaps
    }
