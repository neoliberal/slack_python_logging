"""main logger"""
import logging
from typing import Optional

from formatter import SlackFormatter
from handler import SlackHandler

def make_slack_logger(
        url: str, app_name: str,
        formatter: Optional[logging.Formatter] = None
    ) -> logging.Logger:
    """makes new slack logger"""
    slack_logger: logging.Logger = logging.getLogger(__name__)
    slack_logger.setLevel(logging.INFO)

    slack_handler: logging.Handler = SlackHandler(url)
    slack_handler.setLevel(logging.INFO)

    slack_formatter: logging.Formatter = SlackFormatter(app_name) if (
        formatter is None
    ) else formatter

    slack_handler.setFormatter(slack_formatter)

    slack_logger.addHandler(slack_handler)
    return slack_logger
