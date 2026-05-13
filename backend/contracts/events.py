from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class BaseEvent(BaseModel):
    schema_version: str = Field(default="1.0.0")
    event_version: str = Field(default="1.0.0")
    event_type: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    execution_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AuditStartedEvent(BaseEvent):
    event_type: str = "audit.started"
    company_name: str

class AuditValidatedEvent(BaseEvent):
    event_type: str = "audit.validated"

class AuditFailedEvent(BaseEvent):
    event_type: str = "audit.failed"
    error_message: str

class WorkflowAnalyzedEvent(BaseEvent):
    event_type: str = "workflow.analyzed"

class GovernanceMappedEvent(BaseEvent):
    event_type: str = "governance.mapped"

class RelationshipCreatedEvent(BaseEvent):
    event_type: str = "relationship.created"

class RiskScoredEvent(BaseEvent):
    event_type: str = "risk.scored"
    risk_level: str

class ReportGeneratedEvent(BaseEvent):
    event_type: str = "report.generated"
    report_path: str

class PersistenceCompletedEvent(BaseEvent):
    event_type: str = "persistence.completed"

class TraceLoggedEvent(BaseEvent):
    event_type: str = "trace.logged"
    level: str = "INFO"
    message: str
