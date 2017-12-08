"""formats data to be pushable"""
import logging
from typing import Dict, Any, Optional

class SlackFormatter(logging.Formatter):
    """generic formatter"""
    def __init__(self, name: str) -> None:
        self.name = name
        super(SlackFormatter, self).__init__()
        return

    def format(self, record: logging.LogRecord) -> str:
        import json

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
                            "title": "Level",
                            "value": record.levelname.title(),
                            "short": True
                        }
                        # {
                        #     "title": "User",
                        #     "value": (
                        #         f"<https://reddit.com/r/{record.user}|{record.user}>"
                        #         if record.user else "Unknown"
                        #     ),
                        #     "short": True
                        # }
                    ],
                    "footer": (
                        "<https://github.com/neoliberal/slackbot_python_logging"
                        "|slackbot_python_logging>"
                    ),
                    "ts": int(record.created)
                }
            ]
        }
        return json.dumps(data)
