import pytest
from spend_parser import parse_spend_estimate

def test_parse_spend_exact():
    """Test deterministic exact spend parsing."""
    result = parse_spend_estimate("$500")
    assert result['min'] == 500
    assert result['max'] == 500
    assert result['average'] == 500.0

def test_parse_spend_range():
    """Test deterministic range spend parsing."""
    result = parse_spend_estimate("$2K-$10K")
    assert result['min'] == 2000
    assert result['max'] == 10000
    assert result['average'] == 6000.0

def test_parse_spend_less_than():
    """Test deterministic '<' spend parsing."""
    result = parse_spend_estimate("< $500")
    assert result['min'] == 0
    assert result['max'] == 500
    assert result['average'] == 250.0

def test_parse_spend_greater_than():
    """Test deterministic '+' spend parsing."""
    result = parse_spend_estimate("$10K+")
    assert result['min'] == 10000
    assert result['max'] is None
    assert result['average'] == 10000.0

def test_parse_spend_empty_or_invalid():
    """Test invalid or empty spend handling."""
    empty = parse_spend_estimate("")
    assert empty['min'] == 0
    assert empty['max'] == 0

    invalid = parse_spend_estimate("unknown")
    assert invalid['min'] == 0
    assert invalid['max'] == 0
