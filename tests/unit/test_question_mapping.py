import pytest
from scoring_engine import DIMENSION_QUESTIONS, RESPONSE_POINTS

def test_dimension_mappings_exist():
    """Ensure q1_1 through q5_3 mappings exist correctly."""
    assert 'awareness' in DIMENSION_QUESTIONS
    assert 'adoption' in DIMENSION_QUESTIONS
    assert 'integration' in DIMENSION_QUESTIONS
    assert 'governance' in DIMENSION_QUESTIONS
    assert 'roi' in DIMENSION_QUESTIONS

    assert DIMENSION_QUESTIONS['awareness'] == ['q1_1', 'q1_2', 'q1_3']
    assert DIMENSION_QUESTIONS['adoption'] == ['q2_1', 'q2_2', 'q2_3']
    assert DIMENSION_QUESTIONS['integration'] == ['q3_1', 'q3_2', 'q3_3']
    assert DIMENSION_QUESTIONS['governance'] == ['q4_1', 'q4_2', 'q4_3']
    assert DIMENSION_QUESTIONS['roi'] == ['q5_1', 'q5_2', 'q5_3']

def test_response_points_integrity():
    """Ensure scoring-compatible options remain valid."""
    assert RESPONSE_POINTS['a'] == 20
    assert RESPONSE_POINTS['b'] == 15
    assert RESPONSE_POINTS['c'] == 10
    assert RESPONSE_POINTS['d'] == 5
    assert RESPONSE_POINTS['e'] == 0

    assert RESPONSE_POINTS['A'] == 20
    assert RESPONSE_POINTS['E'] == 0
