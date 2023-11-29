"""
This module contains functions providing log operations
"""

import os
import json


def is_valid_json(filename: str) -> bool:
    """
    Checks if file exists and file is non-empty valid JSON file
    :param filename: Name of file
    :return: True if file is valid JSON, otherwise False
    """
    if not os.path.exists(filename):
        return False

    # This checking must be only done when file is small
    if os.path.getsize(filename) < 100:

        with open(filename) as f:
            try:
                content = json.load(f)
                if not content:
                    return False
            except Exception:
                return False
    return True


def log_to_json(filename: str, data: dict) -> None:
    """
    Appends passed data into a JSON file
    :param filename: Name of file
    :param data: A single log record
    :return: None
    """
    if is_valid_json(filename):
        with open(filename, "rb+") as f:
            f.seek(-2, os.SEEK_END)
            record = (",\n" + json.dumps(data, indent=4) + "\n]").encode()
            f.write(record)
    else:
        with open(filename, "w") as f:
            f.write("[\n" + json.dumps(data, indent=4) + "\n]")
