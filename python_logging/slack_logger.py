"""main logger"""
import logging
import os
from typing import Optional
import sys

from .formatter import SlackFormatter
from .handler import SlackHandler

def make_slack_logger(
        app_name: str,
        formatter: Optional[logging.Formatter] = None
    ) -> logging.Logger:
    """makes new slack logger"""
    slack_logger: logging.Logger = logging.getLogger(app_name)

    slack_handler: logging.Handler = SlackHandler(os.environ["slack_webhook_url"])
    slack_handler.setLevel(logging.INFO)
    slack_formatter: logging.Formatter = SlackFormatter(app_name) if (
        formatter is None
    ) else formatter
    slack_handler.setFormatter(slack_formatter)

    file_handler: logging.Handler = logging.FileHandler(
        os.path.join(os.sep, "var", "log", app_name + ".log")
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter: logging.Formatter = logging.Formatter(
        fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    slack_logger.addHandler(slack_handler)
    slack_logger.addHandler(file_handler)

    def log_excepthook(exctype, value, traceback):
        """override excepthook to log"""
        import traceback
        traceback: str = traceback.print_exception(exctype, value, traceback)
        slack_logger.critical(traceback)

    sys.excepthook = log_excepthook

    return slack_logger
