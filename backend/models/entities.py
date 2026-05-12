from pydantic import BaseModel, Field
from typing import List, Optional

class AITool(BaseModel):
    name: str
    category: str
    compliance_impact: str
    spend_tier: str
    governance_required: List[str]

class GovernanceState(BaseModel):
    policy_status: str
    privacy_status: str
    eu_ai_act_readiness: str
    maturity_score: int
    gaps: List[str]

class ComplianceExposure(BaseModel):
    overall_exposure: str
    flags: List[str]

class Workflow(BaseModel):
    name: str
    department: str
    tools_used: List[str]
    criticality: str

class OperationalRisk(BaseModel):
    risk_name: str
    severity: str
    description: str
    linked_workflows: List[str]
    linked_tools: List[str]

class Organization(BaseModel):
    company_name: str
    industry: str
    employee_count: str
    tools: List[AITool]
    workflows: List[Workflow]
    governance: GovernanceState
    compliance: ComplianceExposure
    risks: List[OperationalRisk]
