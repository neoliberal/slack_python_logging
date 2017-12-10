"""main logger"""
import logging
import os
import sys

from systemd import journal

from .formatter import SlackFormatter
from .handler import SlackHandler


def initialize(app_name: str, webhook_url=os.environ["slack_webhook_url"]) -> logging.Logger:
    """makes new slack logger"""
    slack_logger: logging.Logger = logging.getLogger(app_name)

    slack_handler: logging.Handler = SlackHandler(webhook_url)
    slack_handler.setLevel(logging.INFO)
    slack_formatter: logging.Formatter = SlackFormatter(app_name)
    slack_handler.setFormatter(slack_formatter)

    journal_handler: logging.Handler = journal.JournalHandler(SYSLOG_IDENTIFIER=app_name)
    journal_handler.setLevel(logging.DEBUG)
    journal_formatter: logging.Formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(lineno)-4d %(message)s'
    )
    journal_handler.setFormatter(journal_formatter)

    slack_logger.addHandler(slack_handler)
    slack_logger.addHandler(journal_handler)

    from types import TracebackType
    from typing import Type
    def log_excepthook(
            type_: Type[BaseException],
            value: BaseException,
            traceback: TracebackType
        ) -> None:
        """override excepthook to log"""
        slack_logger.critical(
            "Critical Exception caught, exiting.",
            exc_info=(type_, value, traceback)
        )
        return


    import atexit
    # shut it, pylint: disable=W0612
    @atexit.register
    def graceful_exit() -> None:
        """outputs if graceful exit"""
        slack_logger.info("Exited gracefully")
        return

    sys.excepthook = log_excepthook

    slack_logger.setLevel(logging.DEBUG)
    return slack_logger
