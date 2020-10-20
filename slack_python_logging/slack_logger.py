"""main logger"""
import logging
import os
import sys
import traceback


from .formatter import SlackFormatter
from .handler import SlackHandler


def initialize(app_name: str) -> logging.Logger:
    """makes new slack logger"""
    # The logger object to which we will add stream/systemd/slack handlers
    slack_logger: logging.Logger = logging.getLogger(app_name)
    formatter: logging.Formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(lineno)-4s %(message)s'
    )

    # Log everything to stdout/stderr
    stream_handler: logging.Handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    slack_logger.addHandler(stream_handler)

    # Attempt to log to systemd, otherwise log to a file
    try:
        from systemd import journal
    except ImportError:
        file_handler: logging.Handler = logging.FileHandler(f"{app_name}.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        slack_logger.addHandler(file_handler)
    else:
        journal_handler: logging.Handler = journal.JournalHandler(SYSLOG_IDENTIFIER=app_name)
        journal_handler.setLevel(logging.DEBUG)
        journal_handler.setFormatter(formatter)
        slack_logger.addHandler(journal_handler)

    # Catch and log all exceptions
    from types import TracebackType
    from typing import Type
    def log_excepthook(
            type_: Type[BaseException],
            value: BaseException,
            tb: TracebackType
        ) -> None:
        """override excepthook to log"""
        slack_logger.critical(
            "Critical Exception caught, exiting.",
            exc_info=(type_, value, tb)
        )
        return
    sys.excepthook = log_excepthook

    # Attempt to log to Slack, but don't if there isn't a webhook url
    try:
        webhook_url: str = os.environ["slack_webhook_url"]
        slack_handler: logging.Handler = SlackHandler(webhook_url)
        slack_handler.setLevel(logging.ERROR)
        slack_formatter: logging.Formatter = SlackFormatter(app_name)
        slack_handler.setFormatter(slack_formatter)
        slack_logger.addHandler(slack_handler)
    except KeyError:
        slack_logger.warning("No Slack webhook -- not logging to slack")


    return slack_logger
