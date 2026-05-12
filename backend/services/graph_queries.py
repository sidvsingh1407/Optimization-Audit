import networkx as nx
from typing import Dict, Any, List

def get_tool_ecosystem(G: nx.DiGraph) -> List[Dict[str, Any]]:
    """Returns a summary of tools, their departments, and workflows."""
    ecosystem = []
    tools = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'tool']

    for tool in tools:
        tool_name = G.nodes[tool].get('name', 'Unknown Tool')

        # Find departments
        departments = []
        for pred in G.predecessors(tool):
            if G.edges[pred, tool].get('type') == 'operates_tool' and G.nodes[pred].get('type') == 'department':
                departments.append(G.nodes[pred].get('name'))

        # Find workflows
        workflows = []
        for succ in G.successors(tool):
            if G.edges[tool, succ].get('type') == 'supports_workflow' and G.nodes[succ].get('type') == 'workflow':
                workflows.append(G.nodes[succ].get('name'))

        ecosystem.append({
            "tool": tool_name,
            "departments": departments,
            "workflows": workflows
        })

    return ecosystem

def get_governance_summary(G: nx.DiGraph) -> Dict[str, Any]:
    """Returns governance score and risk level for the audit."""
    gov_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'governance']
    if not gov_nodes:
        return {"score": "N/A", "risk_level": "N/A"}

    gov_node = gov_nodes[0]
    return {
        "score": G.nodes[gov_node].get('score', 'N/A'),
        "risk_level": G.nodes[gov_node].get('risk_level', 'N/A')
    }

def get_risk_concentrations(G: nx.DiGraph) -> List[Dict[str, Any]]:
    """Returns compliance exposures linked to workflows and tools."""
    concentrations = []
    exposures = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'compliance_exposure']

    for exp in exposures:
        exp_name = G.nodes[exp].get('name', 'Unknown Exposure')

        # Find tools creating this exposure
        tools = []
        for pred in G.predecessors(exp):
            if G.edges[pred, exp].get('type') == 'creates_exposure':
                tools.append(G.nodes[pred].get('name'))

        concentrations.append({
            "exposure": exp_name,
            "tools_involved": tools
        })

    return concentrations

def get_workflow_dependencies(G: nx.DiGraph) -> List[Dict[str, Any]]:
    """Returns a summary of workflows and their dependent tools."""
    wf_deps = []
    workflows = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'workflow']

    for wf in workflows:
        wf_name = G.nodes[wf].get('name', 'Unknown Workflow')

        # Find tools supporting this workflow
        tools = []
        for pred in G.predecessors(wf):
            if G.edges[pred, wf].get('type') == 'supports_workflow':
                tools.append(G.nodes[pred].get('name'))

        wf_deps.append({
            "workflow": wf_name,
            "tools_supporting": tools
        })

    return wf_deps
