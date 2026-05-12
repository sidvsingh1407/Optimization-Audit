import pytest
from backend.models.graph_entities import GraphEntity, GraphRelationship
from backend.config.relationship_rules import get_tool_mapping, get_governance_risk_level

def test_tool_mapping():
    mapping = get_tool_mapping("ChatGPT")
    assert "Knowledge Work" in mapping["departments"]
    assert "Customer Communication" in mapping["workflows"]

    mapping_unknown = get_tool_mapping("UnknownTool")
    assert mapping_unknown["governance_exposure"] == "unknown"

def test_governance_risk_level():
    assert get_governance_risk_level(5) == "critical"
    assert get_governance_risk_level(10) == "high"
    assert get_governance_risk_level(15) == "medium"
    assert get_governance_risk_level(18) == "low"
