import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union

from ..config.settings import settings


class ColoredFormatter(logging.Formatter):
    """Formatter that adds colors to log messages based on level

    The colors are:
    - DEBUG: Grey (less important information)
    - INFO: Cyan (normal operations)
    - WARNING: Yellow (potential issues)
    - ERROR: Red (errors that need attention)
    - CRITICAL: Red background (severe errors)
    """

    COLORS = {
        logging.DEBUG: "\033[37m",  # Grey
        logging.INFO: "\033[36m",  # Cyan
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",  # Red
        logging.CRITICAL: "\033[41m",  # Red background
    }
    RESET = "\033[0m"  # Reset to default terminal color

    def format(self, record):
        """Format the log record with appropriate color based on level

        Args:
            record (LogRecord): The log record to format

        Returns:
            str: The formatted log message
        """
        color = self.COLORS.get(record.levelno)
        return f"{color}{super().format(record)}{self.RESET}"