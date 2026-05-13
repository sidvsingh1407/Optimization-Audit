import time
from typing import Dict, Any, List, Optional
from backend.utils.logger import generate_execution_id, get_logger
from backend.contracts.audit import AuditInputContract, AuditScoreResult, ExecutionTraceContract

logger = get_logger()

class ExecutionContext:
    def __init__(self, raw_input: Dict[str, Any]):
        self.execution_id: str = generate_execution_id()
        self.current_stage: str = "INITIALIZATION"
        self.start_time: float = time.time()
        self.raw_input: Dict[str, Any] = raw_input
        self.audit_id: Optional[int] = None

        # Stages logic state
        self.contract: Optional[AuditInputContract] = None
        self.scores: Optional[AuditScoreResult] = None
        self.agent_findings: Dict[str, Any] = {}
        self.report_path: Optional[str] = None

        # Governance and traceability stats
        self.validation_state: Dict[str, Any] = {"status": "pending"}
        self.governance_flags: int = 0
        self.relationships_created: int = 0
        self.entity_count: int = 0
        self.trace_logs: List[ExecutionTraceContract] = []
        self.runtime_metadata: Dict[str, Any] = {}

    def transition(self, new_stage: str, status: str = "success", metadata: Dict[str, Any] = None):
        """Record the state transition and tracing."""
        self.current_stage = new_stage
        duration_ms = int((time.time() - self.start_time) * 1000)
        trace = ExecutionTraceContract(
            execution_id=self.execution_id,
            audit_id=self.audit_id,
            stage=self.current_stage,
            status=status,
            duration_ms=duration_ms,
            validation_outcomes=self.validation_state,
            governance_flags=self.governance_flags,
            relationships_created=self.relationships_created,
            entity_count=self.entity_count,
            metadata=metadata or {}
        )
        self.trace_logs.append(trace)

        # We don't necessarily log the entire contract trace here,
        # as logger.TraceContext will handle stage entry/exit logs.
        # But this trace list serves as the operational lineage to persist.

    def generate_trace_summary(self) -> Dict[str, Any]:
        """Output the final summary of the execution context."""
        duration_ms = int((time.time() - self.start_time) * 1000)
        return {
            "execution_id": self.execution_id,
            "audit_id": self.audit_id,
            "final_stage": self.current_stage,
            "entity_count": self.entity_count,
            "relationships_created": self.relationships_created,
            "risk_flags": self.governance_flags,
            "duration_ms": duration_ms,
            "validation_state": self.validation_state
        }
