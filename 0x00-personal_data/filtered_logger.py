#!/usr/bin/env python3
"""function called filter_datum that
returns the log message obfuscated
"""

import re
from typing import List
import logging

PII_FIELDS = ["name", "email", "phone", "ssn", "password"]

# def filter_datum(fields, redaction, message, separator):
#     """Returns the log message obfuscated"""
#     pattern = f"({'|'.join(fields)})=[^;{separator}]*"
#     return re.sub(pattern, lambda m: m.group().split('=')
#                   [0] + '=' + redaction, message)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialization"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Uses the superclass (logging.Formatter) format
        method to get the original log message
        """
        messages = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            messages, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Creates and configures a logger name"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
