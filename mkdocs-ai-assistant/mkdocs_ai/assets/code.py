"""Code documentation processor."""

from pathlib import Path
from typing import Dict, List, Any, Optional
import ast
import re

from ..providers import AIProvider
from ..cache import CacheManager


class CodeProcessor:
    """Generate documentation from source code.
    
    Features:
    - API documentation
    - Class diagrams (Mermaid)
    - Function/method documentation
    - Module overview
    - Usage examples
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
    
    async def process_python_module(
        self,
        module_path: Path,
        include_diagram: bool = True,
    ) -> str:
        """Process a Python module into documentation.
        
        Args:
            module_path: Path to Python file
            include_diagram: Whether to include class diagram
            
        Returns:
            Generated markdown documentation
        """
        # Parse Python code
        code = module_path.read_text(encoding="utf-8")
        tree = ast.parse(code)
        
        # Extract module info
        module_info = self._extract_module_info(tree, code)
        
        # Generate documentation sections
        sections = []
        
        # Module overview
        sections.append(await self._generate_module_overview(
            module_path,
            module_info,
            code,
        ))
        
        # Class diagram
        if include_diagram and module_info["classes"]:
            diagram = self._generate_class_diagram(module_info["classes"])
            sections.append(f"## Class Diagram\n\n{diagram}")
        
        # Classes
        if module_info["classes"]:
            sections.append(await self._generate_classes_docs(
                module_info["classes"],
                code,
            ))
        
        # Functions
        if module_info["functions"]:
            sections.append(await self._generate_functions_docs(
                module_info["functions"],
                code,
            ))
        
        # Usage examples
        sections.append(await self._generate_usage_examples(
            module_path,
            module_info,
            code,
        ))
        
        return "\n\n".join(sections)
    
    async def process_class(
        self,
        module_path: Path,
        class_name: str,
    ) -> str:
        """Process a single class from a Python module.
        
        Args:
            module_path: Path to Python file
            class_name: Name of class to document
            
        Returns:
            Generated markdown documentation for class
        """
        code = module_path.read_text(encoding="utf-8")
        tree = ast.parse(code)
        
        # Find class
        class_node = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                class_node = node
                break
        
        if not class_node:
            raise ValueError(f"Class '{class_name}' not found in {module_path}")
        
        class_info = self._extract_class_info(class_node, code)
        
        return await self._generate_class_doc(class_info, code)
    
    def _extract_module_info(
        self,
        tree: ast.Module,
        code: str,
    ) -> Dict[str, Any]:
        """Extract information from module AST.
        
        Args:
            tree: AST tree
            code: Source code
            
        Returns:
            Module information dictionary
        """
        info = {
            "docstring": ast.get_docstring(tree),
            "classes": [],
            "functions": [],
            "imports": [],
        }
        
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                info["classes"].append(self._extract_class_info(node, code))
            elif isinstance(node, ast.FunctionDef):
                info["functions"].append(self._extract_function_info(node, code))
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                info["imports"].append(self._extract_import_info(node))
        
        return info
    
    def _extract_class_info(
        self,
        node: ast.ClassDef,
        code: str,
    ) -> Dict[str, Any]:
        """Extract information from class node.
        
        Args:
            node: Class AST node
            code: Source code
            
        Returns:
            Class information dictionary
        """
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(self._extract_function_info(item, code))
        
        return {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "bases": [self._get_name(base) for base in node.bases],
            "methods": methods,
            "decorators": [self._get_name(dec) for dec in node.decorator_list],
        }
    
    def _extract_function_info(
        self,
        node: ast.FunctionDef,
        code: str,
    ) -> Dict[str, Any]:
        """Extract information from function node.
        
        Args:
            node: Function AST node
            code: Source code
            
        Returns:
            Function information dictionary
        """
        args = []
        for arg in node.args.args:
            arg_info = {"name": arg.arg}
            if arg.annotation:
                arg_info["type"] = self._get_name(arg.annotation)
            args.append(arg_info)
        
        return_type = None
        if node.returns:
            return_type = self._get_name(node.returns)
        
        return {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "args": args,
            "return_type": return_type,
            "decorators": [self._get_name(dec) for dec in node.decorator_list],
            "is_async": isinstance(node, ast.AsyncFunctionDef),
        }
    
    def _extract_import_info(self, node: ast.AST) -> str:
        """Extract import statement.
        
        Args:
            node: Import AST node
            
        Returns:
            Import statement string
        """
        if isinstance(node, ast.Import):
            return ", ".join(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = ", ".join(alias.name for alias in node.names)
            return f"{module}: {names}"
        return ""
    
    def _get_name(self, node: ast.AST) -> str:
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
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[{self._get_name(node.slice)}]"
        return str(node)
    
    async def _generate_module_overview(
        self,
        module_path: Path,
        module_info: Dict[str, Any],
        code: str,
    ) -> str:
        """Generate module overview section.
        
        Args:
            module_path: Path to module
            module_info: Extracted module information
            code: Source code
            
        Returns:
            Overview markdown
        """
        prompt = f"""Generate an overview for this Python module.

Module: {module_path.name}
Classes: {', '.join(c['name'] for c in module_info['classes'])}
Functions: {', '.join(f['name'] for f in module_info['functions'])}

Module docstring:
{module_info['docstring'] or 'No docstring'}

Write a brief overview explaining:
- What this module does
- Main classes and their purposes
- Main functions and their purposes
- How to use this module"""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a technical writer documenting Python code.",
        )
        
        return f"# {module_path.stem} Module\n\n{response.content}"
    
    async def _generate_classes_docs(
        self,
        classes: List[Dict[str, Any]],
        code: str,
    ) -> str:
        """Generate documentation for all classes.
        
        Args:
            classes: List of class information
            code: Source code
            
        Returns:
            Classes documentation markdown
        """
        sections = ["## Classes\n"]
        
        for class_info in classes:
            class_doc = await self._generate_class_doc(class_info, code)
            sections.append(class_doc)
        
        return "\n\n".join(sections)
    
    async def _generate_class_doc(
        self,
        class_info: Dict[str, Any],
        code: str,
    ) -> str:
        """Generate documentation for a single class.
        
        Args:
            class_info: Class information
            code: Source code
            
        Returns:
            Class documentation markdown
        """
        sections = [f"### {class_info['name']}\n"]
        
        # Docstring
        if class_info["docstring"]:
            sections.append(class_info["docstring"])
        
        # Inheritance
        if class_info["bases"]:
            bases = ", ".join(f"`{base}`" for base in class_info["bases"])
            sections.append(f"\n**Inherits from**: {bases}")
        
        # Methods
        if class_info["methods"]:
            sections.append("\n**Methods**:\n")
            for method in class_info["methods"]:
                method_sig = self._format_function_signature(method)
                sections.append(f"- `{method_sig}`")
                if method["docstring"]:
                    # First line of docstring
                    first_line = method["docstring"].split("\n")[0]
                    sections.append(f"  - {first_line}")
        
        return "\n".join(sections)
    
    async def _generate_functions_docs(
        self,
        functions: List[Dict[str, Any]],
        code: str,
    ) -> str:
        """Generate documentation for all functions.
        
        Args:
            functions: List of function information
            code: Source code
            
        Returns:
            Functions documentation markdown
        """
        sections = ["## Functions\n"]
        
        for func_info in functions:
            sections.append(f"### {func_info['name']}\n")
            
            # Signature
            sig = self._format_function_signature(func_info)
            sections.append(f"```python\n{sig}\n```")
            
            # Docstring
            if func_info["docstring"]:
                sections.append(f"\n{func_info['docstring']}")
        
        return "\n\n".join(sections)
    
    def _format_function_signature(self, func_info: Dict[str, Any]) -> str:
        """Format function signature.
        
        Args:
            func_info: Function information
            
        Returns:
            Formatted signature string
        """
        args = []
        for arg in func_info["args"]:
            if "type" in arg:
                args.append(f"{arg['name']}: {arg['type']}")
            else:
                args.append(arg["name"])
        
        sig = f"{func_info['name']}({', '.join(args)})"
        
        if func_info["return_type"]:
            sig += f" -> {func_info['return_type']}"
        
        if func_info["is_async"]:
            sig = f"async {sig}"
        
        return sig
    
    def _generate_class_diagram(
        self,
        classes: List[Dict[str, Any]],
    ) -> str:
        """Generate Mermaid class diagram.
        
        Args:
            classes: List of class information
            
        Returns:
            Mermaid diagram markdown
        """
        lines = ["```mermaid", "classDiagram"]
        
        for class_info in classes:
            class_name = class_info["name"]
            
            # Class definition
            lines.append(f"    class {class_name} {{")
            
            # Methods
            for method in class_info["methods"]:
                method_name = method["name"]
                return_type = method.get("return_type", "")
                if return_type:
                    lines.append(f"        +{method_name}() {return_type}")
                else:
                    lines.append(f"        +{method_name}()")
            
            lines.append("    }")
            
            # Inheritance
            for base in class_info["bases"]:
                lines.append(f"    {base} <|-- {class_name}")
        
        lines.append("```")
        
        return "\n".join(lines)
    
    async def _generate_usage_examples(
        self,
        module_path: Path,
        module_info: Dict[str, Any],
        code: str,
    ) -> str:
        """Generate usage examples section.
        
        Args:
            module_path: Path to module
            module_info: Module information
            code: Source code
            
        Returns:
            Usage examples markdown
        """
        prompt = f"""Generate usage examples for this Python module.

Module: {module_path.name}
Classes: {', '.join(c['name'] for c in module_info['classes'])}
Functions: {', '.join(f['name'] for f in module_info['functions'])}

Generate 2-3 practical code examples showing how to use this module.
Include imports and complete, runnable examples."""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a technical writer creating code examples.",
        )
        
        return f"## Usage Examples\n\n{response.content}"
