import logging
import json
import uuid
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

        # Merge extra attributes (like execution_id)
        if hasattr(record, "execution_id"):
            log_obj["execution_id"] = record.execution_id
        if hasattr(record, "stage"):
            log_obj["stage"] = record.stage

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
