import logging
import json
from datetime import datetime
from typing import Any, Dict
from backend.contracts.events import TraceLoggedEvent
from backend.persistence.database import log_event

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName
        }
        if hasattr(record, "execution_id"):
            log_obj["execution_id"] = record.execution_id
        if hasattr(record, "metadata"):
            log_obj["metadata"] = record.metadata

        return json.dumps(log_obj)

def setup_logger():
    logger = logging.getLogger("audit_system")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def get_logger():
    return logging.getLogger("audit_system")

class ExecutionTracer:
    def __init__(self, execution_id: str):
        self.execution_id = execution_id
        self.logger = get_logger()

    def log_trace(self, message: str, level: str = "INFO", **kwargs):
        """Structured logging of standard traces"""
        extra = {"execution_id": self.execution_id, "metadata": kwargs}
        if level.upper() == "INFO":
            self.logger.info(message, extra=extra)
        elif level.upper() == "WARNING":
            self.logger.warning(message, extra=extra)
        elif level.upper() == "ERROR":
            self.logger.error(message, extra=extra)
        else:
            self.logger.debug(message, extra=extra)

        # Write high value traces into the persistence event log
        event = TraceLoggedEvent(
            execution_id=self.execution_id,
            level=level,
            message=message,
            metadata=kwargs
        )
        log_event(event)
