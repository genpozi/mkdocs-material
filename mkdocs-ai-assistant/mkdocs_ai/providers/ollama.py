"""Ollama local LLM provider implementation."""

import httpx
from typing import Optional, Any
from .base import AIProvider, ProviderError, ProviderResponse


class OllamaProvider(AIProvider):
    """Ollama provider for local LLM inference.
    
    Ollama allows running models locally for privacy and cost savings.
    This provider is ready for when your local LLM setup is complete.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        if not self.model:
            self.model = "llama3.2"

    def requires_api_key(self) -> bool:
        """Ollama doesn't require an API key for local usage."""
        return False

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Generate text using Ollama API.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system context
            **kwargs: Additional parameters
            
        Returns:
            ProviderResponse with generated content
        """
        payload = {
            "model": kwargs.get("model", self.model),
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.temperature),
                "num_predict": kwargs.get("max_tokens", self.max_tokens),
            },
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                
                if "error" in data:
                    raise ProviderError(f"Ollama error: {data['error']}")
                
                content = data.get("response", "")
                
                return ProviderResponse(
                    content=content,
                    model=data.get("model", self.model),
                    tokens_used=data.get("eval_count"),
                    finish_reason=data.get("done_reason"),
                    metadata={
                        "provider": "ollama",
                        "context": data.get("context"),
                        "total_duration": data.get("total_duration"),
                    },
                )
                
            except httpx.HTTPStatusError as e:
                raise ProviderError(
                    f"Ollama HTTP error {e.response.status_code}: {e.response.text}"
                )
            except httpx.RequestError as e:
                raise ProviderError(
                    f"Ollama request error: {str(e)}. "
                    "Is Ollama running at {self.base_url}?"
                )
            except (KeyError, IndexError) as e:
                raise ProviderError(f"Invalid Ollama response format: {str(e)}")

    async def embed(self, text: str) -> list[float]:
        """Generate embeddings using Ollama.
        
        Ollama supports embedding models like nomic-embed-text.
        """
        payload = {
            "model": "nomic-embed-text",  # Default embedding model
            "prompt": text,
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/embeddings",
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                
                return data["embedding"]
                
            except httpx.HTTPStatusError as e:
                raise ProviderError(f"Ollama embedding error: {e.response.status_code}")
            except (KeyError, IndexError) as e:
                raise ProviderError(f"Invalid embedding response: {str(e)}")

    def supports_streaming(self) -> bool:
        """Ollama supports streaming."""
        return True

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ):
        """Generate text with streaming (future implementation)."""
        # TODO: Implement Ollama streaming
        raise NotImplementedError("Streaming not yet implemented for Ollama")

    async def check_model_available(self) -> bool:
        """Check if the specified model is available locally.
        
        Returns:
            True if model is available
        """
        async with httpx.AsyncClient(timeout=10) as client:
            try:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                data = response.json()
                
                models = [m["name"] for m in data.get("models", [])]
                return self.model in models
                
            except Exception:
                return False
