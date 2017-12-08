"""custom handler that pipes messages into neoliberal slack"""
import logging

class SlackHandler(logging.Handler):
    """main class"""

    def __init__(self, url: str) -> None:
        self.url = url
        super(SlackHandler, self).__init__()
        return

    def emit(self, record: logging.LogRecord) -> None:
        """emits message"""
        import requests
        msg: str = self.format(record)
        requests.post(
            self.url,
            data=str.encode(msg),
            headers={"Content-type": "application/json"}
        )
        return
