"""CCAPI - Cloud Commerce Pro API integraion."""

import logging.config
from copy import copy
dictLogConfig = {
    "version": 1,
    "handlers": {
        "default_file_handler": {
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "filename": "ccapi.log"
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "error.log",
            "maxBytes": 102400,
            "formatter": "default_formatter",
        }
    },
    "loggers": {
        "ccapi.requests.ccapisession": {
            "handlers": [],
            "level": "DEBUG",
        },
        "errors": {
            "handlers": ["error_file_handler"],
            "level": "ERROR",
        }
    },
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    }
}

logging.config.dictConfig(dictLogConfig)


class RequestFormatter(logging.Formatter):
    """Format log with escaped newlines."""

    def format(self, record):
        """Format log with escaped newlines."""
        record = copy(record)
        record.msg = record.msg.strip().replace('\n', '\\n')
        return super().format(record)


logger = logging.getLogger('ccapi.requests.ccapisession')
handler = logging.handlers.RotatingFileHandler(
    filename='ccapi_requests.log', maxBytes=102400)
handler.setFormatter(
    RequestFormatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

from .ccapi import CCAPI  # NOQA
from .inventoryitems import ProductOptions, Warehouses, VatRates  # NOQA
from .urls import URLs  # NOQA
from .requests.createorder import NewOrderItem  # NOQA
