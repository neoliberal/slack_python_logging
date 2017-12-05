"""main logger"""
import logging
import os
import sys
from typing import List

from .formatter import SlackFormatter
from .handler import SlackHandler

def make_slack_logger(app_name: str) -> logging.Logger:
    """makes new slack logger"""
    slack_logger: logging.Logger = logging.getLogger(app_name)

    slack_handler: logging.Handler = SlackHandler(os.environ["slack_webhook_url"])
    slack_handler.setLevel(logging.INFO)
    slack_formatter: logging.Formatter = SlackFormatter(app_name)
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

    from traceback import format_exception
    from types import TracebackType
    from typing import Type
    def log_excepthook(
            type_: Type[BaseException],
            value: BaseException,
            traceback: TracebackType
        ) -> None:
        """override excepthook to log"""
        fmt_trace: List[str] = format_exception(type_, value, traceback)
        slack_logger.critical("".join(fmt_trace))
        return

    sys.excepthook = log_excepthook

    slack_logger.setLevel(logging.DEBUG)
    return slack_logger
