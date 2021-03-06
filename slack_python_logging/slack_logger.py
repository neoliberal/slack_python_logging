"""main logger"""
import logging
import os
import sys
from typing import Union

from .formatter import SlackFormatter
from .handler import SlackHandler


def getLogger(
        app_name: str,
        stream_loglevel: Union[str, int] = "WARNING",
        slack_loglevel: Union[str, int] = "CRITICAL",
    ) -> logging.Logger:
    """makes new slack logger"""

    # The logger object to which we will add stream/slack handlers
    slack_logger: logging.Logger = logging.getLogger(app_name)
    slack_logger.setLevel("DEBUG") # Log everything that the handlers emit
    formatter: logging.Formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(lineno)-4s %(message)s'
    )

    # Log everything to stdout/stderr
    stream_handler: logging.Handler = logging.StreamHandler()
    stream_handler.setLevel(stream_loglevel)
    stream_handler.setFormatter(formatter)
    slack_logger.addHandler(stream_handler)

    # Attempt to log to Slack, but don't if there isn't a webhook url
    try:
        webhook_url: str = os.environ["slack_webhook_url"]
        slack_handler: logging.Handler = SlackHandler(webhook_url)
        slack_handler.setLevel(slack_loglevel)
        slack_formatter: logging.Formatter = SlackFormatter(app_name)
        slack_handler.setFormatter(slack_formatter)
        slack_logger.addHandler(slack_handler)
    except KeyError:
        slack_logger.warning("No Slack webhook -- not logging to slack")

    return slack_logger
