from backend.models.entities import Organization, AITool, ComplianceExposure
from backend.services.governance_mapper import map_governance
from backend.services.workflow_mapper import map_workflows
from backend.services.risk_mapper import calculate_risks
from backend.config.tool_risk_mapping import TOOL_CATALOG
from backend.config.compliance_rules import evaluate_compliance_exposure

def map_organization(audit_data: dict, responses: dict) -> Organization:
    raw_tools = audit_data.get("tools_used") or responses.get("tools_used", "")
    tool_names = [t.strip().lower() for t in raw_tools.split(",") if t.strip()]
    tools = []
    for name in tool_names:
        catalog_info = TOOL_CATALOG.get(name, TOOL_CATALOG["unknown"])
        tools.append(AITool(
            name=name.title(),
            category=catalog_info["category"],
            compliance_impact=catalog_info["compliance_impact"],
            spend_tier=catalog_info["spend_tier"],
            governance_required=catalog_info["governance_required"]
        ))

    governance = map_governance(responses)

    industry = audit_data.get("industry", "Unknown")
    tools_dicts = [t.model_dump() for t in tools]
    workflows = map_workflows(industry, tools_dicts)

    compliance_data = evaluate_compliance_exposure(governance.model_dump(), tools_dicts)
    compliance = ComplianceExposure(**compliance_data)

    risks = calculate_risks(governance, tools, workflows)

    org = Organization(
        company_name=audit_data.get("company_name", "Unknown"),
        industry=industry,
        employee_count=audit_data.get("employee_count", "Unknown"),
        tools=tools,
        workflows=workflows,
        governance=governance,
        compliance=compliance,
        risks=risks
    )

    return org
