"""Google Gemini AI provider implementation."""

import httpx
from typing import Optional, Any
from .base import AIProvider, ProviderError, ProviderResponse


class GeminiProvider(AIProvider):
    """Google Gemini provider for testing and development.
    
    Gemini offers competitive performance and is useful for testing
    before deploying with OpenRouter in production.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.base_url = config.get(
            "base_url",
            "https://generativelanguage.googleapis.com/v1beta",
        )
        if not self.model:
            self.model = "gemini-pro"

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> ProviderResponse:
        """Generate text using Gemini API.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system context
            **kwargs: Additional parameters
            
        Returns:
            ProviderResponse with generated content
        """
        # Combine system prompt and user prompt for Gemini
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": kwargs.get("temperature", self.temperature),
                "maxOutputTokens": kwargs.get("max_tokens", self.max_tokens),
            },
        }
        
        url = f"{self.base_url}/models/{self.model}:generateContent"
        params = {"key": self.api_key}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    url,
                    params=params,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                
                if "error" in data:
                    raise ProviderError(f"Gemini error: {data['error']}")
                
                # Extract content from Gemini response
                candidate = data["candidates"][0]
                content = candidate["content"]["parts"][0]["text"]
                
                return ProviderResponse(
                    content=content,
                    model=self.model,
                    tokens_used=data.get("usageMetadata", {}).get("totalTokenCount"),
                    finish_reason=candidate.get("finishReason"),
                    metadata={
                        "provider": "gemini",
                        "safety_ratings": candidate.get("safetyRatings", []),
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
                    f"Gemini HTTP error {e.response.status_code}: {error_detail}"
                )
            except httpx.RequestError as e:
                raise ProviderError(f"Gemini request error: {str(e)}")
            except (KeyError, IndexError) as e:
                raise ProviderError(f"Invalid Gemini response format: {str(e)}")

    async def embed(self, text: str) -> list[float]:
        """Generate embeddings using Gemini.
        
        Gemini provides embedding models for semantic search.
        """
        embedding_model = "embedding-001"
        url = f"{self.base_url}/models/{embedding_model}:embedContent"
        params = {"key": self.api_key}
        
        payload = {
            "content": {
                "parts": [
                    {"text": text}
                ]
            }
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    url,
                    params=params,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                
                return data["embedding"]["values"]
                
            except httpx.HTTPStatusError as e:
                raise ProviderError(f"Gemini embedding error: {e.response.status_code}")
            except (KeyError, IndexError) as e:
                raise ProviderError(f"Invalid embedding response: {str(e)}")

    def supports_streaming(self) -> bool:
        """Gemini supports streaming."""
        return True

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ):
        """Generate text with streaming (future implementation)."""
        # TODO: Implement Gemini streaming
        raise NotImplementedError("Streaming not yet implemented for Gemini")
