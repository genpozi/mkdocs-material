"""Asset discovery system for automatic documentation generation."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml
import json


class AssetDiscovery:
    """Discover project assets for documentation generation.
    
    Automatically finds:
    - Docker Compose files
    - Python modules
    - OpenAPI specifications
    - Configuration files
    """
    
    def __init__(self, project_root: Path):
        """Initialize discovery system.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root)
        
    def discover_all(self) -> Dict[str, List[Path]]:
        """Discover all supported asset types.
        
        Returns:
            Dictionary mapping asset types to file paths
        """
        return {
            "docker_compose": self.discover_docker_compose(),
            "python_modules": self.discover_python_modules(),
            "openapi_specs": self.discover_openapi_specs(),
            "config_files": self.discover_config_files(),
        }
    
    def discover_docker_compose(self) -> List[Path]:
        """Discover Docker Compose files.
        
        Looks for:
        - docker-compose.yml
        - docker-compose.yaml
        - compose.yml
        - compose.yaml
        - docker-compose.*.yml
        
        Returns:
            List of Docker Compose file paths
        """
        patterns = [
            "docker-compose.yml",
            "docker-compose.yaml",
            "compose.yml",
            "compose.yaml",
            "docker-compose.*.yml",
            "docker-compose.*.yaml",
        ]
        
        files = []
        for pattern in patterns:
            files.extend(self.project_root.rglob(pattern))
        
        # Filter out files in common ignore directories
        return self._filter_ignored(files)
    
    def discover_python_modules(self) -> List[Path]:
        """Discover Python modules.
        
        Looks for:
        - __init__.py files (packages)
        - Standalone .py files in src/lib directories
        
        Returns:
            List of Python module paths
        """
        files = []
        
        # Find all __init__.py files (packages)
        files.extend(self.project_root.rglob("__init__.py"))
        
        # Find Python files in common source directories
        for src_dir in ["src", "lib", "app"]:
            src_path = self.project_root / src_dir
            if src_path.exists():
                files.extend(src_path.rglob("*.py"))
        
        return self._filter_ignored(files)
    
    def discover_openapi_specs(self) -> List[Path]:
        """Discover OpenAPI specification files.
        
        Looks for:
        - openapi.json
        - openapi.yaml
        - swagger.json
        - swagger.yaml
        - Files with 'openapi' or 'swagger' in name
        
        Returns:
            List of OpenAPI spec file paths
        """
        patterns = [
            "openapi.json",
            "openapi.yaml",
            "openapi.yml",
            "swagger.json",
            "swagger.yaml",
            "swagger.yml",
            "*openapi*.json",
            "*openapi*.yaml",
            "*swagger*.json",
            "*swagger*.yaml",
        ]
        
        files = []
        for pattern in patterns:
            files.extend(self.project_root.rglob(pattern))
        
        # Validate that files are actually OpenAPI specs
        validated = []
        for file in files:
            if self._is_openapi_spec(file):
                validated.append(file)
        
        return self._filter_ignored(validated)
    
    def discover_config_files(self) -> List[Path]:
        """Discover configuration files.
        
        Looks for:
        - package.json
        - pyproject.toml
        - Cargo.toml
        - go.mod
        - pom.xml
        
        Returns:
            List of configuration file paths
        """
        patterns = [
            "package.json",
            "pyproject.toml",
            "Cargo.toml",
            "go.mod",
            "pom.xml",
            "build.gradle",
            "CMakeLists.txt",
        ]
        
        files = []
        for pattern in patterns:
            files.extend(self.project_root.rglob(pattern))
        
        return self._filter_ignored(files)
    
    def _filter_ignored(self, files: List[Path]) -> List[Path]:
        """Filter out files in ignored directories.
        
        Args:
            files: List of file paths
            
        Returns:
            Filtered list of file paths
        """
        ignore_dirs = {
            "node_modules",
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "dist",
            "build",
            ".tox",
            "site",
            ".cache",
        }
        
        filtered = []
        for file in files:
            # Check if any parent directory is in ignore list
            if not any(part in ignore_dirs for part in file.parts):
                filtered.append(file)
        
        return filtered
    
    def _is_openapi_spec(self, file: Path) -> bool:
        """Check if file is a valid OpenAPI specification.
        
        Args:
            file: Path to file
            
        Returns:
            True if file is an OpenAPI spec
        """
        try:
            content = file.read_text(encoding="utf-8")
            
            if file.suffix == ".json":
                data = json.loads(content)
            else:
                data = yaml.safe_load(content)
            
            # Check for OpenAPI/Swagger markers
            return (
                "openapi" in data or
                "swagger" in data or
                ("info" in data and "paths" in data)
            )
        except Exception:
            return False


class Asset:
    """Represents a discovered asset."""
    
    def __init__(
        self,
        path: Path,
        asset_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Initialize asset.
        
        Args:
            path: Path to asset file
            asset_type: Type of asset (docker_compose, python_module, etc.)
            metadata: Optional metadata about the asset
        """
        self.path = path
        self.asset_type = asset_type
        self.metadata = metadata or {}
    
    def read_content(self) -> str:
        """Read asset file content.
        
        Returns:
            File content as string
        """
        return self.path.read_text(encoding="utf-8")
    
    def __repr__(self) -> str:
        return f"Asset(path={self.path}, type={self.asset_type})"
