import pytest
import os
import networkx as nx
from backend.services.graph_builder import build_graph_for_audit, load_graph_from_db
from backend.db.database import get_connection

def test_graph_builder_and_loader():
    audit_id = "test_audit_123"
    audit_data = {
        "company_name": "TestCorp",
        "responses": {
            "tools_used": "ChatGPT, Jasper"
        }
    }
    scores = {
        "dimensions": {
            "governance": 8
        }
    }

    # Build
    build_graph_for_audit(audit_id, audit_data, scores)

    # Load
    G = load_graph_from_db(audit_id)

    # Assert
    assert len(G.nodes) > 0
    assert len(G.edges) > 0

    org_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'org']
    assert len(org_nodes) == 1
    assert G.nodes[org_nodes[0]]['name'] == "TestCorp"

    tool_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'tool']
    tool_names = [G.nodes[n]['name'] for n in tool_nodes]
    assert "ChatGPT" in tool_names
    assert "Jasper" in tool_names
