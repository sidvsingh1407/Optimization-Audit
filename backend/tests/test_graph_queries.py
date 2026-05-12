import pytest
import networkx as nx
from backend.services.graph_queries import get_tool_ecosystem, get_governance_summary, get_risk_concentrations, get_workflow_dependencies

def test_queries():
    G = nx.DiGraph()
    G.add_node("tool_1", type="tool", name="ChatGPT")
    G.add_node("dept_1", type="department", name="Marketing")
    G.add_node("wf_1", type="workflow", name="Content")
    G.add_node("gov_1", type="governance", score=8, risk_level="high")
    G.add_node("exp_1", type="compliance_exposure", name="IP Risk")

    G.add_edge("dept_1", "tool_1", type="operates_tool")
    G.add_edge("tool_1", "wf_1", type="supports_workflow")
    G.add_edge("tool_1", "exp_1", type="creates_exposure")

    ecosystem = get_tool_ecosystem(G)
    assert len(ecosystem) == 1
    assert ecosystem[0]["tool"] == "ChatGPT"
    assert "Marketing" in ecosystem[0]["departments"]
    assert "Content" in ecosystem[0]["workflows"]

    gov = get_governance_summary(G)
    assert gov["score"] == 8
    assert gov["risk_level"] == "high"

    risks = get_risk_concentrations(G)
    assert len(risks) == 1
    assert "IP Risk" in risks[0]["exposure"]
    assert "ChatGPT" in risks[0]["tools_involved"]

    deps = get_workflow_dependencies(G)
    assert len(deps) == 1
    assert deps[0]["workflow"] == "Content"
    assert "ChatGPT" in deps[0]["tools_supporting"]
