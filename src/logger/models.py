"""Pydantic models for logger configuration."""
from enum import Enum
from typing import Dict

from pydantic import BaseModel, Field


class AnsiStyle(BaseModel):
    """ANSI color codes for terminal output."""
    model_config = {"frozen": True}

    black: str = Field(default="\033[30m")
    red: str = Field(default="\033[31m")
    green: str = Field(default="\033[32m")
    yellow: str = Field(default="\033[33m")
    blue: str = Field(default="\033[34m")
    magenta: str = Field(default="\033[35m")
    cyan: str = Field(default="\033[36m")
    white: str = Field(default="\033[37m")
    reset: str = Field(default="\033[0m")
    bright: str = Field(default="\033[1m")


class LogLevel(Enum):
    """Log level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogLevelConfig(BaseModel):
    """Configuration for each log level including color, emoji, and color name."""
    model_config = {"frozen": True}

    color: str
    emoji: str
    color_name: str


# Create singleton instance of ANSI styles
ansi_style = AnsiStyle()

# Log level configurations with colors and emojis
LOG_LEVEL_CONFIGS: Dict[LogLevel, LogLevelConfig] = {
    LogLevel.DEBUG: LogLevelConfig(color=ansi_style.cyan, emoji="🔍", color_name="cyan"),
    LogLevel.INFO: LogLevelConfig(color=ansi_style.green, emoji="✨", color_name="green"),
    LogLevel.WARNING: LogLevelConfig(color=ansi_style.yellow, emoji="⚠️", color_name="yellow"),
    LogLevel.ERROR: LogLevelConfig(color=ansi_style.red, emoji="❌", color_name="red"),
    LogLevel.CRITICAL: LogLevelConfig(color=ansi_style.magenta, emoji="🚨", color_name="magenta"),
}

# Default configuration for unknown log levels
DEFAULT_CONFIG = LogLevelConfig(color=ansi_style.white, emoji="📝", color_name="white")

