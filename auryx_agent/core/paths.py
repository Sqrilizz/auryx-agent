"""Cross-platform path utilities for Auryx Agent."""

import sys
from pathlib import Path


def get_config_dir() -> Path:
    """Get the configuration directory based on the operating system.
    
    Returns:
        Path to configuration directory:
        - Linux/macOS: ~/.config/auryx-agent/
        - Windows: %APPDATA%/auryx-agent/
    """
    if sys.platform == "win32":
        # Windows: use APPDATA
        appdata = Path.home() / "AppData" / "Roaming"
        return appdata / "auryx-agent"
    else:
        # Linux/macOS: use XDG config directory
        return Path.home() / ".config" / "auryx-agent"


def get_config_file() -> Path:
    """Get the path to the configuration file."""
    return get_config_dir() / "config.toml"


def get_history_file() -> Path:
    """Get the path to the history file."""
    return get_config_dir() / "history.json"


def get_reports_dir() -> Path:
    """Get the path to the reports directory."""
    return get_config_dir() / "reports"


def get_logs_dir() -> Path:
    """Get the path to the logs directory."""
    return get_config_dir() / "logs"


def get_plugins_dir() -> Path:
    """Get the path to the plugins directory."""
    return get_config_dir() / "plugins"


def ensure_config_dirs() -> None:
    """Create all necessary configuration directories if they don't exist."""
    get_config_dir().mkdir(parents=True, exist_ok=True)
    get_reports_dir().mkdir(parents=True, exist_ok=True)
    get_logs_dir().mkdir(parents=True, exist_ok=True)
    get_plugins_dir().mkdir(parents=True, exist_ok=True)
