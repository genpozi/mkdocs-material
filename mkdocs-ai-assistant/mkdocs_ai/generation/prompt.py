"""Prompt-based document generation."""

from typing import Optional
from pathlib import Path

from ..providers import AIProvider, ProviderError
from ..cache import CacheManager


class PromptGenerator:
    """Generate documentation from prompts using AI.
    
    This class handles the core document generation logic, including:
    - Prompt engineering for documentation
    - Cache management
    - Template rendering
    - Error handling
    """

    def __init__(
        self,
        provider: AIProvider,
        cache_manager: Optional[CacheManager] = None,
    ):
        """Initialize generator.
        
        Args:
            provider: AI provider instance
            cache_manager: Optional cache manager
        """
        self.provider = provider
        self.cache_manager = cache_manager

    async def generate_from_prompt(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Generate documentation from a prompt.
        
        Args:
            prompt: User prompt describing what to generate
            system_prompt: Optional system prompt for context
            **kwargs: Additional provider parameters
            
        Returns:
            Generated markdown content
            
        Raises:
            ProviderError: If generation fails
        """
        # Check cache first
        if self.cache_manager:
            cached = self.cache_manager.get(
                prompt,
                system_prompt=system_prompt,
                model=self.provider.model,
                **kwargs,
            )
            if cached:
                return cached
        
        # Build system prompt for documentation
        if not system_prompt:
            system_prompt = self._build_documentation_system_prompt()
        
        # Generate content
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            **kwargs,
        )
        
        content = response.content
        
        # Cache the result
        if self.cache_manager:
            self.cache_manager.set(
                prompt,
                content,
                system_prompt=system_prompt,
                model=self.provider.model,
                **kwargs,
            )
        
        return content

    async def generate_from_template(
        self,
        template_path: str,
        context: dict,
        prompt: Optional[str] = None,
    ) -> str:
        """Generate documentation using a Jinja2 template.
        
        The template can contain placeholders that will be filled by AI.
        
        Args:
            template_path: Path to Jinja2 template file
            context: Context variables for template
            prompt: Optional additional prompt for AI
            
        Returns:
            Generated markdown content
            
        Raises:
            ProviderError: If generation fails
            FileNotFoundError: If template not found
        """
        from jinja2 import Template, TemplateError
        
        # Load template
        template_file = Path(template_path)
        if not template_file.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        template_content = template_file.read_text(encoding="utf-8")
        
        try:
            template = Template(template_content)
        except TemplateError as e:
            raise ProviderError(f"Invalid template: {e}")
        
        # Identify AI placeholders in template
        # Format: {{ ai.field_name }}
        ai_fields = self._extract_ai_fields(template_content)
        
        if not ai_fields:
            # No AI fields, just render template
            return template.render(**context)
        
        # Generate content for AI fields
        ai_context = {}
        for field in ai_fields:
            field_prompt = self._build_field_prompt(field, context, prompt)
            content = await self.generate_from_prompt(field_prompt)
            ai_context[field] = content
        
        # Render template with AI-generated content
        full_context = {**context, "ai": ai_context}
        return template.render(**full_context)

    def _build_documentation_system_prompt(self) -> str:
        """Build system prompt optimized for documentation generation."""
        return """You are an expert technical writer creating high-quality documentation.

Your documentation should be:
- Clear and concise
- Well-structured with proper headings
- Include code examples where appropriate
- Use markdown formatting
- Be accurate and technically correct
- Include practical examples
- Be beginner-friendly while remaining comprehensive

Format your response as clean markdown. Do not include meta-commentary about the documentation itself."""

    def _build_field_prompt(
        self,
        field: str,
        context: dict,
        base_prompt: Optional[str] = None,
    ) -> str:
        """Build prompt for a specific template field.
        
        Args:
            field: Field name from template
            context: Template context
            base_prompt: Optional base prompt
            
        Returns:
            Prompt for generating field content
        """
        # Convert field name to readable prompt
        field_readable = field.replace("_", " ").title()
        
        prompt_parts = []
        
        if base_prompt:
            prompt_parts.append(base_prompt)
        
        prompt_parts.append(f"Generate content for: {field_readable}")
        
        # Add context information
        if context:
            context_str = ", ".join(f"{k}={v}" for k, v in context.items())
            prompt_parts.append(f"Context: {context_str}")
        
        return "\n\n".join(prompt_parts)

    def _extract_ai_fields(self, template_content: str) -> list[str]:
        """Extract AI field names from template.
        
        Looks for patterns like {{ ai.field_name }}
        
        Args:
            template_content: Template content
            
        Returns:
            List of field names
        """
        import re
        
        pattern = r'\{\{\s*ai\.(\w+)\s*\}\}'
        matches = re.findall(pattern, template_content)
        return list(set(matches))  # Remove duplicates

    async def enhance_content(
        self,
        content: str,
        enhancement_type: str = "general",
    ) -> str:
        """Enhance existing content.
        
        Args:
            content: Original content
            enhancement_type: Type of enhancement (grammar, clarity, etc.)
            
        Returns:
            Enhanced content
        """
        enhancement_prompts = {
            "grammar": "Fix grammar and spelling errors in the following text. Preserve the original meaning and structure. Only fix errors, don't rewrite.",
            "clarity": "Improve the clarity and readability of the following text. Make it easier to understand while preserving all information.",
            "consistency": "Improve terminology consistency in the following text. Use consistent terms throughout.",
            "general": "Improve the following documentation. Fix grammar, improve clarity, and ensure consistency.",
        }
        
        system_prompt = enhancement_prompts.get(enhancement_type, enhancement_prompts["general"])
        
        prompt = f"{system_prompt}\n\n{content}"
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are an expert editor improving technical documentation.",
        )
        
        return response.content

    async def generate_from_code(
        self,
        code: str,
        language: str,
        doc_type: str = "api",
    ) -> str:
        """Generate documentation from code.
        
        Args:
            code: Source code
            language: Programming language
            doc_type: Type of documentation (api, tutorial, etc.)
            
        Returns:
            Generated documentation
        """
        prompt = f"""Generate {doc_type} documentation for the following {language} code:

```{language}
{code}
```

Include:
- Overview of what the code does
- Function/class descriptions
- Parameter descriptions
- Return value descriptions
- Usage examples
- Any important notes or warnings"""

        return await self.generate_from_prompt(prompt)

    async def generate_from_compose(
        self,
        compose_content: str,
        service_name: Optional[str] = None,
    ) -> str:
        """Generate documentation from Docker Compose file.
        
        Args:
            compose_content: Docker Compose YAML content
            service_name: Optional specific service to document
            
        Returns:
            Generated documentation
        """
        if service_name:
            prompt = f"""Generate documentation for the '{service_name}' service in this Docker Compose file:

```yaml
{compose_content}
```

Include:
- Service purpose and description
- Configuration details
- Environment variables
- Volumes and their purposes
- Network configuration
- Dependencies
- Usage instructions"""
        else:
            prompt = f"""Generate comprehensive documentation for this Docker Compose setup:

```yaml
{compose_content}
```

Include:
- Overview of the entire stack
- Each service and its purpose
- How services interact
- Configuration details
- Environment variables
- Volumes and persistence
- Network architecture
- Getting started instructions
- Common operations"""

        return await self.generate_from_prompt(prompt)
