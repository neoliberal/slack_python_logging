"""formats data to be pushable"""
import logging
from typing import Dict, Any, Optional, Tuple

class SlackFormatter(logging.Formatter):
    """generic formatter"""
    def __init__(self, name: str) -> None:
        self.name = name
        super(SlackFormatter, self).__init__()
        return

    def format(self, record: logging.LogRecord) -> str:
        import json

        def get_traceback() -> str:
            """returns traceback"""
            from traceback import format_exception
            exc_info: Tuple = record.exc_info
            return "".join(format_exception(*exc_info)) if exc_info else "None"

        def get_color(level: int) -> Optional[str]:
            """returns appropriate color based on logging level"""
            colors: Dict[int, Optional[str]] = {
                0: None,
                10: "#FF00FF",
                20: "good",
                30: "warning",
                40: "danger",
                50:  "#660000"
            }
            return colors[level]

        data: Dict[str, Any] = {
            "attachments": [
                {
                    "color": get_color(record.levelno),
                    "title": self.name,
                    "title_link": f"https://github.com/neoliberal/{self.name}",
                    "text": record.getMessage(),
                    "fields": [
                        {
                            "title": "Module",
                            "value": record.module,
                            "short": True
                        },
                        {
                            "title": "Level",
                            "value": record.levelname.title(),
                            "short": True
                        },
                        {
                            "title": "Function",
                            "value": record.funcName,
                            "short": True
                        },
                        {
                            "title": "Line Number",
                            "value": record.lineno,
                            "short": True
                        },
                        {
                            "title": "Traceback",
                            "value": get_traceback(),
                            "short": False
                        }
                    ],
                    "footer": (
                        "<https://github.com/neoliberal/slack_python_logging"
                        "|slack_python_logging>"
                    ),
                    "ts": int(record.created)
                }
            ]
        }
        return json.dumps(data)
