from backend.models.entities import GovernanceState, Workflow, AITool, OperationalRisk
from typing import List

def calculate_risks(governance: GovernanceState, tools: List[AITool], workflows: List[Workflow]) -> List[OperationalRisk]:
    risks = []

    if len(tools) >= 3 and governance.policy_status in ["None", "Informal"]:
        risks.append(OperationalRisk(
            risk_name="Unmanaged AI Sprawl",
            severity="High",
            description="Multiple AI tools in use without a governing policy.",
            linked_workflows=[w.name for w in workflows],
            linked_tools=[t.name for t in tools]
        ))

    high_impact = [t for t in tools if t.compliance_impact == "High"]
    if high_impact and governance.privacy_status in ["Weak", "Moderate"]:
        risks.append(OperationalRisk(
            risk_name="Data Privacy Exposure",
            severity="High",
            description="High compliance impact tools in use with weak or moderate privacy controls.",
            linked_workflows=[w.name for w in workflows if any(t.name in w.tools_used for t in high_impact)],
            linked_tools=[t.name for t in high_impact]
        ))

    engineering_workflows = [w for w in workflows if w.department == "Engineering"]
    if engineering_workflows and governance.policy_status in ["None", "Informal"]:
        risks.append(OperationalRisk(
            risk_name="Unmanaged Code Generation IP Risk",
            severity="Critical",
            description="Code is being generated using AI without IP protection policies.",
            linked_workflows=[w.name for w in engineering_workflows],
            linked_tools=list(set([t for w in engineering_workflows for t in w.tools_used]))
        ))

    return risks
