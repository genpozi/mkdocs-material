"""Asset processing module for automatic documentation generation."""

from .discovery import AssetDiscovery, Asset
from .compose import ComposeProcessor
from .code import CodeProcessor
from .processor import AssetProcessor, process_project_assets

__all__ = [
    "AssetDiscovery",
    "Asset",
    "ComposeProcessor",
    "CodeProcessor",
    "AssetProcessor",
    "process_project_assets",
]
