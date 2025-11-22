"""Factory for creating AI client from configuration."""

from auryx_agent.core.config import Config
from auryx_agent.core.providers.base import BaseProvider
from auryx_agent.core.providers.factory import ProviderFactory


def create_client_from_config(config: Config) -> BaseProvider:
    """Create AI client from configuration.
    
    Args:
        config: Configuration object
        
    Returns:
        Provider instance
        
    Raises:
        ValueError: If provider is not configured or API key is missing
    """
    provider_name = config.provider.lower()
    
    # Map provider names to config API key attributes
    api_key_map = {
        "yellowfire": config.yellowfire_api_key,
        "openai": config.openai_api_key,
        "anthropic": config.anthropic_api_key,
        "google": config.google_api_key,
        "groq": config.groq_api_key,
        "vercel": config.vercel_api_key,
    }
    
    api_key = api_key_map.get(provider_name)
    
    if not api_key:
        raise ValueError(
            f"API key for provider '{provider_name}' is not configured. "
            f"Please add it to your config file at ~/.config/auryx-agent/config.toml"
        )
    
    return ProviderFactory.create(
        provider_name=provider_name,
        api_key=api_key,
        model=config.default_model
    )


def get_available_providers(config: Config) -> list[str]:
    """Get list of providers that have API keys configured.
    
    Args:
        config: Configuration object
        
    Returns:
        List of provider names with configured API keys
    """
    available = []
    
    if config.yellowfire_api_key:
        available.append("yellowfire")
    if config.openai_api_key:
        available.append("openai")
    if config.anthropic_api_key:
        available.append("anthropic")
    if config.google_api_key:
        available.append("google")
    if config.groq_api_key:
        available.append("groq")
    if config.vercel_api_key:
        available.append("vercel")
    
    return available
