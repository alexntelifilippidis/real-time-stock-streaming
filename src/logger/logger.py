"""Custom colored logger implementation."""
import logging
import os
import sys
from datetime import datetime
from typing import Dict

from src.logger.models import (
    DEFAULT_CONFIG,
    LOG_LEVEL_CONFIGS,
    LogLevel,
    ansi_style,
)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors and emojis using ANSI codes and Pydantic config."""

    def format(self, record: logging.LogRecord) -> str:
        # Try to get config from enum, fallback to default
        try:
            level_enum = LogLevel[record.levelname]
            config = LOG_LEVEL_CONFIGS[level_enum]
        except (KeyError, ValueError):
            config = DEFAULT_CONFIG

        # Format timestamp with white color
        timestamp = f"{ansi_style.white}{datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')}{ansi_style.reset}"
        # Format logger name with blue color and bold
        logger_name = f"{ansi_style.blue}{ansi_style.bright}{record.name}{ansi_style.reset}"
        # Format level with specific color and emoji
        level_text = f"{config.color}{config.emoji} {record.levelname}{ansi_style.reset}"
        # Format message with level-specific color
        message = f"{config.color}{record.getMessage()}{ansi_style.reset}"
        # Combine all parts with dashes
        return f"{timestamp} - {logger_name} - {level_text} - {message}"


class KafkaModelLogger:
    """Custom logger for KafkaModel with colors and emojis.

    This class provides a singleton-like pattern for managing colored loggers
    across the KafkaModel application. It ensures that each named logger
    is created only once and configured with the custom ColoredFormatter.

    :cvar _loggers: Cache of created logger instances
    :vartype _loggers: Dict[str, logging.Logger]
    """

    _loggers: Dict[str, logging.Logger] = {}

    @classmethod
    def get_logger(cls, name: str = "KafkaModel") -> logging.Logger:
        """Get or create a colored logger instance.

        Creates a new logger with ColoredFormatter if it doesn't exist,
        or returns the existing logger for the given name.

        :param name: Name of the logger to create or retrieve
        :type name: str
        :return: Configured logger instance with colored formatting
        :rtype: logging.Logger

        . note::
           The logger is configured with DEBUG level and uses stdout for output.
           Propagation is disabled to prevent duplicate messages.

        . code-block:: python

           logger = SparkModelLogger.get_logger("MyModule")
           logger.info("This is a colored log message")
        """
        loglevel = os.getenv("LOGLEVEL", "INFO")
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(getattr(logging, loglevel.upper(), logging.INFO))

            # Remove existing handlers to avoid duplicates
            logger.handlers.clear()

            # Create console handler
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(ColoredFormatter())

            logger.addHandler(handler)
            logger.propagate = False

            cls._loggers[name] = logger

        return cls._loggers[name]