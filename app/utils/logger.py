import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union

from app.config.settings import settings


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


def setup_logger(
    name: str = settings.APP_NAME,
    log_file: Optional[Union[str, Path]] = None,
    console_level: Optional[int] = None,
    file_level: int = logging.DEBUG,
    log_format: str = settings.LOG_FORMAT,
    max_file_size: int = 5 * 1024 * 1024,  # 5 MB
    backup_count: int = 5,
) -> logging.Logger:
    """Set up a logger with the given settings

    Args:
        name: Logger name (default is APP_NAME from settings)
        log_file: Optional path to log file (if None, no file logging)
        console_level: Level for console output (default from settings)
        file_level: Level for file output (default DEBUG)
        log_format: Format string for log messages
        max_file_size: Maximum log file size before rotation (bytes)
        backup_count: Number of backup log files to keep

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logger("mylogger", log_file="app.log")
        >>> logger.info("Application started")
    """

    if console_level is None:
        console_level = getattr(logging, settings.LOG_LEVEL)

    logger = logging.getLogger(name)
    logger.setLevel(min(console_level, file_level))

    logger.propagate = False  # Prevent log messages from propagating to root logger

    if logger.hasHandlers():
        logger.handlers.clear()

    console_formatter = ColoredFormatter(log_format)
    file_formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(console_level)
    logger.addHandler(console_handler)

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_path, maxBytes=max_file_size, backupCount=backup_count
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(file_level)
        logger.addHandler(file_handler)

    return logger


def get_repository_logger(repo_path: Union[str, Path]) -> logging.Logger:
    """
    Get logger configured for a specific repository.

    Args:
        repo_path: Path to the repository

    Returns:
        Configured logger for the repository

    Example:
        >>> repo_logger = get_repository_logger("/path/to/repo")
        >>> repo_logger.info("Repository operation completed")
    """
    repo_path = Path(repo_path)
    repo_name = repo_path.name  # Use repository folder name in logger name

    # Store logs in .gvcs/logs inside the repository
    log_file = settings.get_repo_path(repo_path) / "logs" / f"{settings.APP_NAME}.log"

    # Create a logger with the repository name as part of the logger name
    # This creates a hierarchy of loggers (app.repo_name)
    return setup_logger(
        name=f"{settings.APP_NAME}.{repo_name}",
        log_file=log_file,
    )


logger = setup_logger()

root_logger = logging.getLogger()
if not root_logger.handlers:
    root_handler = logging.StreamHandler()
    root_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    root_logger.addHandler(root_handler)
    root_logger.setLevel(logging.WARNING)


"""if __name__ == "__main__":
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
"""