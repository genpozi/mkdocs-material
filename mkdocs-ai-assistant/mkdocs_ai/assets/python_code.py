"""Python code asset processor with mkdocstrings integration."""

import ast
import logging
from pathlib import Path
from typing import Optional

from .base import AssetProcessor
from .models import Asset, Documentation

logger = logging.getLogger("mkdocs.plugins.ai-assistant.assets")


class PythonCodeProcessor(AssetProcessor):
    """Process Python code with mkdocstrings integration."""

    def __init__(self, *args, use_mkdocstrings: bool = True, **kwargs):
        """Initialize processor.

        Args:
            use_mkdocstrings: Whether to use mkdocstrings for API reference
            *args: Positional arguments for base class
            **kwargs: Keyword arguments for base class
        """
        super().__init__(*args, **kwargs)
        self.use_mkdocstrings = use_mkdocstrings

    async def process(self, asset: Asset) -> Documentation:
        """Process Python module.

        Args:
            asset: Python module asset

        Returns:
            Generated documentation
        """
        # Parse module
        module_info = self._parse_module(asset.path)

        # Generate structure
        structure = self.generate_structure(asset)

        # Generate mkdocstrings reference
        api_reference = self._generate_mkdocstrings_ref(module_info, asset)

        # Generate AI summary if available
        summary = ""
        if self.provider:
            summary = await self._generate_summary(module_info)

        # Generate usage examples if available
        examples = ""
        if self.provider:
            examples = await self._generate_examples(module_info)

        # Generate class diagram
        diagram = self._generate_class_diagram(module_info)

        # Combine into documentation
        content = self._combine_content(
            module_name=asset.name,
            summary=summary,
            api_reference=api_reference,
            examples=examples,
        )

        return Documentation(
            content=content,
            diagrams=[diagram] if diagram else [],
            metadata={
                "title": f"API: {asset.name}",
                "type": "python",
                "module": asset.name,
                "classes": [cls["name"] for cls in module_info.get("classes", [])],
                "functions": [
                    func["name"] for func in module_info.get("functions", [])
                ],
            },
            file_path=f"api/{asset.name.replace('.', '/')}.md",
        )

    def generate_structure(self, asset: Asset) -> dict:
        """Generate structured documentation data.

        Args:
            asset: Python module asset

        Returns:
            Structured data
        """
        module_info = self._parse_module(asset.path)
        return {
            "name": asset.name,
            "path": str(asset.path),
            "docstring": module_info.get("docstring", ""),
            "classes": module_info.get("classes", []),
            "functions": module_info.get("functions", []),
        }

    def _parse_module(self, file_path: Path) -> dict:
        """Parse Python module using AST.

        Args:
            file_path: Path to Python file

        Returns:
            Module information
        """
        try:
            with open(file_path, "r") as f:
                source = f.read()

            tree = ast.parse(source)

            module_info = {
                "docstring": ast.get_docstring(tree) or "",
                "classes": [],
                "functions": [],
                "imports": [],
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "docstring": ast.get_docstring(node) or "",
                        "methods": [],
                        "bases": [self._get_name(base) for base in node.bases],
                    }

                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_info["methods"].append(item.name)

                    module_info["classes"].append(class_info)

                elif isinstance(node, ast.FunctionDef) and not isinstance(
                    node, ast.AsyncFunctionDef
                ):
                    # Only top-level functions
                    if isinstance(getattr(node, "parent", None), ast.Module):
                        module_info["functions"].append(
                            {
                                "name": node.name,
                                "docstring": ast.get_docstring(node) or "",
                            }
                        )

            return module_info

        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            return {
                "docstring": "",
                "classes": [],
                "functions": [],
                "imports": [],
            }

    def _get_name(self, node) -> str:
        """Get name from AST node.

        Args:
            node: AST node

        Returns:
            Name string
        """
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)

    def _generate_mkdocstrings_ref(
        self, module_info: dict, asset: Asset
    ) -> Optional[str]:
        """Generate mkdocstrings reference.

        Args:
            module_info: Parsed module information
            asset: Asset being processed

        Returns:
            mkdocstrings reference code
        """
        if not self.use_mkdocstrings:
            return None

        module_path = asset.name

        return f"""
## API Reference

::: {module_path}
    options:
      show_source: true
      show_root_heading: true
      show_root_full_path: false
      members_order: source
      heading_level: 3
"""

    async def _generate_summary(self, module_info: dict) -> str:
        """Generate AI summary of module.

        Args:
            module_info: Parsed module information

        Returns:
            Generated summary
        """
        classes = [cls["name"] for cls in module_info.get("classes", [])]
        functions = [func["name"] for func in module_info.get("functions", [])]

        prompt = f"""
Generate a concise summary of this Python module:

**Docstring**:
{module_info.get('docstring', 'No docstring available')}

**Classes**: {', '.join(classes) if classes else 'None'}
**Functions**: {', '.join(functions) if functions else 'None'}

Provide:
1. What the module does (1-2 sentences)
2. Key features (bullet points)
3. When to use it (1 sentence)

Keep it concise and technical.
"""

        response = await self.provider.generate(prompt)
        return response.content

    async def _generate_examples(self, module_info: dict) -> str:
        """Generate usage examples with AI.

        Args:
            module_info: Parsed module information

        Returns:
            Generated examples
        """
        classes = [cls["name"] for cls in module_info.get("classes", [])]
        functions = [func["name"] for func in module_info.get("functions", [])]

        if not classes and not functions:
            return ""

        prompt = f"""
Generate practical usage examples for this Python module:

**Docstring**:
{module_info.get('docstring', 'No docstring available')}

**Classes**: {', '.join(classes) if classes else 'None'}
**Functions**: {', '.join(functions) if functions else 'None'}

Create 2-3 examples showing:
1. Basic usage
2. Common use case
3. Advanced usage (if applicable)

Use realistic code that would actually work. Include imports.
Format as Markdown code blocks.
"""

        response = await self.provider.generate(prompt)
        return response.content

    def _generate_class_diagram(self, module_info: dict) -> Optional[str]:
        """Generate Mermaid class diagram.

        Args:
            module_info: Parsed module information

        Returns:
            Mermaid diagram code
        """
        classes = module_info.get("classes", [])
        if not classes:
            return None

        mermaid = ["```mermaid", "classDiagram"]

        for cls in classes:
            # Add class
            mermaid.append(f"    class {cls['name']} {{")

            # Add methods (limit to first 5 for readability)
            methods = cls.get("methods", [])[:5]
            for method in methods:
                mermaid.append(f"        +{method}()")

            if len(cls.get("methods", [])) > 5:
                mermaid.append(f"        +... ({len(cls['methods']) - 5} more)")

            mermaid.append("    }")

            # Add inheritance
            for base in cls.get("bases", []):
                if base and base != "object":
                    mermaid.append(f"    {base} <|-- {cls['name']}")

        mermaid.append("```")
        return "\n".join(mermaid)

    def _combine_content(
        self,
        module_name: str,
        summary: str,
        api_reference: Optional[str],
        examples: str,
    ) -> str:
        """Combine all content into final documentation.

        Args:
            module_name: Name of the module
            summary: AI-generated summary
            api_reference: mkdocstrings reference
            examples: AI-generated examples

        Returns:
            Combined documentation
        """
        lines = [f"# {module_name}", ""]

        if summary:
            lines.extend(["## Overview", "", summary, ""])

        if examples:
            lines.extend(["## Examples", "", examples, ""])

        if api_reference:
            lines.extend([api_reference, ""])

        return "\n".join(lines)
