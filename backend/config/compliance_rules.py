"""
Deterministic mapping for compliance and risk exposure.
"""

def evaluate_compliance_exposure(governance_state: dict, tool_stack: list) -> dict:
    exposure_level = "Low"
    flags = []

    high_impact_tools = [t for t in tool_stack if t.get("compliance_impact", "Unknown") == "High"]

    if high_impact_tools:
        if governance_state.get("privacy_status") in ["Weak", "Moderate"]:
            exposure_level = "High"
            flags.append("High-risk tools in use without strong privacy controls")
        elif governance_state.get("privacy_status") == "Strong":
            exposure_level = "Medium"
            flags.append("High-risk tools in use, but privacy controls are active")

    if governance_state.get("eu_ai_act_readiness") == "Unaware":
        flags.append("Complete lack of EU AI Act readiness")
        if exposure_level != "High":
            exposure_level = "Medium"

    if not tool_stack and governance_state.get("policy_status") == "None":
        flags.append("No policy exists to prevent Shadow AI")
        exposure_level = "Medium"

    return {
        "overall_exposure": exposure_level,
        "flags": flags
    }
