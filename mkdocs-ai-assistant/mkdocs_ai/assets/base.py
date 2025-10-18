"""Base asset processor."""

from abc import ABC, abstractmethod
from typing import Optional

from mkdocs_ai.cache.manager import CacheManager
from mkdocs_ai.providers.base import AIProvider

from .models import Asset, Documentation


class AssetProcessor(ABC):
    """Base class for asset processors."""

    def __init__(
        self, provider: Optional[AIProvider] = None, cache: Optional[CacheManager] = None
    ):
        """Initialize asset processor.

        Args:
            provider: AI provider for content generation
            cache: Cache manager for caching results
        """
        self.provider = provider
        self.cache = cache

    @abstractmethod
    async def process(self, asset: Asset) -> Documentation:
        """Process asset and generate documentation.

        Args:
            asset: Asset to process

        Returns:
            Generated documentation
        """
        pass

    @abstractmethod
    def generate_structure(self, asset: Asset) -> dict:
        """Generate structured documentation data.

        Args:
            asset: Asset to process

        Returns:
            Structured documentation data
        """
        pass

    async def enhance_with_ai(self, structure: dict, prompt_template: str) -> str:
        """Enhance structured docs with AI-generated content.

        Args:
            structure: Structured documentation data
            prompt_template: Template for AI prompt

        Returns:
            AI-enhanced documentation
        """
        if not self.provider:
            # Return basic documentation without AI enhancement
            return self._format_basic_docs(structure)

        # Generate AI prompt
        prompt = prompt_template.format(**structure)

        # Check cache
        cache_key = None
        if self.cache:
            import hashlib

            cache_key = f"asset:{hashlib.sha256(prompt.encode()).hexdigest()[:16]}"
            cached = self.cache.get(cache_key)
            if cached:
                return cached

        # Generate with AI
        response = await self.provider.generate(prompt)
        content = response.content

        # Cache result
        if self.cache and cache_key:
            self.cache.set(cache_key, content)

        return content

    def _format_basic_docs(self, structure: dict) -> str:
        """Format basic documentation without AI.

        Args:
            structure: Structured documentation data

        Returns:
            Basic formatted documentation
        """
        # Override in subclasses for better formatting
        return str(structure)
