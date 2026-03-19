"""
Structured logging utility.
"""
import logging
import json
import sys
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "service": getattr(record, "service", "unknown"),
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra_data"):
            log_data["data"] = record.extra_data
        return json.dumps(log_data)


def get_logger(service_name: str) -> logging.Logger:
    """Get a structured logger for a service."""
    logger = logging.getLogger(service_name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    logger = logging.LoggerAdapter(logger, {"service": service_name})
    return logger
