#!/usr/bin/env python3
"""function called filter_datum that
returns the log message obfuscated
"""

import re


def filter_datum(fields, redaction, message, separator):
    """Returns the log message obfuscated"""
    pattern = f"({'|'.join(fields)})=[^;{separator}]*"
    return re.sub(pattern, lambda m: m.group().split('=')
                  [0] + '=' + redaction, message)
