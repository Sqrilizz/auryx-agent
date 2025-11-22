"""Provider factory for creating AI provider instances."""

from typing import Dict, Type, Optional
from auryx_agent.core.providers.base import BaseProvider
from auryx_agent.core.providers.yellowfire import YellowFireProvider
from auryx_agent.core.providers.google import GoogleProvider
from auryx_agent.core.providers.groq import GroqProvider


class ProviderFactory:
    """Factory for creating AI provider instances."""
    
    # Map provider names to their classes
    PROVIDERS: Dict[str, Type[BaseProvider]] = {
        "yellowfire": YellowFireProvider,
        "google": GoogleProvider,
        "groq": GroqProvider,
    }
    
    # Default models for each provider
    DEFAULT_MODELS = {
        "yellowfire": "command-a",
        "google": "gemini-2.5-flash",
        "groq": "llama-3.3-70b-versatile",
    }
    
    @classmethod
    def create(cls, provider_name: str, api_key: str, model: Optional[str] = None) -> BaseProvider:
        """Create a provider instance.
        
        Args:
            provider_name: Name of the provider (yellowfire, google, groq)
            api_key: API key for the provider
            model: Model to use (optional, uses default if not specified)
            
        Returns:
            Provider instance
            
        Raises:
            ValueError: If provider name is unknown
        """
        provider_name = provider_name.lower()
        
        if provider_name not in cls.PROVIDERS:
            available = ", ".join(cls.PROVIDERS.keys())
            raise ValueError(f"Unknown provider '{provider_name}'. Available: {available}")
        
        provider_class = cls.PROVIDERS[provider_name]
        default_model = model or cls.DEFAULT_MODELS[provider_name]
        
        try:
            return provider_class(api_key=api_key, default_model=default_model)
        except ImportError as e:
            raise ImportError(f"Failed to initialize {provider_name} provider: {str(e)}")
    
    @classmethod
    def list_providers(cls) -> list[str]:
        """List all available provider names."""
        return list(cls.PROVIDERS.keys())
    
    @classmethod
    def get_default_model(cls, provider_name: str) -> str:
        """Get default model for a provider.
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            Default model name
        """
        return cls.DEFAULT_MODELS.get(provider_name.lower(), "")
