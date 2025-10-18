"""Data models for asset processing."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Asset:
    """Represents a project asset to be documented."""

    type: str  # python, docker-compose, openapi, etc.
    path: Path
    name: str
    metadata: dict = field(default_factory=dict)


@dataclass
class Documentation:
    """Generated documentation from an asset."""

    content: str
    diagrams: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    examples: list[str] = field(default_factory=list)
    file_path: Optional[str] = None


@dataclass
class AssetSource:
    """Configuration for an asset source."""

    type: str
    path: str
    pattern: Optional[str] = None
    output_dir: str = "docs/generated"
    use_mkdocstrings: bool = False
    ai_summaries: bool = True
    ai_examples: bool = True
    generate_diagrams: bool = True


@dataclass
class AssetConfig:
    """Configuration for asset processing."""

    enabled: bool = False
    sources: list[AssetSource] = field(default_factory=list)
