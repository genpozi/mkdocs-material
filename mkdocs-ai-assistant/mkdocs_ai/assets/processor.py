"""Asset processing orchestrator."""

from pathlib import Path
from typing import Dict, List, Optional
import asyncio

from ..providers import AIProvider, create_provider
from ..cache import CacheManager
from .discovery import AssetDiscovery, Asset
from .compose import ComposeProcessor
from .code import CodeProcessor


class AssetProcessor:
    """Orchestrate asset discovery and documentation generation.
    
    This class coordinates:
    - Asset discovery
    - Processor selection
    - Batch processing
    - Progress reporting
    """
    
    def __init__(
        self,
        project_root: Path,
        provider: AIProvider,
        cache_manager: Optional[CacheManager] = None,
        output_dir: Optional[Path] = None,
    ):
        """Initialize processor.
        
        Args:
            project_root: Root directory of project
            provider: AI provider for generation
            cache_manager: Optional cache manager
            output_dir: Optional output directory for generated docs
        """
        self.project_root = Path(project_root)
        self.provider = provider
        self.cache_manager = cache_manager
        self.output_dir = Path(output_dir) if output_dir else self.project_root / "docs" / "generated"
        
        # Initialize discovery and processors
        self.discovery = AssetDiscovery(project_root)
        self.compose_processor = ComposeProcessor(provider, cache_manager)
        self.code_processor = CodeProcessor(provider, cache_manager)
    
    async def process_all_assets(
        self,
        asset_types: Optional[List[str]] = None,
    ) -> Dict[str, List[Path]]:
        """Discover and process all assets.
        
        Args:
            asset_types: Optional list of asset types to process
                        (docker_compose, python_modules, etc.)
                        If None, processes all types.
        
        Returns:
            Dictionary mapping asset types to generated doc paths
        """
        # Discover assets
        all_assets = self.discovery.discover_all()
        
        # Filter by requested types
        if asset_types:
            all_assets = {
                k: v for k, v in all_assets.items()
                if k in asset_types
            }
        
        # Process each asset type
        results = {}
        
        if "docker_compose" in all_assets:
            results["docker_compose"] = await self._process_compose_files(
                all_assets["docker_compose"]
            )
        
        if "python_modules" in all_assets:
            results["python_modules"] = await self._process_python_modules(
                all_assets["python_modules"]
            )
        
        return results
    
    async def process_docker_compose(
        self,
        compose_path: Optional[Path] = None,
    ) -> Path:
        """Process Docker Compose file(s).
        
        Args:
            compose_path: Optional specific compose file to process
                         If None, discovers and processes all compose files
        
        Returns:
            Path to generated documentation
        """
        if compose_path:
            files = [compose_path]
        else:
            files = self.discovery.discover_docker_compose()
        
        if not files:
            raise ValueError("No Docker Compose files found")
        
        results = await self._process_compose_files(files)
        return results[0] if results else None
    
    async def process_python_code(
        self,
        module_path: Optional[Path] = None,
    ) -> Path:
        """Process Python module(s).
        
        Args:
            module_path: Optional specific module to process
                        If None, discovers and processes all modules
        
        Returns:
            Path to generated documentation
        """
        if module_path:
            files = [module_path]
        else:
            files = self.discovery.discover_python_modules()
        
        if not files:
            raise ValueError("No Python modules found")
        
        results = await self._process_python_modules(files)
        return results[0] if results else None
    
    async def _process_compose_files(
        self,
        files: List[Path],
    ) -> List[Path]:
        """Process multiple Docker Compose files.
        
        Args:
            files: List of compose file paths
        
        Returns:
            List of generated documentation paths
        """
        results = []
        
        for file in files:
            try:
                # Generate documentation
                content = await self.compose_processor.process_compose_file(file)
                
                # Save to output directory
                output_path = self._get_output_path(file, "compose")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(content, encoding="utf-8")
                
                results.append(output_path)
            except Exception as e:
                print(f"Error processing {file}: {e}")
        
        return results
    
    async def _process_python_modules(
        self,
        files: List[Path],
    ) -> List[Path]:
        """Process multiple Python modules.
        
        Args:
            files: List of module file paths
        
        Returns:
            List of generated documentation paths
        """
        results = []
        
        # Filter to only __init__.py files (packages) or main modules
        main_modules = [
            f for f in files
            if f.name == "__init__.py" or not any(
                p.name == "__init__.py" for p in f.parent.glob("__init__.py")
            )
        ]
        
        for file in main_modules:
            try:
                # Generate documentation
                content = await self.code_processor.process_python_module(file)
                
                # Save to output directory
                output_path = self._get_output_path(file, "code")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(content, encoding="utf-8")
                
                results.append(output_path)
            except Exception as e:
                print(f"Error processing {file}: {e}")
        
        return results
    
    def _get_output_path(
        self,
        source_path: Path,
        asset_type: str,
    ) -> Path:
        """Get output path for generated documentation.
        
        Args:
            source_path: Source file path
            asset_type: Type of asset (compose, code, etc.)
        
        Returns:
            Output file path
        """
        # Create relative path from project root
        try:
            rel_path = source_path.relative_to(self.project_root)
        except ValueError:
            # File is outside project root
            rel_path = source_path.name
        
        # Create output path
        output_name = f"{rel_path.stem}-{asset_type}.md"
        return self.output_dir / asset_type / output_name
    
    def get_discovery_summary(self) -> Dict[str, int]:
        """Get summary of discovered assets.
        
        Returns:
            Dictionary mapping asset types to counts
        """
        all_assets = self.discovery.discover_all()
        return {k: len(v) for k, v in all_assets.items()}


async def process_project_assets(
    project_root: Path,
    provider_name: str = "openrouter",
    api_key: Optional[str] = None,
    output_dir: Optional[Path] = None,
    asset_types: Optional[List[str]] = None,
) -> Dict[str, List[Path]]:
    """Convenience function to process project assets.
    
    Args:
        project_root: Root directory of project
        provider_name: AI provider name
        api_key: Optional API key
        output_dir: Optional output directory
        asset_types: Optional list of asset types to process
    
    Returns:
        Dictionary mapping asset types to generated doc paths
    """
    # Create provider
    provider = create_provider(provider_name, api_key=api_key)
    
    # Create cache manager
    cache_dir = project_root / ".ai-cache"
    cache_manager = CacheManager(cache_dir=cache_dir)
    
    # Create processor
    processor = AssetProcessor(
        project_root=project_root,
        provider=provider,
        cache_manager=cache_manager,
        output_dir=output_dir,
    )
    
    # Process assets
    return await processor.process_all_assets(asset_types=asset_types)
