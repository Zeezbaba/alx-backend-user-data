#!/usr/bin/env python3
"""function called filter_datum that
returns the log message obfuscated
"""

import re
from typing import List
import logging
import os
import mysql.connector
# from mysql.connector import connection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")

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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connection.MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=db_name)


def main() -> None:
    """Retrieves and logs user data"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        log_record = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(log_record.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
