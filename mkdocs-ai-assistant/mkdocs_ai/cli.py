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


if __name__ == "__main__":
    main()
