from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, List, Optional
from datetime import datetime

class AuditInputContract(BaseModel):
    company_name: str = Field(..., description="The name of the company being audited.")
    industry: Optional[str] = Field(default="Unknown")
    employee_count: Optional[str] = Field(default="Unknown")
    contact_name: Optional[str] = Field(default="Unknown")
    contact_email: Optional[str] = Field(default="Unknown")
    benchmark_opt_in: bool = Field(default=False)
    responses: Dict[str, Any] = Field(..., description="The answers to the audit questions and other raw data.")

class GovernanceContract(BaseModel):
    has_ai_policy: bool = Field(default=False)
    has_compliance_officer: bool = Field(default=False)
    eu_ai_act_awareness: str = Field(default="Low")
    gdpr_compliance_status: str = Field(default="Unknown")

class RiskProfileContract(BaseModel):
    overall_risk_level: str = Field(..., pattern="^(low|medium|high|critical)$")
    eu_ai_act_risk: str = Field(default="low")
    gdpr_risk: str = Field(default="low")
    governance_gaps: List[Dict[str, str]] = Field(default_factory=list)
    compliance_deadline: Optional[str] = None
    required_actions: List[str] = Field(default_factory=list)

class RelationshipContract(BaseModel):
    entity_source: str
    entity_target: str
    relationship_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ExecutionTraceContract(BaseModel):
    execution_id: str
    audit_id: Optional[int] = None
    stage: str
    status: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    duration_ms: Optional[int] = None
    validation_outcomes: Dict[str, Any] = Field(default_factory=dict)
    governance_flags: int = 0
    relationships_created: int = 0
    entity_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ScoreDimensions(BaseModel):
    awareness: int = Field(default=0, ge=0, le=20)
    adoption: int = Field(default=0, ge=0, le=20)
    integration: int = Field(default=0, ge=0, le=20)
    governance: int = Field(default=0, ge=0, le=20)
    roi: int = Field(default=0, ge=0, le=20)

class AuditScoreResult(BaseModel):
    dimensions: ScoreDimensions
    total_score: int = Field(default=0, ge=0, le=100)
    rating: str
    compliance_risk_flag: bool = False
    compliance_risk_reasons: List[str] = Field(default_factory=list)

class ReportMetadataContract(BaseModel):
    pdf_path: str
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    executive_summary: str
    top_recommendations: List[Dict[str, Any]]
