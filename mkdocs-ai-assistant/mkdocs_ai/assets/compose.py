"""Docker Compose documentation processor."""

from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

from ..providers import AIProvider
from ..cache import CacheManager


class ComposeProcessor:
    """Generate documentation from Docker Compose files.
    
    Features:
    - Service documentation
    - Architecture diagrams (Mermaid)
    - Network topology
    - Volume documentation
    - Environment variable reference
    """
    
    def __init__(
        self,
        provider: AIProvider,
        cache_manager: Optional[CacheManager] = None,
    ):
        """Initialize processor.
        
        Args:
            provider: AI provider for generation
            cache_manager: Optional cache manager
        """
        self.provider = provider
        self.cache_manager = cache_manager
    
    async def process_compose_file(
        self,
        compose_path: Path,
        include_diagram: bool = True,
    ) -> str:
        """Process a Docker Compose file into documentation.
        
        Args:
            compose_path: Path to docker-compose.yml
            include_diagram: Whether to include Mermaid diagram
            
        Returns:
            Generated markdown documentation
        """
        # Parse compose file
        compose_data = self._parse_compose_file(compose_path)
        
        # Generate documentation sections
        sections = []
        
        # Overview
        sections.append(await self._generate_overview(compose_data, compose_path))
        
        # Architecture diagram
        if include_diagram:
            diagram = self._generate_architecture_diagram(compose_data)
            sections.append(f"## Architecture\n\n{diagram}")
        
        # Services
        sections.append(await self._generate_services_docs(compose_data))
        
        # Networks
        if "networks" in compose_data:
            sections.append(self._generate_networks_docs(compose_data["networks"]))
        
        # Volumes
        if "volumes" in compose_data:
            sections.append(self._generate_volumes_docs(compose_data["volumes"]))
        
        # Getting started
        sections.append(self._generate_getting_started(compose_path))
        
        return "\n\n".join(sections)
    
    async def process_service(
        self,
        compose_path: Path,
        service_name: str,
    ) -> str:
        """Process a single service from Docker Compose file.
        
        Args:
            compose_path: Path to docker-compose.yml
            service_name: Name of service to document
            
        Returns:
            Generated markdown documentation for service
        """
        compose_data = self._parse_compose_file(compose_path)
        
        if service_name not in compose_data.get("services", {}):
            raise ValueError(f"Service '{service_name}' not found in {compose_path}")
        
        service = compose_data["services"][service_name]
        
        return await self._generate_service_doc(service_name, service, compose_data)
    
    def _parse_compose_file(self, compose_path: Path) -> Dict[str, Any]:
        """Parse Docker Compose YAML file.
        
        Args:
            compose_path: Path to compose file
            
        Returns:
            Parsed compose data
        """
        content = compose_path.read_text(encoding="utf-8")
        return yaml.safe_load(content)
    
    async def _generate_overview(
        self,
        compose_data: Dict[str, Any],
        compose_path: Path,
    ) -> str:
        """Generate overview section.
        
        Args:
            compose_data: Parsed compose data
            compose_path: Path to compose file
            
        Returns:
            Overview markdown
        """
        services = list(compose_data.get("services", {}).keys())
        
        prompt = f"""Generate an overview for this Docker Compose setup.

File: {compose_path.name}
Services: {', '.join(services)}

Compose content:
```yaml
{yaml.dump(compose_data, default_flow_style=False)}
```

Write a brief overview explaining:
- What this Docker Compose setup does
- The main services and their roles
- The overall purpose of the stack"""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a technical writer documenting Docker infrastructure.",
        )
        
        return f"# {compose_path.stem} Documentation\n\n{response.content}"
    
    async def _generate_services_docs(
        self,
        compose_data: Dict[str, Any],
    ) -> str:
        """Generate documentation for all services.
        
        Args:
            compose_data: Parsed compose data
            
        Returns:
            Services documentation markdown
        """
        services = compose_data.get("services", {})
        
        if not services:
            return ""
        
        sections = ["## Services\n"]
        
        for service_name, service_config in services.items():
            service_doc = await self._generate_service_doc(
                service_name,
                service_config,
                compose_data,
            )
            sections.append(service_doc)
        
        return "\n\n".join(sections)
    
    async def _generate_service_doc(
        self,
        service_name: str,
        service_config: Dict[str, Any],
        compose_data: Dict[str, Any],
    ) -> str:
        """Generate documentation for a single service.
        
        Args:
            service_name: Name of service
            service_config: Service configuration
            compose_data: Full compose data for context
            
        Returns:
            Service documentation markdown
        """
        # Build service info
        image = service_config.get("image", "N/A")
        build = service_config.get("build", None)
        ports = service_config.get("ports", [])
        environment = service_config.get("environment", {})
        volumes = service_config.get("volumes", [])
        depends_on = service_config.get("depends_on", [])
        
        sections = [f"### {service_name}\n"]
        
        # Basic info
        if image != "N/A":
            sections.append(f"**Image**: `{image}`")
        if build:
            sections.append(f"**Build**: `{build}`")
        
        # Ports
        if ports:
            sections.append("\n**Ports**:")
            for port in ports:
                sections.append(f"- `{port}`")
        
        # Environment variables
        if environment:
            sections.append("\n**Environment Variables**:")
            if isinstance(environment, dict):
                for key, value in environment.items():
                    sections.append(f"- `{key}`: {value}")
            else:
                for env in environment:
                    sections.append(f"- `{env}`")
        
        # Volumes
        if volumes:
            sections.append("\n**Volumes**:")
            for volume in volumes:
                sections.append(f"- `{volume}`")
        
        # Dependencies
        if depends_on:
            sections.append("\n**Dependencies**:")
            for dep in depends_on:
                sections.append(f"- `{dep}`")
        
        return "\n".join(sections)
    
    def _generate_architecture_diagram(
        self,
        compose_data: Dict[str, Any],
    ) -> str:
        """Generate Mermaid architecture diagram.
        
        Args:
            compose_data: Parsed compose data
            
        Returns:
            Mermaid diagram markdown
        """
        services = compose_data.get("services", {})
        
        if not services:
            return ""
        
        lines = ["```mermaid", "graph TB"]
        
        # Add services as nodes
        for service_name in services.keys():
            # Sanitize name for Mermaid
            node_id = service_name.replace("-", "_").replace(".", "_")
            lines.append(f"    {node_id}[{service_name}]")
        
        # Add dependencies as edges
        for service_name, service_config in services.items():
            node_id = service_name.replace("-", "_").replace(".", "_")
            depends_on = service_config.get("depends_on", [])
            
            for dep in depends_on:
                dep_id = dep.replace("-", "_").replace(".", "_")
                lines.append(f"    {node_id} --> {dep_id}")
        
        lines.append("```")
        
        return "\n".join(lines)
    
    def _generate_networks_docs(self, networks: Dict[str, Any]) -> str:
        """Generate networks documentation.
        
        Args:
            networks: Networks configuration
            
        Returns:
            Networks documentation markdown
        """
        sections = ["## Networks\n"]
        
        for network_name, network_config in networks.items():
            sections.append(f"### {network_name}")
            
            if network_config:
                driver = network_config.get("driver", "bridge")
                sections.append(f"**Driver**: `{driver}`")
        
        return "\n\n".join(sections)
    
    def _generate_volumes_docs(self, volumes: Dict[str, Any]) -> str:
        """Generate volumes documentation.
        
        Args:
            volumes: Volumes configuration
            
        Returns:
            Volumes documentation markdown
        """
        sections = ["## Volumes\n"]
        
        for volume_name, volume_config in volumes.items():
            sections.append(f"### {volume_name}")
            
            if volume_config:
                driver = volume_config.get("driver", "local")
                sections.append(f"**Driver**: `{driver}`")
        
        return "\n\n".join(sections)
    
    def _generate_getting_started(self, compose_path: Path) -> str:
        """Generate getting started section.
        
        Args:
            compose_path: Path to compose file
            
        Returns:
            Getting started markdown
        """
        return f"""## Getting Started

### Start Services

```bash
docker-compose -f {compose_path.name} up -d
```

### View Logs

```bash
docker-compose -f {compose_path.name} logs -f
```

### Stop Services

```bash
docker-compose -f {compose_path.name} down
```

### Rebuild Services

```bash
docker-compose -f {compose_path.name} up -d --build
```"""
