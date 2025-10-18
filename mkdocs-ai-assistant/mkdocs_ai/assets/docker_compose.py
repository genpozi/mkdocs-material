"""Docker Compose asset processor."""

import logging
from pathlib import Path
from typing import Optional

import yaml

from .base import AssetProcessor
from .models import Asset, Documentation

logger = logging.getLogger("mkdocs.plugins.ai-assistant.assets")


class DockerComposeProcessor(AssetProcessor):
    """Process Docker Compose files into documentation."""

    async def process(self, asset: Asset) -> Documentation:
        """Process Docker Compose file.

        Args:
            asset: Docker Compose asset

        Returns:
            Generated documentation
        """
        # Parse YAML
        compose_data = self._parse_compose(asset.path)

        # Generate structure
        structure = self.generate_structure(asset)

        # Generate Mermaid diagram
        diagram = self._generate_architecture_diagram(compose_data)

        # Enhance with AI if available
        if self.provider:
            content = await self._generate_ai_docs(structure, compose_data)
        else:
            content = self._generate_basic_docs(structure, compose_data)

        return Documentation(
            content=content,
            diagrams=[diagram] if diagram else [],
            metadata={
                "title": f"Docker Compose: {asset.name}",
                "type": "docker-compose",
                "services": list(compose_data.get("services", {}).keys()),
            },
            file_path=f"docker-compose-{asset.name}.md",
        )

    def generate_structure(self, asset: Asset) -> dict:
        """Generate structured documentation data.

        Args:
            asset: Docker Compose asset

        Returns:
            Structured data
        """
        compose_data = self._parse_compose(asset.path)

        services = {}
        for name, config in compose_data.get("services", {}).items():
            services[name] = {
                "image": config.get("image", "N/A"),
                "ports": config.get("ports", []),
                "volumes": config.get("volumes", []),
                "environment": config.get("environment", {}),
                "depends_on": config.get("depends_on", []),
                "networks": config.get("networks", []),
            }

        return {
            "name": asset.name,
            "services": services,
            "networks": compose_data.get("networks", {}),
            "volumes": compose_data.get("volumes", {}),
        }

    def _parse_compose(self, file_path: Path) -> dict:
        """Parse Docker Compose YAML file.

        Args:
            file_path: Path to compose file

        Returns:
            Parsed compose data
        """
        try:
            with open(file_path, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            return {}

    def _generate_architecture_diagram(self, compose_data: dict) -> Optional[str]:
        """Generate Mermaid architecture diagram.

        Args:
            compose_data: Parsed compose data

        Returns:
            Mermaid diagram code
        """
        services = compose_data.get("services", {})
        if not services:
            return None

        mermaid = ["```mermaid", "graph TD"]

        # Add services
        for name in services.keys():
            # Sanitize name for Mermaid
            node_id = name.replace("-", "_").replace(".", "_")
            mermaid.append(f"    {node_id}[{name}]")

        # Add dependencies
        for name, config in services.items():
            node_id = name.replace("-", "_").replace(".", "_")
            depends_on = config.get("depends_on", [])

            if isinstance(depends_on, list):
                for dep in depends_on:
                    dep_id = dep.replace("-", "_").replace(".", "_")
                    mermaid.append(f"    {node_id} --> {dep_id}")
            elif isinstance(depends_on, dict):
                for dep in depends_on.keys():
                    dep_id = dep.replace("-", "_").replace(".", "_")
                    mermaid.append(f"    {node_id} --> {dep_id}")

        # Add networks
        networks = compose_data.get("networks", {})
        for name, config in services.items():
            node_id = name.replace("-", "_").replace(".", "_")
            service_networks = config.get("networks", [])

            if isinstance(service_networks, list):
                for network in service_networks:
                    net_id = f"net_{network}".replace("-", "_").replace(".", "_")
                    mermaid.append(f"    {node_id} -.-> {net_id}[{network}]")
                    mermaid.append(f"    style {net_id} fill:#e1f5ff")

        mermaid.append("```")
        return "\n".join(mermaid)

    async def _generate_ai_docs(self, structure: dict, compose_data: dict) -> str:
        """Generate AI-enhanced documentation.

        Args:
            structure: Structured data
            compose_data: Raw compose data

        Returns:
            Generated documentation
        """
        services_desc = "\n".join(
            [
                f"- **{name}**: {info['image']}"
                for name, info in structure["services"].items()
            ]
        )

        prompt = f"""
Generate comprehensive documentation for this Docker Compose setup:

**Services**:
{services_desc}

**Networks**: {', '.join(structure['networks'].keys()) if structure['networks'] else 'default'}
**Volumes**: {', '.join(structure['volumes'].keys()) if structure['volumes'] else 'none'}

Create documentation that includes:
1. Overview of the stack
2. Service descriptions
3. Port mappings
4. Volume mounts
5. Network configuration
6. Environment variables
7. Dependencies between services
8. How to start/stop the stack
9. Common troubleshooting tips

Format as Markdown with proper headings and structure.
"""

        response = await self.provider.generate(prompt)
        return response.content

    def _generate_basic_docs(self, structure: dict, compose_data: dict) -> str:
        """Generate basic documentation without AI.

        Args:
            structure: Structured data
            compose_data: Raw compose data

        Returns:
            Basic documentation
        """
        lines = [
            f"# Docker Compose: {structure['name']}",
            "",
            "## Services",
            "",
        ]

        for name, info in structure["services"].items():
            lines.extend(
                [
                    f"### {name}",
                    "",
                    f"**Image**: `{info['image']}`",
                    "",
                ]
            )

            if info["ports"]:
                lines.append("**Ports**:")
                for port in info["ports"]:
                    lines.append(f"- `{port}`")
                lines.append("")

            if info["volumes"]:
                lines.append("**Volumes**:")
                for volume in info["volumes"]:
                    lines.append(f"- `{volume}`")
                lines.append("")

            if info["depends_on"]:
                lines.append("**Depends on**:")
                for dep in info["depends_on"]:
                    lines.append(f"- `{dep}`")
                lines.append("")

        if structure["networks"]:
            lines.extend(["## Networks", ""])
            for network in structure["networks"].keys():
                lines.append(f"- `{network}`")
            lines.append("")

        if structure["volumes"]:
            lines.extend(["## Volumes", ""])
            for volume in structure["volumes"].keys():
                lines.append(f"- `{volume}`")
            lines.append("")

        return "\n".join(lines)
