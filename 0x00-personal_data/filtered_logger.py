#!/usr/bin/python3
""" filter datum module """

from typing import List
import re
import logging


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """filter datum function obfuscate sensitive information
    Args:
        fields (List[str]): fields to obfuscate
        redaction (str): content to obfuscate with
        message (str): the message to obfuscate
        separator (str): line separator

    Returns:
        str: obfuscated str
    """
    for field in fields:
        pattern: str = r'({}=).*?;'.format(field)
        replace: str = r'\1{}{}'.format(redaction, separator)
        message = re.sub(pattern, replace, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format the messages

        Args:
            record (logging.LogRecord): _description_

        Returns:
            str: redacted messages
        """
        # call the parent class format method to format the log record
        message = super().format(record)
        redacted = filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)

        return redacted
