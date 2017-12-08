"""custom logrecord"""
import logging

def slack_log_factory(*args, **kwargs) -> logging.LogRecord:
    old_factory = logging.getLogRecordFactory()
    record = old_factory(*args, **kwargs)
    return record