"""
Deterministic mapping of common AI tools to operational characteristics.
"""

TOOL_CATALOG = {
    "chatgpt": {
        "category": "General Purpose LLM",
        "compliance_impact": "High", # Processes raw user input
        "spend_tier": "Medium",
        "governance_required": ["Data Privacy Policy", "Vendor Approval"]
    },
    "copilot": {
        "category": "Code Assistant",
        "compliance_impact": "Medium", # Processes IP
        "spend_tier": "High",
        "governance_required": ["IP Protection Policy"]
    },
    "github copilot": {
        "category": "Code Assistant",
        "compliance_impact": "Medium",
        "spend_tier": "High",
        "governance_required": ["IP Protection Policy"]
    },
    "jasper": {
        "category": "Copywriting",
        "compliance_impact": "Low", # Mostly public marketing copy
        "spend_tier": "Medium",
        "governance_required": ["Brand Guidelines"]
    },
    "midjourney": {
        "category": "Image Generation",
        "compliance_impact": "Medium", # Copyright issues
        "spend_tier": "Low",
        "governance_required": ["Copyright Policy"]
    },
    "notion ai": {
        "category": "Productivity / Knowledge Management",
        "compliance_impact": "High",
        "spend_tier": "Medium",
        "governance_required": ["Data Privacy Policy"]
    },
    "claude": {
        "category": "General Purpose LLM",
        "compliance_impact": "High",
        "spend_tier": "Medium",
        "governance_required": ["Data Privacy Policy", "Vendor Approval"]
    },
    "gemini": {
        "category": "General Purpose LLM",
        "compliance_impact": "High",
        "spend_tier": "Medium",
        "governance_required": ["Data Privacy Policy", "Vendor Approval"]
    },
    # Default fallback
    "unknown": {
        "category": "Unclassified AI Tool",
        "compliance_impact": "Unknown",
        "spend_tier": "Unknown",
        "governance_required": ["General AI Policy"]
    }
}
