"""Content enhancement processor."""

from pathlib import Path
from typing import Optional, Dict, Any, List
import re

from ..providers import AIProvider
from ..cache import CacheManager


class EnhancementProcessor:
    """Process and enhance documentation content.
    
    Features:
    - Grammar and spelling corrections
    - Clarity improvements
    - Consistency checking
    - Preserves code blocks and frontmatter
    - Configurable enhancement levels
    """
    
    def __init__(
        self,
        provider: AIProvider,
        cache_manager: Optional[CacheManager] = None,
        enhancement_level: str = "moderate",
    ):
        """Initialize processor.
        
        Args:
            provider: AI provider for enhancements
            cache_manager: Optional cache manager
            enhancement_level: Enhancement level (light, moderate, aggressive)
        """
        self.provider = provider
        self.cache_manager = cache_manager
        self.enhancement_level = enhancement_level
        
        # Enhancement level configurations
        self.level_configs = {
            "light": {
                "fix_grammar": True,
                "fix_spelling": True,
                "improve_clarity": False,
                "check_consistency": False,
                "rewrite_sentences": False,
            },
            "moderate": {
                "fix_grammar": True,
                "fix_spelling": True,
                "improve_clarity": True,
                "check_consistency": True,
                "rewrite_sentences": False,
            },
            "aggressive": {
                "fix_grammar": True,
                "fix_spelling": True,
                "improve_clarity": True,
                "check_consistency": True,
                "rewrite_sentences": True,
            },
        }
    
    async def enhance_content(
        self,
        content: str,
        preserve_code: bool = True,
        preserve_frontmatter: bool = True,
    ) -> str:
        """Enhance markdown content.
        
        Args:
            content: Original markdown content
            preserve_code: Whether to preserve code blocks
            preserve_frontmatter: Whether to preserve frontmatter
            
        Returns:
            Enhanced markdown content
        """
        # Extract and preserve special sections
        preserved_sections = {}
        working_content = content
        
        if preserve_frontmatter:
            working_content, frontmatter = self._extract_frontmatter(working_content)
            if frontmatter:
                preserved_sections["frontmatter"] = frontmatter
        
        if preserve_code:
            working_content, code_blocks = self._extract_code_blocks(working_content)
            preserved_sections["code_blocks"] = code_blocks
        
        # Enhance the content
        enhanced = await self._enhance_text(working_content)
        
        # Restore preserved sections
        enhanced = self._restore_code_blocks(enhanced, preserved_sections.get("code_blocks", {}))
        if "frontmatter" in preserved_sections:
            enhanced = self._restore_frontmatter(enhanced, preserved_sections["frontmatter"])
        
        return enhanced
    
    async def enhance_file(
        self,
        file_path: Path,
        output_path: Optional[Path] = None,
    ) -> Path:
        """Enhance a markdown file.
        
        Args:
            file_path: Path to markdown file
            output_path: Optional output path (defaults to overwriting input)
            
        Returns:
            Path to enhanced file
        """
        content = file_path.read_text(encoding="utf-8")
        enhanced = await self.enhance_content(content)
        
        output = output_path or file_path
        output.write_text(enhanced, encoding="utf-8")
        
        return output
    
    async def _enhance_text(self, text: str) -> str:
        """Enhance text content using AI.
        
        Args:
            text: Text to enhance
            
        Returns:
            Enhanced text
        """
        config = self.level_configs.get(self.enhancement_level, self.level_configs["moderate"])
        
        # Build enhancement prompt based on configuration
        instructions = []
        
        if config["fix_grammar"]:
            instructions.append("Fix any grammar errors")
        if config["fix_spelling"]:
            instructions.append("Correct spelling mistakes")
        if config["improve_clarity"]:
            instructions.append("Improve clarity and readability")
        if config["check_consistency"]:
            instructions.append("Ensure terminology consistency")
        if config["rewrite_sentences"]:
            instructions.append("Rewrite unclear sentences for better flow")
        
        if not instructions:
            return text
        
        prompt = f"""Enhance the following documentation text.

Instructions:
{chr(10).join(f'- {inst}' for inst in instructions)}

Important:
- Preserve all markdown formatting
- Keep the same structure and organization
- Don't add new content, only improve existing text
- Maintain the original tone and style
- Keep technical terms unchanged

Text to enhance:

{text}

Return ONLY the enhanced text, no explanations or meta-commentary."""
        
        # Check cache
        cache_key = f"enhance_{self.enhancement_level}_{text[:100]}"
        if self.cache_manager:
            cached = self.cache_manager.get(
                cache_key,
                model=self.provider.model,
            )
            if cached:
                return cached
        
        # Generate enhancement
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are an expert technical editor improving documentation quality.",
            temperature=0.3,  # Lower temperature for more consistent edits
        )
        
        enhanced = response.content.strip()
        
        # Cache result
        if self.cache_manager:
            self.cache_manager.set(cache_key, enhanced, model=self.provider.model)
        
        return enhanced
    
    def _extract_frontmatter(self, content: str) -> tuple[str, Optional[str]]:
        """Extract YAML frontmatter from content.
        
        Args:
            content: Markdown content
            
        Returns:
            Tuple of (content without frontmatter, frontmatter)
        """
        # Match YAML frontmatter (--- at start and end)
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        
        if match:
            frontmatter = match.group(0)
            content_without = content[len(frontmatter):]
            return content_without, frontmatter
        
        return content, None
    
    def _restore_frontmatter(self, content: str, frontmatter: str) -> str:
        """Restore frontmatter to content.
        
        Args:
            content: Content without frontmatter
            frontmatter: Frontmatter to restore
            
        Returns:
            Content with frontmatter
        """
        return frontmatter + content
    
    def _extract_code_blocks(self, content: str) -> tuple[str, Dict[str, str]]:
        """Extract code blocks from content.
        
        Args:
            content: Markdown content
            
        Returns:
            Tuple of (content with placeholders, dict of code blocks)
        """
        code_blocks = {}
        counter = 0
        
        def replace_code_block(match):
            nonlocal counter
            placeholder = f"__CODE_BLOCK_{counter}__"
            code_blocks[placeholder] = match.group(0)
            counter += 1
            return placeholder
        
        # Match fenced code blocks (``` or ~~~)
        pattern = r'```[\s\S]*?```|~~~[\s\S]*?~~~'
        content_with_placeholders = re.sub(pattern, replace_code_block, content)
        
        # Also match inline code
        def replace_inline_code(match):
            nonlocal counter
            placeholder = f"__INLINE_CODE_{counter}__"
            code_blocks[placeholder] = match.group(0)
            counter += 1
            return placeholder
        
        pattern = r'`[^`\n]+`'
        content_with_placeholders = re.sub(pattern, replace_inline_code, content_with_placeholders)
        
        return content_with_placeholders, code_blocks
    
    def _restore_code_blocks(self, content: str, code_blocks: Dict[str, str]) -> str:
        """Restore code blocks to content.
        
        Args:
            content: Content with placeholders
            code_blocks: Dict of code blocks to restore
            
        Returns:
            Content with code blocks restored
        """
        for placeholder, code_block in code_blocks.items():
            content = content.replace(placeholder, code_block)
        
        return content
    
    async def check_quality(self, content: str) -> Dict[str, Any]:
        """Check content quality and provide metrics.
        
        Args:
            content: Content to check
            
        Returns:
            Quality metrics dictionary
        """
        prompt = f"""Analyze the quality of this documentation and provide metrics.

Content:
{content}

Provide a JSON response with these metrics:
- grammar_score: 0-100 (grammar quality)
- clarity_score: 0-100 (how clear and understandable)
- consistency_score: 0-100 (terminology consistency)
- readability_score: 0-100 (overall readability)
- issues: list of specific issues found
- suggestions: list of improvement suggestions

Return ONLY valid JSON, no other text."""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a documentation quality analyzer.",
            temperature=0.3,
        )
        
        # Parse JSON response
        import json
        try:
            metrics = json.loads(response.content)
            return metrics
        except json.JSONDecodeError:
            # Fallback if AI doesn't return valid JSON
            return {
                "grammar_score": 0,
                "clarity_score": 0,
                "consistency_score": 0,
                "readability_score": 0,
                "issues": ["Could not parse quality metrics"],
                "suggestions": [],
            }
    
    async def get_enhancement_preview(
        self,
        content: str,
        max_length: int = 500,
    ) -> Dict[str, str]:
        """Get a preview of enhancements without applying them.
        
        Args:
            content: Content to preview
            max_length: Maximum length of preview
            
        Returns:
            Dict with 'original' and 'enhanced' preview
        """
        # Take a sample of the content
        sample = content[:max_length]
        
        # Enhance the sample
        enhanced_sample = await self._enhance_text(sample)
        
        return {
            "original": sample,
            "enhanced": enhanced_sample,
        }


async def enhance_markdown_file(
    file_path: Path,
    provider: AIProvider,
    cache_manager: Optional[CacheManager] = None,
    enhancement_level: str = "moderate",
    output_path: Optional[Path] = None,
) -> Path:
    """Convenience function to enhance a markdown file.
    
    Args:
        file_path: Path to markdown file
        provider: AI provider
        cache_manager: Optional cache manager
        enhancement_level: Enhancement level (light, moderate, aggressive)
        output_path: Optional output path
        
    Returns:
        Path to enhanced file
    """
    processor = EnhancementProcessor(
        provider=provider,
        cache_manager=cache_manager,
        enhancement_level=enhancement_level,
    )
    
    return await processor.enhance_file(file_path, output_path)
