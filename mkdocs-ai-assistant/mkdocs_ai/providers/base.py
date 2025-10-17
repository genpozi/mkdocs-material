"""Base AI provider interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Any


class ProviderError(Exception):
    """Base exception for provider errors."""

    pass


@dataclass
class ProviderResponse:
    """Standardized response from AI providers."""

    content: str
    model: str
    tokens_used: Optional[int] = None
    finish_reason: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


class AIProvider(ABC):
    """Abstract base class for all AI providers.
    
    All providers must implement this interface to ensure consistent
    behavior across different AI services.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize provider with configuration.
        
        Args:
            config: Provider configuration dictionary
        """
        self.config = config
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url")
        self.model = config.get("model")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 4000)
        self.timeout = config.get("timeout", 60)

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Generate text from a prompt.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            **kwargs: Additional provider-specific parameters
            
        Returns:
            ProviderResponse with generated content
            
        Raises:
            ProviderError: If generation fails
        """
        pass

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Generate embeddings for text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of embedding values
            
        Raises:
            ProviderError: If embedding generation fails
        """
        pass

    @abstractmethod
    def supports_streaming(self) -> bool:
        """Check if provider supports streaming responses.
        
        Returns:
            True if streaming is supported
        """
        pass

    def validate_config(self) -> None:
        """Validate provider configuration.
        
        Raises:
            ProviderError: If configuration is invalid
        """
        if not self.api_key and self.requires_api_key():
            raise ProviderError(f"API key required for {self.__class__.__name__}")
        
        if not self.model:
            raise ProviderError("Model name is required")

    def requires_api_key(self) -> bool:
        """Check if provider requires an API key.
        
        Returns:
            True if API key is required (default for most providers)
        """
        return True

    async def generate_with_retry(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_retries: int = 3,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Generate with automatic retry on failure.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            max_retries: Maximum number of retry attempts
            **kwargs: Additional parameters
            
        Returns:
            ProviderResponse with generated content
            
        Raises:
            ProviderError: If all retries fail
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                return await self.generate(prompt, system_prompt, **kwargs)
            except ProviderError as e:
                last_error = e
                if attempt < max_retries - 1:
                    # Exponential backoff
                    import asyncio
                    await asyncio.sleep(2 ** attempt)
                continue
        
        raise ProviderError(f"Failed after {max_retries} attempts: {last_error}")
