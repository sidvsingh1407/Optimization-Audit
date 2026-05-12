# Deterministic operational mappings for graph generation

# Maps common AI tools to generalized departments and workflows
TOOL_ECOSYSTEM_MAP = {
    "chatgpt": {
        "departments": ["Knowledge Work", "Operations"],
        "workflows": ["Customer Communication", "Content Creation", "Data Analysis"],
        "governance_exposure": "high",
        "compliance_linkage": ["Data Privacy", "IP Risk"]
    },
    "chatgpt enterprise": {
        "departments": ["Knowledge Work", "Operations", "IT"],
        "workflows": ["Customer Communication", "Content Creation", "Data Analysis"],
        "governance_exposure": "medium",
        "compliance_linkage": ["IP Risk"]
    },
    "copilot": {
        "departments": ["Engineering", "IT"],
        "workflows": ["Software Development", "Code Review"],
        "governance_exposure": "medium",
        "compliance_linkage": ["IP Risk"]
    },
    "github copilot": {
        "departments": ["Engineering", "IT"],
        "workflows": ["Software Development", "Code Review"],
        "governance_exposure": "medium",
        "compliance_linkage": ["IP Risk"]
    },
    "jasper": {
        "departments": ["Marketing", "Sales"],
        "workflows": ["Content Creation", "Copywriting"],
        "governance_exposure": "low",
        "compliance_linkage": ["Brand Risk"]
    },
    "midjourney": {
        "departments": ["Design", "Marketing"],
        "workflows": ["Asset Creation", "Design Prototyping"],
        "governance_exposure": "low",
        "compliance_linkage": ["Copyright Risk"]
    },
    "notion ai": {
        "departments": ["Operations", "Knowledge Work", "Product"],
        "workflows": ["Documentation", "Knowledge Management"],
        "governance_exposure": "medium",
        "compliance_linkage": ["Data Privacy"]
    },
    "zapier": {
        "departments": ["Operations", "IT"],
        "workflows": ["Automation", "Integration"],
        "governance_exposure": "medium",
        "compliance_linkage": ["Data Flow Risk", "Access Control"]
    }
}

def get_tool_mapping(tool_name: str) -> dict:
    """Safely get mapping for a tool name, falling back to a generic mapping."""
    clean_name = tool_name.strip().lower()
    if clean_name in TOOL_ECOSYSTEM_MAP:
        return TOOL_ECOSYSTEM_MAP[clean_name]

    # Generic fallback mapping for unknown tools
    return {
        "departments": ["General Business"],
        "workflows": ["General Operations"],
        "governance_exposure": "unknown",
        "compliance_linkage": ["General Operational Risk"]
    }

# Mapping between governance score thresholds and risk linkage
def get_governance_risk_level(governance_score: int) -> str:
    if governance_score < 7:
        return "critical"
    elif governance_score < 12:
        return "high"
    elif governance_score < 16:
        return "medium"
    return "low"
