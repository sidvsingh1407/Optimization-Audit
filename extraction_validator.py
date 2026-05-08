from typing import Dict, Any, List

def validate_extraction(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates structured conversational extraction data against the expected schema.
    Returns a dictionary with 'is_valid', 'validated_data', and 'missing_fields'.
    """
    required_fields = ['company_name', 'industry', 'employee_count']
    expected_questions = [f"q{i}_{j}" for i in range(1, 6) for j in range(1, 4)]

    missing_fields = []

    # Check root required fields
    for field in required_fields:
        if field not in extracted_data or not extracted_data[field]:
            missing_fields.append(field)

    responses = extracted_data.get('responses', {})
    if not isinstance(responses, dict):
        responses = {}
        missing_fields.append("responses")

    # Check questions
    for q in expected_questions:
        if q not in responses or not responses[q]:
            missing_fields.append(f"responses.{q}")

    is_valid = len(missing_fields) == 0

    # Provide fallback mapping or safe extraction
    validated_data = {
        'company_name': extracted_data.get('company_name', 'Unknown'),
        'industry': extracted_data.get('industry', 'Unknown'),
        'employee_count': extracted_data.get('employee_count', 'Unknown'),
        'responses': {q: responses.get(q, 'e') for q in expected_questions} # Default missing to 'e'
    }

    return {
        'is_valid': is_valid,
        'missing_fields': missing_fields,
        'validated_data': validated_data
    }
