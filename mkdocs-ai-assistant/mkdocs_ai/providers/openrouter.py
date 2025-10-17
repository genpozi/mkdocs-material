"""OpenRouter AI provider implementation."""

import httpx
from typing import Optional, Any
from .base import AIProvider, ProviderError, ProviderResponse


class OpenRouterProvider(AIProvider):
    """OpenRouter provider for multi-model access.
    
    OpenRouter provides access to multiple AI models through a single API,
    making it ideal as the primary provider for flexibility and cost optimization.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.base_url = config.get("base_url", "https://openrouter.ai/api/v1")
        self.fallback_model = config.get("fallback")
        self.site_url = config.get("site_url", "https://github.com/genpozi/mkdocs-material")
        self.site_name = config.get("site_name", "MkDocs AI Assistant")

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Generate text using OpenRouter API.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system context
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            ProviderResponse with generated content
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name,
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
        }
        
        # Try primary model
        try:
            return await self._make_request(headers, payload)
        except ProviderError as e:
            # Try fallback model if configured
            if self.fallback_model:
                payload["model"] = self.fallback_model
                try:
                    return await self._make_request(headers, payload)
                except ProviderError:
                    pass  # Fall through to raise original error
            raise e

    async def _make_request(
        self,
        headers: dict[str, str],
        payload: dict[str, Any],
    ) -> ProviderResponse:
        """Make HTTP request to OpenRouter API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                
                if "error" in data:
                    raise ProviderError(f"OpenRouter error: {data['error']}")
                
                choice = data["choices"][0]
                content = choice["message"]["content"]
                
                return ProviderResponse(
                    content=content,
                    model=data.get("model", payload["model"]),
                    tokens_used=data.get("usage", {}).get("total_tokens"),
                    finish_reason=choice.get("finish_reason"),
                    metadata={
                        "id": data.get("id"),
                        "provider": "openrouter",
                    },
                )
                
            except httpx.HTTPStatusError as e:
                raise ProviderError(f"HTTP error: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                raise ProviderError(f"Request error: {str(e)}")
            except (KeyError, IndexError) as e:
                raise ProviderError(f"Invalid response format: {str(e)}")

    async def embed(self, text: str) -> list[float]:
        """Generate embeddings using OpenRouter.
        
        Note: OpenRouter supports embeddings through specific models.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": "text-embedding-3-small",  # OpenAI embedding model via OpenRouter
            "input": text,
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/embeddings",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                
                return data["data"][0]["embedding"]
                
            except httpx.HTTPStatusError as e:
                raise ProviderError(f"Embedding error: {e.response.status_code}")
            except (KeyError, IndexError) as e:
                raise ProviderError(f"Invalid embedding response: {str(e)}")

    def supports_streaming(self) -> bool:
        """OpenRouter supports streaming."""
        return True

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ):
        """Generate text with streaming (future implementation).
        
        This is a placeholder for future streaming support.
        """
        # TODO: Implement streaming in future version
        raise NotImplementedError("Streaming not yet implemented")
