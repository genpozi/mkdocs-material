"""AI provider abstraction layer."""

from .base import AIProvider, ProviderError, ProviderResponse
from .openrouter import OpenRouterProvider
from .gemini import GeminiProvider
from .anthropic import AnthropicProvider
from .ollama import OllamaProvider

__all__ = [
    "AIProvider",
    "ProviderError",
    "ProviderResponse",
    "OpenRouterProvider",
    "GeminiProvider",
    "AnthropicProvider",
    "OllamaProvider",
    "get_provider",
    "create_provider",
]


def get_provider(config: dict) -> AIProvider:
    """Factory function to get the appropriate provider."""
    provider_name = config.get("name", "openrouter")
    
    providers = {
        "openrouter": OpenRouterProvider,
        "gemini": GeminiProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider,
    }
    
    provider_class = providers.get(provider_name)
    if not provider_class:
        raise ValueError(f"Unknown provider: {provider_name}")
    
    return provider_class(config)


def create_provider(
    provider_name: str = "openrouter",
    api_key: str = None,
    model: str = None,
    **kwargs
) -> AIProvider:
    """Create a provider instance with simple parameters.
    
    Args:
        provider_name: Name of provider (openrouter, gemini, anthropic, ollama)
        api_key: Optional API key
        model: Optional model name
        **kwargs: Additional provider-specific parameters
    
    Returns:
        Configured provider instance
    """
    config = {
        "name": provider_name,
        **kwargs
    }
    
    if api_key:
        config["api_key"] = api_key
    if model:
        config["model"] = model
    
    return get_provider(config)
