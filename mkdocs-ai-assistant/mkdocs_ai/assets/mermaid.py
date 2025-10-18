"""Mermaid diagram generator for various asset types."""

import logging
from typing import Optional

logger = logging.getLogger("mkdocs.plugins.ai-assistant.assets")


class MermaidGenerator:
    """Generate Mermaid diagrams from various data structures."""

    @staticmethod
    def generate_class_diagram(classes: list[dict]) -> Optional[str]:
        """Generate class diagram from class information.

        Args:
            classes: List of class dictionaries with name, methods, bases

        Returns:
            Mermaid diagram code or None if no classes
        """
        if not classes:
            return None

        mermaid = ["```mermaid", "classDiagram"]

        for cls in classes:
            class_name = cls.get("name", "Unknown")

            # Add class with methods
            mermaid.append(f"    class {class_name} {{")

            # Add methods (limit to avoid clutter)
            methods = cls.get("methods", [])[:10]
            for method in methods:
                # Determine visibility
                if method.startswith("_") and not method.startswith("__"):
                    visibility = "-"  # private
                elif method.startswith("__"):
                    visibility = "#"  # protected
                else:
                    visibility = "+"  # public

                mermaid.append(f"        {visibility}{method}()")

            if len(cls.get("methods", [])) > 10:
                mermaid.append(f"        ... ({len(cls['methods']) - 10} more)")

            mermaid.append("    }")

            # Add inheritance relationships
            bases = cls.get("bases", [])
            for base in bases:
                if base and base not in ["object", "type"]:
                    mermaid.append(f"    {base} <|-- {class_name}")

        mermaid.append("```")
        return "\n".join(mermaid)

    @staticmethod
    def generate_sequence_diagram(interactions: list[dict]) -> Optional[str]:
        """Generate sequence diagram from interactions.

        Args:
            interactions: List of interaction dictionaries

        Returns:
            Mermaid diagram code or None if no interactions
        """
        if not interactions:
            return None

        mermaid = ["```mermaid", "sequenceDiagram"]

        # Add participants
        participants = set()
        for interaction in interactions:
            participants.add(interaction.get("from", "Unknown"))
            participants.add(interaction.get("to", "Unknown"))

        for participant in sorted(participants):
            mermaid.append(f"    participant {participant}")

        # Add interactions
        for interaction in interactions:
            from_actor = interaction.get("from", "Unknown")
            to_actor = interaction.get("to", "Unknown")
            message = interaction.get("message", "")
            arrow = interaction.get("arrow", "->")  # ->, -->>, -x, --x

            mermaid.append(f"    {from_actor}{arrow}{to_actor}: {message}")

        mermaid.append("```")
        return "\n".join(mermaid)

    @staticmethod
    def generate_architecture_diagram(components: list[dict]) -> Optional[str]:
        """Generate architecture diagram from components.

        Args:
            components: List of component dictionaries

        Returns:
            Mermaid diagram code or None if no components
        """
        if not components:
            return None

        mermaid = ["```mermaid", "graph TD"]

        # Add components
        for component in components:
            comp_id = component.get("id", "unknown")
            comp_name = component.get("name", comp_id)
            comp_type = component.get("type", "component")

            # Different shapes for different types
            if comp_type == "database":
                mermaid.append(f"    {comp_id}[({comp_name})]")
            elif comp_type == "service":
                mermaid.append(f"    {comp_id}[{comp_name}]")
            elif comp_type == "external":
                mermaid.append(f"    {comp_id}[/{comp_name}/]")
            else:
                mermaid.append(f"    {comp_id}[{comp_name}]")

        # Add relationships
        for component in components:
            comp_id = component.get("id", "unknown")
            depends_on = component.get("depends_on", [])

            for dep in depends_on:
                dep_id = dep if isinstance(dep, str) else dep.get("id", "unknown")
                label = (
                    dep.get("label", "")
                    if isinstance(dep, dict)
                    else ""
                )

                if label:
                    mermaid.append(f"    {comp_id} -->|{label}| {dep_id}")
                else:
                    mermaid.append(f"    {comp_id} --> {dep_id}")

        # Add styling
        for component in components:
            comp_id = component.get("id", "unknown")
            comp_type = component.get("type", "component")

            if comp_type == "database":
                mermaid.append(f"    style {comp_id} fill:#f9f,stroke:#333")
            elif comp_type == "external":
                mermaid.append(f"    style {comp_id} fill:#ff9,stroke:#333")

        mermaid.append("```")
        return "\n".join(mermaid)

    @staticmethod
    def generate_dependency_graph(dependencies: dict) -> Optional[str]:
        """Generate dependency graph.

        Args:
            dependencies: Dictionary mapping items to their dependencies

        Returns:
            Mermaid diagram code or None if no dependencies
        """
        if not dependencies:
            return None

        mermaid = ["```mermaid", "graph LR"]

        # Add nodes and edges
        for item, deps in dependencies.items():
            # Sanitize names for Mermaid
            item_id = item.replace("-", "_").replace(".", "_")

            if not deps:
                # Standalone node
                mermaid.append(f"    {item_id}[{item}]")
            else:
                for dep in deps:
                    dep_id = dep.replace("-", "_").replace(".", "_")
                    mermaid.append(f"    {item_id}[{item}] --> {dep_id}[{dep}]")

        mermaid.append("```")
        return "\n".join(mermaid)

    @staticmethod
    def generate_flowchart(steps: list[dict]) -> Optional[str]:
        """Generate flowchart from steps.

        Args:
            steps: List of step dictionaries

        Returns:
            Mermaid diagram code or None if no steps
        """
        if not steps:
            return None

        mermaid = ["```mermaid", "flowchart TD"]

        for i, step in enumerate(steps):
            step_id = step.get("id", f"step{i}")
            step_text = step.get("text", "")
            step_type = step.get("type", "process")  # process, decision, start, end

            # Different shapes for different types
            if step_type == "start":
                mermaid.append(f"    {step_id}([{step_text}])")
            elif step_type == "end":
                mermaid.append(f"    {step_id}([{step_text}])")
            elif step_type == "decision":
                mermaid.append(f"    {step_id}{{{step_text}}}")
            else:
                mermaid.append(f"    {step_id}[{step_text}]")

            # Add connections
            next_steps = step.get("next", [])
            if isinstance(next_steps, str):
                next_steps = [next_steps]

            for next_step in next_steps:
                if isinstance(next_step, dict):
                    next_id = next_step.get("id", "")
                    label = next_step.get("label", "")
                    if label:
                        mermaid.append(f"    {step_id} -->|{label}| {next_id}")
                    else:
                        mermaid.append(f"    {step_id} --> {next_id}")
                else:
                    mermaid.append(f"    {step_id} --> {next_step}")

        mermaid.append("```")
        return "\n".join(mermaid)

    @staticmethod
    def generate_entity_relationship(entities: list[dict]) -> Optional[str]:
        """Generate entity relationship diagram.

        Args:
            entities: List of entity dictionaries

        Returns:
            Mermaid diagram code or None if no entities
        """
        if not entities:
            return None

        mermaid = ["```mermaid", "erDiagram"]

        # Add entities with attributes
        for entity in entities:
            entity_name = entity.get("name", "Unknown")
            attributes = entity.get("attributes", [])

            if attributes:
                mermaid.append(f"    {entity_name} {{")
                for attr in attributes:
                    attr_name = attr.get("name", "")
                    attr_type = attr.get("type", "string")
                    attr_key = attr.get("key", "")  # PK, FK

                    if attr_key:
                        mermaid.append(f"        {attr_type} {attr_name} {attr_key}")
                    else:
                        mermaid.append(f"        {attr_type} {attr_name}")
                mermaid.append("    }")
            else:
                mermaid.append(f"    {entity_name}")

        # Add relationships
        for entity in entities:
            entity_name = entity.get("name", "Unknown")
            relationships = entity.get("relationships", [])

            for rel in relationships:
                target = rel.get("target", "")
                rel_type = rel.get("type", "||--||")  # ||--||, ||--o{, etc.
                label = rel.get("label", "")

                if label:
                    mermaid.append(
                        f"    {entity_name} {rel_type} {target} : {label}"
                    )
                else:
                    mermaid.append(f"    {entity_name} {rel_type} {target}")

        mermaid.append("```")
        return "\n".join(mermaid)
