"""Asset processing module for automatic documentation generation."""

from .discovery import AssetDiscovery
from .base import AssetProcessor
from .models import Asset, AssetConfig, AssetSource, Documentation
from .docker_compose import DockerComposeProcessor
from .python_code import PythonCodeProcessor
from .mermaid import MermaidGenerator
from .processor import AssetProcessorOrchestrator

# Legacy imports for backward compatibility
from .compose import ComposeProcessor
from .code import CodeProcessor

__all__ = [
    "AssetDiscovery",
    "Asset",
    "AssetConfig",
    "AssetSource",
    "Documentation",
    "AssetProcessor",
    "DockerComposeProcessor",
    "PythonCodeProcessor",
    "MermaidGenerator",
    "AssetProcessorOrchestrator",
    # Legacy
    "ComposeProcessor",
    "CodeProcessor",
]
