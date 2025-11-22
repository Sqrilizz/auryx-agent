"""Parser for model specifications with provider support.

YellowFire is the default provider with all models already defined in code.
Parser is only needed for other providers with explicit provider:model format.

Supported formats:
- model_name → YellowFire (default, models defined in YellowFireClient.AVAILABLE_MODELS)
- google:model_name → Google AI API directly
- groq:model_name → Groq API directly

Examples:
- gpt-4o-mini → YellowFire (no parsing, direct lookup)
- claude-3-5-sonnet → YellowFire (no parsing, direct lookup)
- google:gemini-1.5-pro → Google AI API (parsed, uses Google SDK)
- groq:llama-3.3-70b-versatile → Groq API (parsed, uses Groq SDK)
"""

from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class ModelSpec:
    """Specification for a model with optional provider."""
    model: str
    provider: Optional[str] = None
    
    def __str__(self) -> str:
        if self.provider:
            return f"{self.provider}:{self.model}"
        return self.model


def parse_model_spec(spec: str) -> ModelSpec:
    """Parse model specification string.
    
    Without provider prefix, uses YellowFire (default, access to all models).
    With provider prefix, uses that provider's API directly.
    
    Args:
        spec: Model specification (e.g., "gpt-4o-mini" or "openai:gpt-4o")
        
    Returns:
        ModelSpec with parsed provider and model
        
    Examples:
        >>> parse_model_spec("gpt-4o-mini")
        ModelSpec(model='gpt-4o-mini', provider=None)  # Uses YellowFire
        
        >>> parse_model_spec("openai:gpt-4o")
        ModelSpec(model='gpt-4o', provider='openai')  # Uses OpenAI directly
        
        >>> parse_model_spec("anthropic:claude-3-5-sonnet")
        ModelSpec(model='claude-3-5-sonnet', provider='anthropic')  # Uses Anthropic directly
    """
    if ":" in spec:
        provider, model = spec.split(":", 1)
        provider = provider.strip().lower()
        model = model.strip()
        
        # Validate provider
        if not validate_provider(provider):
            raise ValueError(
                f"Unknown provider '{provider}'. "
                f"Valid providers: yellowfire, google, groq"
            )
        
        return ModelSpec(model=model, provider=provider)
    
    # No provider specified = use YellowFire (default, no parsing needed)
    return ModelSpec(model=spec.strip(), provider=None)


def validate_provider(provider: str) -> bool:
    """Check if provider name is valid.
    
    Args:
        provider: Provider name to validate
        
    Returns:
        True if provider is valid
    """
    valid_providers = [
        "yellowfire",
        "google",
        "groq"
    ]
    return provider.lower() in valid_providers


def get_provider_models(provider: str) -> list[str]:
    """Get list of models available for a specific provider.
    
    Args:
        provider: Provider name
        
    Returns:
        List of model names available for this provider
    """
    # Import here to avoid circular dependency
    from auryx_agent.core.yellowfire_client import YellowFireClient
    
    provider = provider.lower()
    
    if provider == "yellowfire":
        # YellowFire has access to ALL models (это база)
        return YellowFireClient.AVAILABLE_MODELS
    
    # For other providers, return their native models
    # These are models you can use with provider:model format
    
    elif provider == "google":
        # Google AI native models (актуальные названия из API)
        return [
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro-latest", "gemini-1.5-pro",
            "gemini-1.5-flash-latest", "gemini-1.5-flash",
            "gemini-1.0-pro-latest", "gemini-1.0-pro"
        ]
    
    elif provider == "groq":
        # Groq text-to-text models (все доступные из API)
        return [
            # Llama models
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            # OpenAI OSS models
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            # Other models
            "qwen/qwen3-32b",
            "moonshotai/kimi-k2-instruct",
            "groq/compound",
            "groq/compound-mini",
            "allam-2-7b"
        ]
    
    return []


def suggest_models(query: str, provider: Optional[str] = None, limit: int = 10) -> list[str]:
    """Suggest models based on query and optional provider.
    
    Args:
        query: Search query (partial model name)
        provider: Optional provider to filter by
        limit: Maximum number of suggestions
        
    Returns:
        List of matching model names
    """
    if provider:
        available_models = get_provider_models(provider)
    else:
        from auryx_agent.core.yellowfire_client import YellowFireClient
        available_models = YellowFireClient.AVAILABLE_MODELS
    
    query_lower = query.lower()
    
    # Exact matches first
    exact = [m for m in available_models if m.lower() == query_lower]
    
    # Starts with
    starts = [m for m in available_models 
              if m.lower().startswith(query_lower) and m not in exact]
    
    # Contains
    contains = [m for m in available_models 
                if query_lower in m.lower() and m not in exact and m not in starts]
    
    results = exact + starts + contains
    return results[:limit]


def format_model_with_provider(model: str, provider: Optional[str] = None) -> str:
    """Format model name with provider prefix if specified.
    
    Args:
        model: Model name
        provider: Optional provider name
        
    Returns:
        Formatted string (e.g., "openai:gpt-4o" or "gpt-4o-mini")
    """
    if provider:
        return f"{provider}:{model}"
    return model
