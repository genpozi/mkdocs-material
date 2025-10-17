"""Anthropic Claude AI provider implementation."""

import httpx
from typing import Optional, Any
from .base import AIProvider, ProviderError, ProviderResponse


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider.
    
    Direct access to Claude models for users who prefer Anthropic's API.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.base_url = config.get("base_url", "https://api.anthropic.com/v1")
        self.api_version = config.get("api_version", "2023-06-01")
        if not self.model:
            self.model = "claude-3-5-sonnet-20241022"

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Generate text using Anthropic API.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system context
            **kwargs: Additional parameters
            
        Returns:
            ProviderResponse with generated content
        """
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.api_version,
            "content-type": "application/json",
        }
        
        payload = {
            "model": kwargs.get("model", self.model),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "messages": [
                {"role": "user", "content": prompt}
            ],
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/messages",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                
                if "error" in data:
                    raise ProviderError(f"Anthropic error: {data['error']}")
                
                content = data["content"][0]["text"]
                
                return ProviderResponse(
                    content=content,
                    model=data.get("model", self.model),
                    tokens_used=data.get("usage", {}).get("input_tokens", 0)
                    + data.get("usage", {}).get("output_tokens", 0),
                    finish_reason=data.get("stop_reason"),
                    metadata={
                        "id": data.get("id"),
                        "provider": "anthropic",
                        "usage": data.get("usage", {}),
                    },
                )
                
            except httpx.HTTPStatusError as e:
                error_detail = ""
                try:
                    error_data = e.response.json()
                    error_detail = error_data.get("error", {}).get("message", "")
                except Exception:
                    error_detail = e.response.text
                raise ProviderError(
                    f"Anthropic HTTP error {e.response.status_code}: {error_detail}"
                )
            except httpx.RequestError as e:
                raise ProviderError(f"Anthropic request error: {str(e)}")
            except (KeyError, IndexError) as e:
                raise ProviderError(f"Invalid Anthropic response format: {str(e)}")

    async def embed(self, text: str) -> list[float]:
        """Generate embeddings.
        
        Note: Anthropic doesn't provide embedding models directly.
        This would need to use a different service or be disabled.
        """
        raise ProviderError(
            "Anthropic does not provide embedding models. "
            "Use OpenRouter or Gemini for embeddings."
        )

    def supports_streaming(self) -> bool:
        """Anthropic supports streaming."""
        return True

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ):
        """Generate text with streaming (future implementation)."""
        # TODO: Implement Anthropic streaming
        raise NotImplementedError("Streaming not yet implemented for Anthropic")
