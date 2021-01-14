# slack\_python\_logging

A Python module that makes logging to Slack easy

The `slack_logger` class implemented here lets you create `logging.Logger` objects containing a stream handler and custom slack handler. The stream handler mimics the behavior and formatting of `logging.BasicConfig`, and the slack handler sends the logged message as well as some useful info (incl. a traceback) to Slack.

## Installation

The version on PyPI is out of date. Instead use pip:

```shell
pip install git+https://github.com/neoliberal/slack_python_logging
```

Or you can clone the repo, in which case I assume you know what you're doing
    
## Usage

You must have the `SLACK_WEBHOOK_URL` environment variable set before initializing

```python
from slack_python_logging import slack_logger
    
logger = slack_logger.initialize(
    app_name = "My App", # Appears in slack messages
    stream_loglevel = "DEBUG" # What gets printed to stdout
    slack_loglevel = "CRITICAL" # What gets sent to Slack
)

logger.debug("foo") # Printed to stderr only 
logger.critical("bar") # Printed to stderr and Slack
```
