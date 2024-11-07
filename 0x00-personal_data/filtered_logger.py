#!/usr/bin/env python3
"""
Module contain a function called filter_datum
that returns the log message obfuscated

Args:
    fields(List): a list of strings representing all fields
      to obfuscate
    redaction(str): a string representing by what the field
      will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character
      is separating all fields in the log line (message)
The function should use a regex to replace occurrences
 of certain field values.
filter_datum should be less than 5 lines long and
use re.sub to perform the substitution with a single regex.
"""
from typing import List
import re
import logging
import os
import mysql.connector
from mysql.connector import connection

PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        an initiator class for the
        RedactingFormatter class
        Args:
          fields(List[str]): a list of strings representing all field
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filter values in incoming log records using filter_datum.
        Values for fields in fields should be filtered.
        Args:
            record: logging.LogRecord
        Returns str
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Returns a logger named 'user_data' with a StreamHandler
    and RedactingFormater
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated

      Args:
          fields(List): a list of strings representing all fields
            to obfuscate
          redaction(str): a string representing by what the field
            will be obfuscated
          message: a string representing the log line
          separator: a string representing by which character
            is separating all fields in the log line (message)
      The function should use a regex to replace occurrences
      of certain field values.
      filter_datum should be less than 5 lines long and
      use re.sub to perform the substitution with a single regex.
    """
    pattern = f"({'|'.join(fields)})=([^ {separator}]*)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}",
                  message)

def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to the database
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

