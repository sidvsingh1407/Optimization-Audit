import pytest
from extraction_validator import validate_extraction

def test_valid_extraction():
    """Test a fully correct schema extraction."""
    valid_data = {
        'company_name': 'TestCorp',
        'industry': 'SaaS',
        'employee_count': '50-99',
        'responses': {f"q{i}_{j}": "a" for i in range(1, 6) for j in range(1, 4)}
    }

    result = validate_extraction(valid_data)

    assert result['is_valid'] is True
    assert len(result['missing_fields']) == 0
    assert result['validated_data']['company_name'] == 'TestCorp'

def test_missing_root_fields():
    """Test structured validation failure on root fields."""
    invalid_data = {
        'industry': 'SaaS',
        'responses': {}
    }

    result = validate_extraction(invalid_data)

    assert result['is_valid'] is False
    assert 'company_name' in result['missing_fields']
    assert 'employee_count' in result['missing_fields']

def test_missing_question_responses():
    """Test conversational extraction fallback and detection for missing question mappings."""
    invalid_data = {
        'company_name': 'TestCorp',
        'industry': 'SaaS',
        'employee_count': '50-99',
        'responses': {
            'q1_1': 'a'
            # Missing everything else
        }
    }

    result = validate_extraction(invalid_data)

    assert result['is_valid'] is False
    assert 'responses.q1_2' in result['missing_fields']

    # Verify fallback provides defaults
    assert result['validated_data']['responses']['q1_2'] == 'e'

def test_malformed_extraction():
    """Test handling of completely malformed extraction."""
    malformed_data = {
        'foo': 'bar'
    }

    result = validate_extraction(malformed_data)

    assert result['is_valid'] is False
    # Ensure it caught missing root fields and missing responses dictionary
    assert 'company_name' in result['missing_fields']
    assert result['validated_data']['company_name'] == 'Unknown'
