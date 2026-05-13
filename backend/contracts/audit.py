from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class AuditMetadata(BaseModel):
    company_name: str = Field(default="Unknown")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

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

class ExecutionTraceContract(BaseModel):
    execution_id: str
    stage: str
    status: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
