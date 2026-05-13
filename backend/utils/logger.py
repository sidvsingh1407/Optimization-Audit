import logging
import json
import uuid
import time
from datetime import datetime
from backend.config.settings import LOG_LEVEL

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName
        }

        # Merge extra attributes (like execution_id, stage, duration)
        if hasattr(record, "execution_id"):
            log_obj["execution_id"] = record.execution_id
        if hasattr(record, "stage"):
            log_obj["stage"] = record.stage
        if hasattr(record, "duration_ms"):
            log_obj["duration_ms"] = record.duration_ms
        if hasattr(record, "validation_outcomes"):
            log_obj["validation_outcomes"] = record.validation_outcomes
        if hasattr(record, "failure_reason"):
            log_obj["failure_reason"] = record.failure_reason
        if hasattr(record, "runtime_metadata"):
            log_obj["runtime_metadata"] = record.runtime_metadata

        return json.dumps(log_obj)

def get_logger(name="ai_audit_os"):
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers if logger is already configured
    if not logger.handlers:
        logger.setLevel(LOG_LEVEL)

        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())

        logger.addHandler(handler)

    return logger

def generate_execution_id() -> str:
    """Generate a unique ID for tracing a deterministic execution pipeline run."""
    return f"exec_{uuid.uuid4().hex[:12]}"

class TraceContext:
    def __init__(self, logger, execution_id: str, stage: str):
        self.logger = logger
        self.execution_id = execution_id
        self.stage = stage
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"Starting stage: {self.stage}", extra={"execution_id": self.execution_id, "stage": self.stage})
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = int((time.time() - self.start_time) * 1000)

        if exc_type:
            self.logger.error(f"Stage failed: {self.stage}", extra={
                "execution_id": self.execution_id,
                "stage": self.stage,
                "duration_ms": duration_ms,
                "failure_reason": str(exc_val)
            })
            return False # Let exception propagate

        self.logger.info(f"Completed stage: {self.stage}", extra={
            "execution_id": self.execution_id,
            "stage": self.stage,
            "duration_ms": duration_ms
        })
