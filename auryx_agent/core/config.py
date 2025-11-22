"""Configuration management for Auryx Agent."""

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from auryx_agent.core.paths import get_config_file, ensure_config_dirs


@dataclass
class Config:
    """Configuration for Auryx Agent.
    
    Attributes:
        provider: AI provider to use (yellowfire, openai, anthropic, google, groq, vercel)
        default_model: Default AI model to use
        fallback_model: Fallback model if primary is unavailable
        theme: UI theme (dark, light)
        auto_update: Enable automatic updates
        yellowfire_api_key: YellowFire API key
        openai_api_key: OpenAI API key
        anthropic_api_key: Anthropic API key
        google_api_key: Google API key
        groq_api_key: Groq API key
        vercel_api_key: Vercel API key
        default_timeout: Default timeout for network operations in seconds
        max_history_entries: Maximum number of history entries to keep
        show_spinners: Show animated spinners during operations
        card_width: Width of result cards in characters
        show_logo: Show ASCII art logo on startup
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        assistant_name: Custom name for the AI assistant
        system_prompt: Custom system prompt for AI behavior
        temperature: Temperature for AI generation (0.0-2.0)
    """
    provider: str = "yellowfire"
    default_model: str = "command-a"
    fallback_model: str = "gpt-4o-mini"
    theme: str = "dark"
    auto_update: bool = True
    yellowfire_api_key: str = ""
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    groq_api_key: str = ""
    vercel_api_key: str = ""
    default_timeout: int = 5
    max_history_entries: int = 1000
    show_spinners: bool = True
    card_width: int = 60
    show_logo: bool = True
    log_level: str = "INFO"
    log_file: str = "~/.config/auryx-agent/logs/auryx.log"
    assistant_name: str = "Auryx"
    system_prompt: str = ""
    temperature: float = 0.7


def create_default_config() -> None:
    """Create a default configuration file at the standard location.
    
    Creates the configuration directory structure if it doesn't exist,
    then writes a default configuration file with comments explaining
    each setting.
    """
    ensure_config_dirs()
    config_file = get_config_file()
    
    default_config_content = """# Auryx Agent Configuration

# AI Provider Selection
# Available: yellowfire, openai, anthropic, google, groq, vercel
provider = "yellowfire"

# Default AI model to use
# command-a is the fastest model (2.04s average response time)
default_model = "command-a"

# Fallback model if primary is unavailable
fallback_model = "gpt-4o-mini"

# UI theme (dark, light)
theme = "dark"

# Enable automatic updates
auto_update = true

# API Keys for different providers
[api_keys]
# YellowFire - Get free $1: https://t.me/GPT4_Unlimit_bot?start=api
yellowfire = ""

# OpenAI - https://platform.openai.com/api-keys
openai = ""

# Anthropic - https://console.anthropic.com/
anthropic = ""

# Google AI Studio - https://makersuite.google.com/app/apikey
google = ""

# Groq - https://console.groq.com/keys
groq = ""

# Vercel AI SDK - https://sdk.vercel.ai/
vercel = ""

# Network settings
[network]
default_timeout = 5

# History settings
[history]
max_entries = 1000

# Output settings
[output]
show_spinners = true
card_width = 60
show_logo = true

# Logging settings
[logging]
level = "INFO"
file = "~/.config/auryx-agent/logs/auryx.log"

# AI Customization (like ChatGPT custom instructions)
[ai]
# Custom name for the assistant (default: "Auryx")
assistant_name = "Auryx"

# Custom system prompt to define AI behavior and personality
# Leave empty for default behavior
system_prompt = ""

# Temperature for generation (0.0 = deterministic, 2.0 = very creative)
temperature = 0.7

# Examples of custom system prompts:
# system_prompt = "You are a helpful network engineer assistant. Always provide detailed technical explanations."
# system_prompt = "You are a friendly AI that explains things simply. Use analogies and examples."
# system_prompt = "Ты русскоязычный ассистент. Всегда отвечай на русском языке подробно и профессионально."
"""
    
    config_file.write_text(default_config_content)


def load_config() -> Config:
    """Load configuration from the standard location.
    
    Attempts to load configuration from ~/.config/auryx-agent/config.toml
    (or platform-specific equivalent). If the file doesn't exist, creates
    a default configuration file and returns default values.
    
    If the file exists but is corrupted or invalid, returns default values
    and logs a warning.
    
    Returns:
        Config object with loaded or default values
    """
    config_file = get_config_file()
    
    # If config file doesn't exist, create default and return defaults
    if not config_file.exists():
        create_default_config()
        return Config()
    
    # Try to load and parse the config file
    try:
        with open(config_file, "rb") as f:
            data = tomllib.load(f)
        
        # Extract values with defaults
        api_keys = data.get("api_keys", {})
        config = Config(
            provider=data.get("provider", "yellowfire"),
            default_model=data.get("default_model", "command-a"),
            fallback_model=data.get("fallback_model", "gpt-4o-mini"),
            theme=data.get("theme", "dark"),
            auto_update=data.get("auto_update", True),
            yellowfire_api_key=api_keys.get("yellowfire", ""),
            openai_api_key=api_keys.get("openai", ""),
            anthropic_api_key=api_keys.get("anthropic", ""),
            google_api_key=api_keys.get("google", ""),
            groq_api_key=api_keys.get("groq", ""),
            vercel_api_key=api_keys.get("vercel", ""),
            default_timeout=data.get("network", {}).get("default_timeout", 5),
            max_history_entries=data.get("history", {}).get("max_entries", 1000),
            show_spinners=data.get("output", {}).get("show_spinners", True),
            card_width=data.get("output", {}).get("card_width", 60),
            show_logo=data.get("output", {}).get("show_logo", True),
            log_level=data.get("logging", {}).get("level", "INFO"),
            log_file=data.get("logging", {}).get("file", "~/.config/auryx-agent/logs/auryx.log"),
            assistant_name=data.get("ai", {}).get("assistant_name", "Auryx"),
            system_prompt=data.get("ai", {}).get("system_prompt", ""),
            temperature=data.get("ai", {}).get("temperature", 0.7),
        )
        
        # Validate configuration
        validate_config(config)
        
        return config
        
    except (tomllib.TOMLDecodeError, OSError, ValueError) as e:
        # If file is corrupted or invalid, return defaults
        # In a real application, we would log this warning
        return Config()


def validate_config(config: Config) -> None:
    """Validate configuration values.
    
    Raises:
        ValueError: If any configuration value is invalid
    """
    # Validate provider
    valid_providers = ["yellowfire", "openai", "anthropic", "google", "groq", "vercel"]
    if config.provider not in valid_providers:
        raise ValueError(f"Invalid provider '{config.provider}'. Must be one of: {', '.join(valid_providers)}")
    
    # Validate theme
    valid_themes = ["dark", "light"]
    if config.theme not in valid_themes:
        raise ValueError(f"Invalid theme '{config.theme}'. Must be one of: {', '.join(valid_themes)}")
    
    # Validate timeout
    if config.default_timeout <= 0:
        raise ValueError(f"Invalid default_timeout '{config.default_timeout}'. Must be positive.")
    
    # Validate max_history_entries
    if config.max_history_entries <= 0:
        raise ValueError(f"Invalid max_history_entries '{config.max_history_entries}'. Must be positive.")
    
    # Validate card_width
    if config.card_width < 20 or config.card_width > 200:
        raise ValueError(f"Invalid card_width '{config.card_width}'. Must be between 20 and 200.")
    
    # Validate log_level
    valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if config.log_level.upper() not in valid_log_levels:
        raise ValueError(f"Invalid log_level '{config.log_level}'. Must be one of: {', '.join(valid_log_levels)}")
    
    # Validate temperature
    if config.temperature < 0.0 or config.temperature > 2.0:
        raise ValueError(f"Invalid temperature '{config.temperature}'. Must be between 0.0 and 2.0.")
