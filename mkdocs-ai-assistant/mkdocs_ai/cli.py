"""CLI commands for MkDocs AI Assistant."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.markdown import Markdown

from .generation.prompt import PromptGenerator
from .providers import get_provider, ProviderError
from .cache import CacheManager

console = Console()


@click.group()
@click.version_option(package_name="mkdocs-ai-assistant")
def main():
    """MkDocs AI Assistant - AI-powered documentation generation."""
    pass


@main.command()
@click.argument("prompt")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path (default: auto-generated in docs/generated/)",
)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["openrouter", "gemini", "anthropic", "ollama"]),
    default="openrouter",
    help="AI provider to use",
)
@click.option(
    "--model",
    "-m",
    help="Model to use (provider-specific)",
)
@click.option(
    "--api-key",
    envvar="OPENROUTER_API_KEY",
    help="API key (or set via environment variable)",
)
@click.option(
    "--no-cache",
    is_flag=True,
    help="Disable caching for this generation",
)
@click.option(
    "--template",
    "-t",
    type=click.Path(exists=True),
    help="Use a Jinja2 template file",
)
@click.option(
    "--context",
    "-c",
    multiple=True,
    help="Template context variables (key=value)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def generate(
    prompt: str,
    output: Optional[str],
    provider: str,
    model: Optional[str],
    api_key: Optional[str],
    no_cache: bool,
    template: Optional[str],
    context: tuple[str, ...],
    verbose: bool,
):
    """Generate documentation from a prompt.
    
    Examples:
    
        # Basic generation
        mkdocs ai generate "Create a guide to Docker Compose"
        
        # Specify output file
        mkdocs ai generate "Kubernetes basics" -o docs/k8s.md
        
        # Use specific model
        mkdocs ai generate "API docs" -m anthropic/claude-3-opus
        
        # Use template
        mkdocs ai generate "API reference" -t templates/api.md.j2
        
        # With context variables
        mkdocs ai generate "Service docs" -t templates/service.md.j2 -c name=auth -c version=2.0
    """
    asyncio.run(_generate_async(
        prompt=prompt,
        output=output,
        provider=provider,
        model=model,
        api_key=api_key,
        no_cache=no_cache,
        template=template,
        context=context,
        verbose=verbose,
    ))


async def _generate_async(
    prompt: str,
    output: Optional[str],
    provider: str,
    model: Optional[str],
    api_key: Optional[str],
    no_cache: bool,
    template: Optional[str],
    context: tuple[str, ...],
    verbose: bool,
):
    """Async implementation of generate command."""
    
    # Show header
    console.print(Panel.fit(
        "[bold cyan]MkDocs AI Assistant[/bold cyan]\n"
        "[dim]Document Generation[/dim]",
        border_style="cyan",
    ))
    
    # Parse context variables
    context_dict = {}
    for ctx in context:
        if "=" not in ctx:
            console.print(f"[red]Error:[/red] Invalid context format: {ctx}")
            console.print("Use: -c key=value")
            sys.exit(1)
        key, value = ctx.split("=", 1)
        context_dict[key] = value
    
    # Initialize provider
    try:
        provider_config = {
            "name": provider,
            "api_key": api_key,
            "model": model,
        }
        
        ai_provider = get_provider(provider_config)
        ai_provider.validate_config()
        
        if verbose:
            console.print(f"[dim]Provider: {provider}[/dim]")
            console.print(f"[dim]Model: {model or ai_provider.model}[/dim]")
        
    except ProviderError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)
    
    # Initialize cache
    cache_manager = None
    if not no_cache:
        try:
            cache_manager = CacheManager(cache_dir=".ai-cache")
            if verbose:
                console.print("[dim]Cache: enabled[/dim]")
        except Exception as e:
            console.print(f"[yellow]Warning:[/yellow] Cache initialization failed: {e}")
    
    # Initialize generator
    generator = PromptGenerator(
        provider=ai_provider,
        cache_manager=cache_manager,
    )
    
    # Determine output path
    if not output:
        # Auto-generate filename from prompt
        filename = _sanitize_filename(prompt[:50]) + ".md"
        output_path = Path("docs/generated") / filename
    else:
        output_path = Path(output)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if verbose:
        console.print(f"[dim]Output: {output_path}[/dim]")
    
    # Generate content
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating content...", total=None)
            
            if template:
                content = await generator.generate_from_template(
                    template_path=template,
                    context=context_dict,
                    prompt=prompt,
                )
            else:
                content = await generator.generate_from_prompt(prompt)
            
            progress.update(task, completed=True)
        
        # Write to file
        output_path.write_text(content, encoding="utf-8")
        
        # Show success
        console.print()
        console.print(f"[green]✓[/green] Generated: [bold]{output_path}[/bold]")
        
        # Show preview
        if verbose:
            console.print()
            console.print(Panel(
                Markdown(content[:500] + ("..." if len(content) > 500 else "")),
                title="Preview",
                border_style="green",
            ))
        
        # Show stats
        console.print()
        console.print(f"[dim]Length: {len(content)} characters[/dim]")
        if cache_manager:
            stats = cache_manager.get_stats()
            console.print(f"[dim]Cache: {stats['hits']} hits, {stats['misses']} misses[/dim]")
        
    except ProviderError as e:
        console.print()
        console.print(f"[red]Error:[/red] Generation failed: {e}")
        sys.exit(1)
    except Exception as e:
        console.print()
        console.print(f"[red]Error:[/red] Unexpected error: {e}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)
    finally:
        if cache_manager:
            cache_manager.close()


def _sanitize_filename(text: str) -> str:
    """Convert text to safe filename."""
    # Remove special characters
    safe = "".join(c if c.isalnum() or c in " -_" else "" for c in text)
    # Replace spaces with hyphens
    safe = safe.replace(" ", "-")
    # Remove multiple hyphens
    while "--" in safe:
        safe = safe.replace("--", "-")
    # Lowercase
    safe = safe.lower()
    # Remove leading/trailing hyphens
    safe = safe.strip("-")
    return safe or "generated"


@main.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    default="mkdocs.yml",
    help="Path to mkdocs.yml",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def batch(config: str, verbose: bool):
    """Generate documents from config file tasks.
    
    Reads generation tasks from mkdocs.yml and processes them in batch.
    
    Example mkdocs.yml:
    
        plugins:
          - ai-assistant:
              generation:
                tasks:
                  - prompt: "Create API docs"
                    output: docs/api.md
                  - prompt: "Write tutorial"
                    output: docs/tutorial.md
    """
    console.print("[yellow]Batch generation not yet implemented[/yellow]")
    console.print("Coming in next update!")
    # TODO: Implement batch generation


@main.command()
def cache_stats():
    """Show cache statistics."""
    try:
        cache_manager = CacheManager(cache_dir=".ai-cache")
        stats = cache_manager.get_stats()
        
        console.print(Panel.fit(
            f"[bold]Cache Statistics[/bold]\n\n"
            f"Entries: {stats['count']}\n"
            f"Size: {stats['size'] / 1024 / 1024:.2f} MB\n"
            f"Hits: {stats['hits']}\n"
            f"Misses: {stats['misses']}\n"
            f"Hit Rate: {stats['hits'] / max(stats['hits'] + stats['misses'], 1) * 100:.1f}%",
            border_style="cyan",
        ))
        
        cache_manager.close()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.confirmation_option(prompt="Are you sure you want to clear the cache?")
def cache_clear():
    """Clear the cache."""
    try:
        cache_manager = CacheManager(cache_dir=".ai-cache")
        cache_manager.clear()
        console.print("[green]✓[/green] Cache cleared")
        cache_manager.close()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option(
    "--project-root",
    type=click.Path(exists=True),
    default=".",
    help="Project root directory",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    help="Output directory for generated docs",
)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["openrouter", "gemini", "anthropic", "ollama"]),
    default="openrouter",
    help="AI provider to use",
)
@click.option(
    "--api-key",
    envvar="OPENROUTER_API_KEY",
    help="API key for provider",
)
@click.option(
    "--types",
    "-t",
    multiple=True,
    type=click.Choice(["docker_compose", "python_modules", "openapi_specs", "config_files"]),
    help="Asset types to process (can specify multiple)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def process_assets(
    project_root: str,
    output_dir: Optional[str],
    provider: str,
    api_key: Optional[str],
    types: tuple,
    verbose: bool,
):
    """Discover and process project assets into documentation.
    
    Automatically discovers and generates documentation for:
    - Docker Compose files
    - Python modules
    - OpenAPI specifications
    - Configuration files
    
    Examples:
        # Process all assets
        mkdocs-ai process-assets
        
        # Process only Docker Compose files
        mkdocs-ai process-assets -t docker_compose
        
        # Process multiple types
        mkdocs-ai process-assets -t docker_compose -t python_modules
        
        # Custom output directory
        mkdocs-ai process-assets -o docs/api
    """
    from .assets import AssetProcessor, process_project_assets
    
    try:
        project_path = Path(project_root)
        output_path = Path(output_dir) if output_dir else None
        asset_types = list(types) if types else None
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Discovering assets...", total=None)
            
            # Run async processing
            results = asyncio.run(
                process_project_assets(
                    project_root=project_path,
                    provider_name=provider,
                    api_key=api_key,
                    output_dir=output_path,
                    asset_types=asset_types,
                )
            )
            
            progress.update(task, description="Processing complete!")
        
        # Display results
        console.print("\n[bold green]✓ Asset Processing Complete[/bold green]\n")
        
        for asset_type, paths in results.items():
            console.print(f"[cyan]{asset_type}[/cyan]: {len(paths)} files generated")
            if verbose:
                for path in paths:
                    console.print(f"  - {path}")
        
        total_files = sum(len(paths) for paths in results.values())
        console.print(f"\n[bold]Total:[/bold] {total_files} documentation files generated")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


@main.command()
@click.option(
    "--project-root",
    type=click.Path(exists=True),
    default=".",
    help="Project root directory",
)
def discover_assets(project_root: str):
    """Discover assets in project without processing.
    
    Shows what assets would be processed without actually generating documentation.
    
    Example:
        mkdocs-ai discover-assets
    """
    from .assets import AssetDiscovery
    
    try:
        project_path = Path(project_root)
        discovery = AssetDiscovery(project_path)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Discovering assets...", total=None)
            assets = discovery.discover_all()
            progress.update(task, description="Discovery complete!")
        
        # Display results
        console.print("\n[bold]Discovered Assets[/bold]\n")
        
        for asset_type, paths in assets.items():
            console.print(f"[cyan]{asset_type}[/cyan]: {len(paths)} files")
            for path in paths:
                rel_path = path.relative_to(project_path)
                console.print(f"  - {rel_path}")
        
        total_files = sum(len(paths) for paths in assets.values())
        console.print(f"\n[bold]Total:[/bold] {total_files} assets discovered")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file path (default: overwrite input)",
)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["openrouter", "gemini", "anthropic", "ollama"]),
    default="openrouter",
    help="AI provider to use",
)
@click.option(
    "--api-key",
    envvar="OPENROUTER_API_KEY",
    help="API key for provider",
)
@click.option(
    "--level",
    "-l",
    type=click.Choice(["light", "moderate", "aggressive"]),
    default="moderate",
    help="Enhancement level",
)
@click.option(
    "--preview",
    is_flag=True,
    help="Preview changes without applying",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def enhance(
    file_path: str,
    output: Optional[str],
    provider: str,
    api_key: Optional[str],
    level: str,
    preview: bool,
    verbose: bool,
):
    """Enhance documentation content (grammar, clarity, consistency).
    
    Improves documentation quality by:
    - Fixing grammar and spelling errors
    - Improving clarity and readability
    - Ensuring terminology consistency
    - Preserving code blocks and formatting
    
    Enhancement levels:
    - light: Grammar and spelling only
    - moderate: Grammar, spelling, and clarity
    - aggressive: Full enhancement including rewrites
    
    Examples:
        # Enhance a file
        mkdocs-ai enhance docs/guide.md
        
        # Preview changes
        mkdocs-ai enhance docs/guide.md --preview
        
        # Light enhancement only
        mkdocs-ai enhance docs/guide.md --level light
        
        # Save to different file
        mkdocs-ai enhance docs/guide.md -o docs/guide-enhanced.md
    """
    from .enhancement import EnhancementProcessor
    from .providers import create_provider
    from .cache import CacheManager
    
    try:
        file_path_obj = Path(file_path)
        output_path = Path(output) if output else None
        
        # Create provider
        provider_instance = create_provider(provider, api_key=api_key)
        
        # Create cache manager
        cache_manager = CacheManager(cache_dir=".ai-cache")
        
        # Create processor
        processor = EnhancementProcessor(
            provider=provider_instance,
            cache_manager=cache_manager,
            enhancement_level=level,
        )
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Enhancing {file_path_obj.name}...", total=None)
            
            # Read content
            content = file_path_obj.read_text(encoding="utf-8")
            
            if preview:
                # Get preview
                preview_result = asyncio.run(
                    processor.get_enhancement_preview(content, max_length=500)
                )
                
                progress.update(task, description="Preview ready!")
                
                console.print("\n[bold]Preview (first 500 chars)[/bold]\n")
                console.print("[yellow]Original:[/yellow]")
                console.print(preview_result["original"])
                console.print("\n[green]Enhanced:[/green]")
                console.print(preview_result["enhanced"])
                
            else:
                # Enhance content
                enhanced = asyncio.run(processor.enhance_content(content))
                
                # Save result
                output_file = output_path or file_path_obj
                output_file.write_text(enhanced, encoding="utf-8")
                
                progress.update(task, description="Enhancement complete!")
                
                console.print(f"\n[green]✓[/green] Enhanced: {output_file}")
                
                if verbose:
                    # Show quality metrics
                    metrics = asyncio.run(processor.check_quality(enhanced))
                    console.print("\n[bold]Quality Metrics:[/bold]")
                    console.print(f"Grammar: {metrics.get('grammar_score', 0)}/100")
                    console.print(f"Clarity: {metrics.get('clarity_score', 0)}/100")
                    console.print(f"Consistency: {metrics.get('consistency_score', 0)}/100")
                    console.print(f"Readability: {metrics.get('readability_score', 0)}/100")
        
        cache_manager.close()
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


@main.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["openrouter", "gemini", "anthropic", "ollama"]),
    default="openrouter",
    help="AI provider to use",
)
@click.option(
    "--api-key",
    envvar="OPENROUTER_API_KEY",
    help="API key for provider",
)
def check_quality(
    file_path: str,
    provider: str,
    api_key: Optional[str],
):
    """Check documentation quality and get improvement suggestions.
    
    Analyzes:
    - Grammar quality
    - Clarity and readability
    - Terminology consistency
    - Overall quality score
    
    Example:
        mkdocs-ai check-quality docs/guide.md
    """
    from .enhancement import EnhancementProcessor
    from .providers import create_provider
    from .cache import CacheManager
    
    try:
        file_path_obj = Path(file_path)
        
        # Create provider
        provider_instance = create_provider(provider, api_key=api_key)
        
        # Create cache manager
        cache_manager = CacheManager(cache_dir=".ai-cache")
        
        # Create processor
        processor = EnhancementProcessor(
            provider=provider_instance,
            cache_manager=cache_manager,
        )
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing quality...", total=None)
            
            # Read content
            content = file_path_obj.read_text(encoding="utf-8")
            
            # Check quality
            metrics = asyncio.run(processor.check_quality(content))
            
            progress.update(task, description="Analysis complete!")
        
        # Display results
        console.print(f"\n[bold]Quality Report: {file_path_obj.name}[/bold]\n")
        
        console.print("[cyan]Scores:[/cyan]")
        console.print(f"  Grammar: {metrics.get('grammar_score', 0)}/100")
        console.print(f"  Clarity: {metrics.get('clarity_score', 0)}/100")
        console.print(f"  Consistency: {metrics.get('consistency_score', 0)}/100")
        console.print(f"  Readability: {metrics.get('readability_score', 0)}/100")
        
        if metrics.get('issues'):
            console.print("\n[yellow]Issues Found:[/yellow]")
            for issue in metrics['issues']:
                console.print(f"  - {issue}")
        
        if metrics.get('suggestions'):
            console.print("\n[green]Suggestions:[/green]")
            for suggestion in metrics['suggestions']:
                console.print(f"  - {suggestion}")
        
        cache_manager.close()
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option(
    "--docs-dir",
    type=click.Path(exists=True),
    default="docs",
    help="Documentation directory",
)
@click.option(
    "--index-path",
    type=click.Path(),
    default=".ai-cache/search_index.json",
    help="Path to search index",
)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["openrouter", "gemini", "anthropic", "ollama"]),
    default="openrouter",
    help="AI provider to use",
)
@click.option(
    "--api-key",
    envvar="OPENROUTER_API_KEY",
    help="API key for provider",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def build_search_index(
    docs_dir: str,
    index_path: str,
    provider: str,
    api_key: Optional[str],
    verbose: bool,
):
    """Build semantic search index from documentation.
    
    Generates embeddings for all markdown files and creates a searchable index.
    
    Examples:
        # Build index
        mkdocs-ai build-search-index
        
        # Custom docs directory
        mkdocs-ai build-search-index --docs-dir my-docs
        
        # Custom index path
        mkdocs-ai build-search-index --index-path search.json
    """
    from .search import SearchBuilder
    from .providers import create_provider
    from .cache import CacheManager
    
    try:
        docs_path = Path(docs_dir)
        index_path_obj = Path(index_path)
        
        # Find all markdown files
        md_files = list(docs_path.rglob("*.md"))
        
        if not md_files:
            console.print(f"[yellow]No markdown files found in {docs_dir}[/yellow]")
            return
        
        console.print(f"Found {len(md_files)} markdown files")
        
        # Create provider
        provider_instance = create_provider(provider, api_key=api_key)
        
        # Create cache manager
        cache_manager = CacheManager(cache_dir=".ai-cache")
        
        # Create builder
        builder = SearchBuilder(
            provider=provider_instance,
            cache_manager=cache_manager,
            index_path=index_path_obj,
        )
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Building search index...", total=None)
            
            # Build index
            index = asyncio.run(builder.build_index_from_files(md_files))
            
            # Save index
            index.save()
            
            progress.update(task, description="Index built!")
        
        # Display stats
        stats = index.get_stats()
        console.print("\n[bold green]✓ Search Index Built[/bold green]\n")
        console.print(f"Total chunks: {stats['total_chunks']}")
        console.print(f"Total documents: {stats['total_documents']}")
        console.print(f"Index size: {stats['index_size_mb']:.2f} MB")
        console.print(f"Avg chunk length: {stats['avg_chunk_length']:.0f} chars")
        console.print(f"\nIndex saved to: {index_path_obj}")
        
        cache_manager.close()
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


@main.command()
@click.argument("query")
@click.option(
    "--index-path",
    type=click.Path(exists=True),
    default=".ai-cache/search_index.json",
    help="Path to search index",
)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["openrouter", "gemini", "anthropic", "ollama"]),
    default="openrouter",
    help="AI provider to use",
)
@click.option(
    "--api-key",
    envvar="OPENROUTER_API_KEY",
    help="API key for provider",
)
@click.option(
    "--top-k",
    "-k",
    type=int,
    default=5,
    help="Number of results to return",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def search(
    query: str,
    index_path: str,
    provider: str,
    api_key: Optional[str],
    top_k: int,
    verbose: bool,
):
    """Search documentation using semantic search.
    
    Searches the documentation index for relevant content.
    
    Examples:
        # Search documentation
        mkdocs-ai search "How to configure Docker"
        
        # Get more results
        mkdocs-ai search "API reference" -k 10
        
        # Verbose output
        mkdocs-ai search "deployment guide" -v
    """
    from .search import search_documents
    from .providers import create_provider
    from .cache import CacheManager
    
    try:
        index_path_obj = Path(index_path)
        
        if not index_path_obj.exists():
            console.print(f"[red]Error:[/red] Search index not found at {index_path}")
            console.print("Run 'mkdocs-ai build-search-index' first")
            sys.exit(1)
        
        # Create provider
        provider_instance = create_provider(provider, api_key=api_key)
        
        # Create cache manager
        cache_manager = CacheManager(cache_dir=".ai-cache")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Searching...", total=None)
            
            # Search
            results = asyncio.run(
                search_documents(
                    query=query,
                    index_path=index_path_obj,
                    provider=provider_instance,
                    cache_manager=cache_manager,
                    top_k=top_k,
                )
            )
            
            progress.update(task, description="Search complete!")
        
        # Display results
        console.print(f"\n[bold]Search Results for: \"{query}\"[/bold]\n")
        
        if not results:
            console.print("[yellow]No results found[/yellow]")
        else:
            for i, result in enumerate(results, 1):
                score = result.get('score', 0)
                metadata = result.get('metadata', {})
                highlight = result.get('highlight', '')
                
                console.print(f"[cyan]{i}. {metadata.get('filename', 'Unknown')}[/cyan]")
                console.print(f"   Score: {score:.3f}")
                console.print(f"   {highlight}")
                console.print()
                
                if verbose:
                    console.print(f"   Path: {metadata.get('path', 'N/A')}")
                    console.print()
        
        cache_manager.close()
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
