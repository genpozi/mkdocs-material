"""Configuration schema for MkDocs AI Assistant plugin."""

from mkdocs.config import base, config_options as c
from typing import Literal


class ProviderConfig(base.Config):
    """AI provider configuration."""

    name = c.Choice(
        ["openrouter", "gemini", "anthropic", "ollama"],
        default="openrouter",
    )
    api_key = c.Optional(c.Type(str))
    base_url = c.Optional(c.Type(str))
    model = c.Type(str, default="anthropic/claude-3.5-sonnet")
    fallback = c.Optional(c.Type(str))
    temperature = c.Type(float, default=0.7)
    max_tokens = c.Type(int, default=4000)
    timeout = c.Type(int, default=60)


class CacheConfig(base.Config):
    """Caching configuration."""

    enabled = c.Type(bool, default=True)
    dir = c.Type(str, default=".ai-cache")
    ttl = c.Type(int, default=86400)  # 24 hours
    max_size = c.Type(int, default=1024 * 1024 * 100)  # 100MB


class GenerationTaskConfig(base.Config):
    """Individual generation task configuration."""

    prompt = c.Type(str)
    output = c.Type(str)
    template = c.Optional(c.Type(str))
    context = c.Optional(c.Type(dict))


class GenerationConfig(base.Config):
    """Document generation configuration."""

    enabled = c.Type(bool, default=True)
    output_dir = c.Type(str, default="docs/generated")
    templates_dir = c.Type(str, default=".ai-templates")
    cli_enabled = c.Type(bool, default=True)
    markdown_syntax = c.Type(bool, default=True)
    tasks = c.Optional(c.ListOfItems(c.SubConfig(GenerationTaskConfig)))


class EnhancementConfig(base.Config):
    """Content enhancement configuration."""

    enabled = c.Type(bool, default=True)
    auto_enhance = c.Type(bool, default=False)
    features = c.ListOfItems(
        c.Choice(["grammar", "clarity", "consistency", "seo"]),
        default=["grammar", "clarity"],
    )
    preserve_code = c.Type(bool, default=True)
    preserve_frontmatter = c.Type(bool, default=True)
    exclude_patterns = c.Optional(c.ListOfItems(c.Type(str)))


class SearchConfig(base.Config):
    """Semantic search configuration."""

    enabled = c.Type(bool, default=False)
    embeddings_model = c.Type(str, default="text-embedding-3-small")
    index_file = c.Type(str, default=".ai-cache/embeddings.json")
    chunk_size = c.Type(int, default=1000)
    chunk_overlap = c.Type(int, default=200)


class AssetSourceConfig(base.Config):
    """Asset source configuration."""

    type = c.Choice(["code", "docker-compose", "openapi"])
    path = c.Type(str)
    pattern = c.Optional(c.Type(str))
    languages = c.Optional(c.ListOfItems(c.Type(str)))
    output_dir = c.Type(str)


class AssetsConfig(base.Config):
    """Asset processing configuration."""

    enabled = c.Type(bool, default=False)
    sources = c.Optional(c.ListOfItems(c.SubConfig(AssetSourceConfig)))


class ObeliskConfig(base.Config):
    """Obelisk integration configuration."""

    enabled = c.Type(bool, default=False)
    export_format = c.Type(bool, default=True)
    service_url = c.Type(str, default="http://localhost:8000")
    api_key = c.Optional(c.Type(str))


class AIAssistantConfig(base.Config):
    """Main plugin configuration."""

    enabled = c.Type(bool, default=True)
    provider = c.SubConfig(ProviderConfig)
    cache = c.SubConfig(CacheConfig)
    generation = c.SubConfig(GenerationConfig)
    enhancement = c.SubConfig(EnhancementConfig)
    search = c.SubConfig(SearchConfig)
    assets = c.SubConfig(AssetsConfig)
    obelisk = c.SubConfig(ObeliskConfig)
    debug = c.Type(bool, default=False)
