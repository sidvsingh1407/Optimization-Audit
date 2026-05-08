import pytest
from scoring_engine import (
    response_to_points,
    calculate_dimension_score,
    check_compliance_risk,
    detect_contradictions,
    calculate_scores
)

def test_response_to_points():
    """Test point mapping for specific answers."""
    assert response_to_points('a') == 20
    assert response_to_points('b') == 15
    assert response_to_points('e') == 0
    assert response_to_points('A') == 20
    assert response_to_points('z') == 0  # Invalid maps to 0

def test_calculate_dimension_score_complete():
    """Test deterministic scoring with fully answered dimensions."""
    responses = {'q1_1': 'a', 'q1_2': 'b', 'q1_3': 'c'}
    score, has_missing = calculate_dimension_score(responses, 'awareness')
    # (20 + 15 + 10) / 3 = 15
    assert score == 15
    assert not has_missing

def test_calculate_dimension_score_missing():
    """Test scoring logic when values are missing."""
    responses = {'q1_1': 'a', 'q1_2': 'b'} # q1_3 is missing
    score, has_missing = calculate_dimension_score(responses, 'awareness')
    # (20 + 15) / 2 * 1.5 = 26.25 -> 26
    assert score == 26
    assert has_missing

    empty_responses = {}
    score_empty, missing_empty = calculate_dimension_score(empty_responses, 'awareness')
    assert score_empty == 0
    assert missing_empty

def test_check_compliance_risk():
    """Test compliance risk triggers deterministically."""
    # Safe responses
    safe_responses = {'q4_1': 'a', 'q4_2': 'b', 'q4_3': 'a'}
    has_risk, reasons = check_compliance_risk(safe_responses)
    assert not has_risk
    assert not reasons

    # Risky responses
    risky_responses = {'q4_1': 'e', 'q4_2': 'c', 'q4_3': 'd'}
    has_risk, reasons = check_compliance_risk(risky_responses)
    assert has_risk
    assert set(reasons) == {'q4_1', 'q4_3'}

def test_detect_contradictions():
    """Test logic to find contradictions."""
    # High adoption (a/b) but low frequency (d/e)
    responses1 = {'q2_1': 'a', 'q2_3': 'e'}
    contradictions1 = detect_contradictions(responses1)
    assert len(contradictions1) == 1
    assert "High adoption" in contradictions1[0]

    # Deep integration (a) but low tools (d/e)
    responses2 = {'q3_1': 'a', 'q2_2': 'd'}
    contradictions2 = detect_contradictions(responses2)
    assert len(contradictions2) == 1
    assert "Deep integration" in contradictions2[0]

    # No contradictions
    responses_safe = {'q2_1': 'b', 'q2_3': 'b', 'q3_1': 'b', 'q2_2': 'b'}
    contradictions_safe = detect_contradictions(responses_safe)
    assert len(contradictions_safe) == 0

def test_calculate_scores_integration():
    """Test full score calculation deterministically."""
    full_responses = {
        'q1_1': 'a', 'q1_2': 'a', 'q1_3': 'a',  # awareness: 20
        'q2_1': 'b', 'q2_2': 'b', 'q2_3': 'b',  # adoption: 15
        'q3_1': 'c', 'q3_2': 'c', 'q3_3': 'c',  # integration: 10
        'q4_1': 'e', 'q4_2': 'e', 'q4_3': 'e',  # governance: 0 (and triggers compliance flag)
        'q5_1': 'a', 'q5_2': 'b', 'q5_3': 'c',  # roi: (20+15+10)/3 = 15
    }

    result = calculate_scores(full_responses)

    assert result['dimensions']['awareness'] == 20
    assert result['dimensions']['adoption'] == 15
    assert result['dimensions']['integration'] == 10
    assert result['dimensions']['governance'] == 0
    assert result['dimensions']['roi'] == 15

    assert result['total_score'] == 60
    assert result['rating'] == 'AI Adopting'
    assert result['compliance_risk_flag'] is True
    assert set(result['compliance_risk_reasons']) == {'q4_1', 'q4_2', 'q4_3'}
    assert len(result['missing_data_flags']) == 0
