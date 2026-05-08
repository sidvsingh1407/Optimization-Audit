import json
from typing import Dict, Any, List, Optional
from backend.config.question_mapping import get_all_questions

def validate_extraction(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates the extracted data against the deterministic schema.
    Returns a clean dictionary with only valid fields.
    """
    if not extracted_data:
        return {}

    validated = {"responses": {}}

    # Validate multiple choice responses
    extracted_responses = extracted_data.get("responses", {})
    all_qs = get_all_questions()

    for q in all_qs:
        q_id = q["id"]
        val = extracted_responses.get(q_id)
        if val:
            val = str(val).lower()
            if val in ['a', 'b', 'c', 'd', 'e']:
                validated["responses"][q_id] = val

    # Validate spend
    spend = extracted_data.get("monthly_spend")
    if spend in ["< $500", "$500-$2K", "$2K-$10K", "$10K+"]:
        validated["monthly_spend"] = spend

    # Validate tools
    tools = extracted_data.get("tools_used")
    if tools and isinstance(tools, str):
        validated["tools_used"] = tools

    return validated

def get_missing_fields(validated_data: Dict[str, Any]) -> List[str]:
    """
    Returns a list of question IDs and field names that are still missing.
    """
    missing = []

    responses = validated_data.get("responses", {})
    for q in get_all_questions():
        if q["id"] not in responses:
            missing.append(q["id"])

    if "monthly_spend" not in validated_data:
        missing.append("monthly_spend")

    if "tools_used" not in validated_data:
        missing.append("tools_used")

    return missing
