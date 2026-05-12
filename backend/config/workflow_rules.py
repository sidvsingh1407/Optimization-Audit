"""
Deterministic mapping of workflows based on industry and tool usage.
"""

def infer_workflows(industry: str, tools: list) -> list:
    workflows = []

    if any(t.get("category") == "General Purpose LLM" for t in tools):
        workflows.append({
            "name": "General Knowledge & Drafting",
            "department": "Cross-functional",
            "tools_used": [t["name"] for t in tools if t.get("category") == "General Purpose LLM"],
            "criticality": "Medium"
        })

    if any(t.get("category") == "Code Assistant" for t in tools):
        workflows.append({
            "name": "Software Development",
            "department": "Engineering",
            "tools_used": [t["name"] for t in tools if t.get("category") == "Code Assistant"],
            "criticality": "High"
        })

    if any(t.get("category") == "Copywriting" for t in tools) or any(t.get("category") == "Image Generation" for t in tools):
        workflows.append({
            "name": "Content Creation",
            "department": "Marketing",
            "tools_used": [t["name"] for t in tools if t.get("category") in ["Copywriting", "Image Generation"]],
            "criticality": "Medium"
        })

    if industry.lower() in ["saas/technology", "saas"]:
        if "Software Development" not in [w["name"] for w in workflows] and len(tools) > 0:
            workflows.append({
                "name": "Unmanaged Software Development",
                "department": "Engineering",
                "tools_used": [],
                "criticality": "High"
            })

    return workflows
