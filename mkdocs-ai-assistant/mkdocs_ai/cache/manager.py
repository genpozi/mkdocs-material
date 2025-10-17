"""Cache manager for AI responses."""

import hashlib
import json
from pathlib import Path
from typing import Optional, Any
from diskcache import Cache


class CacheManager:
    """Manages caching of AI responses to reduce costs and improve performance.
    
    Uses diskcache for persistent, disk-based caching with automatic expiration.
    """

    def __init__(self, cache_dir: str, ttl: int = 86400, max_size: int = 100 * 1024 * 1024):
        """Initialize cache manager.
        
        Args:
            cache_dir: Directory for cache storage
            ttl: Time-to-live in seconds (default: 24 hours)
            max_size: Maximum cache size in bytes (default: 100MB)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl
        
        # Initialize diskcache
        self.cache = Cache(
            str(self.cache_dir),
            size_limit=max_size,
            eviction_policy="least-recently-used",
        )

    def _generate_key(self, prompt: str, **kwargs: Any) -> str:
        """Generate cache key from prompt and parameters.
        
        Args:
            prompt: The prompt text
            **kwargs: Additional parameters that affect the response
            
        Returns:
            Cache key string
        """
        # Create deterministic key from prompt and relevant parameters
        key_data = {
            "prompt": prompt,
            "model": kwargs.get("model"),
            "temperature": kwargs.get("temperature"),
            "max_tokens": kwargs.get("max_tokens"),
            "system_prompt": kwargs.get("system_prompt"),
        }
        
        # Remove None values
        key_data = {k: v for k, v in key_data.items() if v is not None}
        
        # Create hash
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()

    def get(self, prompt: str, **kwargs: Any) -> Optional[str]:
        """Get cached response if available.
        
        Args:
            prompt: The prompt text
            **kwargs: Additional parameters
            
        Returns:
            Cached response or None if not found
        """
        key = self._generate_key(prompt, **kwargs)
        return self.cache.get(key)

    def set(self, prompt: str, response: str, **kwargs: Any) -> None:
        """Cache a response.
        
        Args:
            prompt: The prompt text
            response: The AI response to cache
            **kwargs: Additional parameters
        """
        key = self._generate_key(prompt, **kwargs)
        self.cache.set(key, response, expire=self.ttl)

    def clear(self) -> None:
        """Clear all cached responses."""
        self.cache.clear()

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        return {
            "size": self.cache.volume(),
            "count": len(self.cache),
            "hits": self.cache.stats(enable=True)[0],
            "misses": self.cache.stats(enable=True)[1],
        }

    def close(self) -> None:
        """Close the cache."""
        self.cache.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
