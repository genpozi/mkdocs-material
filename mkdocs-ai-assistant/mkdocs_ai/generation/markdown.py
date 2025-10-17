"""Markdown syntax processing for AI generation."""

import re
import logging
from typing import Optional

from ..providers import AIProvider, ProviderError
from ..cache import CacheManager
from .prompt import PromptGenerator

log = logging.getLogger("mkdocs.plugins.ai-assistant.generation")


class MarkdownProcessor:
    """Process markdown files for AI-GENERATE comments.
    
    Supports syntax:
    - <!-- AI-GENERATE: prompt -->
    - <!-- AI-GENERATE: prompt | options -->
    - <!-- AI-GENERATE-START: prompt -->...<!-- AI-GENERATE-END -->
    """

    # Regex patterns for AI comments
    SIMPLE_PATTERN = re.compile(
        r'<!--\s*AI-GENERATE:\s*(.+?)\s*-->',
        re.IGNORECASE | re.DOTALL,
    )
    
    BLOCK_START_PATTERN = re.compile(
        r'<!--\s*AI-GENERATE-START:\s*(.+?)\s*-->',
        re.IGNORECASE | re.DOTALL,
    )
    
    BLOCK_END_PATTERN = re.compile(
        r'<!--\s*AI-GENERATE-END\s*-->',
        re.IGNORECASE,
    )

    def __init__(
        self,
        provider: AIProvider,
        cache_manager: Optional[CacheManager] = None,
    ):
        """Initialize processor.
        
        Args:
            provider: AI provider instance
            cache_manager: Optional cache manager
        """
        self.generator = PromptGenerator(provider, cache_manager)

    async def process_markdown(
        self,
        markdown: str,
        page_context: Optional[dict] = None,
    ) -> str:
        """Process markdown content and replace AI-GENERATE comments.
        
        Args:
            markdown: Original markdown content
            page_context: Optional page context (title, path, etc.)
            
        Returns:
            Processed markdown with AI-generated content
        """
        # Process simple comments first
        markdown = await self._process_simple_comments(markdown, page_context)
        
        # Process block comments
        markdown = await self._process_block_comments(markdown, page_context)
        
        return markdown

    async def _process_simple_comments(
        self,
        markdown: str,
        page_context: Optional[dict] = None,
    ) -> str:
        """Process simple AI-GENERATE comments.
        
        Format: <!-- AI-GENERATE: prompt -->
        """
        matches = list(self.SIMPLE_PATTERN.finditer(markdown))
        
        if not matches:
            return markdown
        
        log.info(f"Found {len(matches)} AI-GENERATE comment(s)")
        
        # Process in reverse to maintain string positions
        for match in reversed(matches):
            prompt_text = match.group(1).strip()
            
            # Parse prompt and options
            prompt, options = self._parse_prompt_options(prompt_text)
            
            # Add page context to prompt if available
            if page_context:
                prompt = self._add_page_context(prompt, page_context)
            
            try:
                # Generate content
                log.debug(f"Generating content for: {prompt[:50]}...")
                content = await self.generator.generate_from_prompt(prompt)
                
                # Replace comment with generated content
                markdown = (
                    markdown[:match.start()] +
                    content +
                    markdown[match.end():]
                )
                
                log.info(f"Generated {len(content)} characters")
                
            except ProviderError as e:
                log.error(f"Generation failed: {e}")
                # Leave comment in place with error note
                error_msg = f"\n\n> **AI Generation Error**: {e}\n\n"
                markdown = (
                    markdown[:match.end()] +
                    error_msg +
                    markdown[match.end():]
                )
        
        return markdown

    async def _process_block_comments(
        self,
        markdown: str,
        page_context: Optional[dict] = None,
    ) -> str:
        """Process block AI-GENERATE comments.
        
        Format:
        <!-- AI-GENERATE-START: prompt -->
        Optional existing content (will be replaced)
        <!-- AI-GENERATE-END -->
        """
        # Find all block pairs
        start_matches = list(self.BLOCK_START_PATTERN.finditer(markdown))
        end_matches = list(self.BLOCK_END_PATTERN.finditer(markdown))
        
        if not start_matches:
            return markdown
        
        if len(start_matches) != len(end_matches):
            log.warning(
                f"Mismatched AI-GENERATE-START/END blocks: "
                f"{len(start_matches)} starts, {len(end_matches)} ends"
            )
            return markdown
        
        log.info(f"Found {len(start_matches)} AI-GENERATE block(s)")
        
        # Process in reverse to maintain string positions
        for start_match, end_match in reversed(list(zip(start_matches, end_matches))):
            if start_match.end() > end_match.start():
                log.warning("Invalid block: END before START")
                continue
            
            prompt_text = start_match.group(1).strip()
            prompt, options = self._parse_prompt_options(prompt_text)
            
            # Add page context
            if page_context:
                prompt = self._add_page_context(prompt, page_context)
            
            try:
                # Generate content
                log.debug(f"Generating block content for: {prompt[:50]}...")
                content = await self.generator.generate_from_prompt(prompt)
                
                # Replace entire block (including comments) with generated content
                markdown = (
                    markdown[:start_match.start()] +
                    f"<!-- AI-GENERATE-START: {prompt_text} -->\n\n" +
                    content +
                    f"\n\n<!-- AI-GENERATE-END -->" +
                    markdown[end_match.end():]
                )
                
                log.info(f"Generated block: {len(content)} characters")
                
            except ProviderError as e:
                log.error(f"Block generation failed: {e}")
                # Leave block in place with error
                error_msg = f"\n\n> **AI Generation Error**: {e}\n\n"
                markdown = (
                    markdown[:end_match.start()] +
                    error_msg +
                    markdown[end_match.start():]
                )
        
        return markdown

    def _parse_prompt_options(self, prompt_text: str) -> tuple[str, dict]:
        """Parse prompt and options from comment text.
        
        Format: "prompt | option1=value1 option2=value2"
        
        Args:
            prompt_text: Raw prompt text from comment
            
        Returns:
            Tuple of (prompt, options_dict)
        """
        if "|" not in prompt_text:
            return prompt_text, {}
        
        parts = prompt_text.split("|", 1)
        prompt = parts[0].strip()
        options_str = parts[1].strip()
        
        # Parse options
        options = {}
        for option in options_str.split():
            if "=" in option:
                key, value = option.split("=", 1)
                options[key.strip()] = value.strip()
        
        return prompt, options

    def _add_page_context(self, prompt: str, page_context: dict) -> str:
        """Add page context to prompt.
        
        Args:
            prompt: Original prompt
            page_context: Page metadata
            
        Returns:
            Enhanced prompt with context
        """
        context_parts = []
        
        if "title" in page_context:
            context_parts.append(f"Page title: {page_context['title']}")
        
        if "path" in page_context:
            context_parts.append(f"Page path: {page_context['path']}")
        
        if context_parts:
            context_str = " | ".join(context_parts)
            return f"{prompt}\n\nContext: {context_str}"
        
        return prompt

    def has_ai_comments(self, markdown: str) -> bool:
        """Check if markdown contains AI-GENERATE comments.
        
        Args:
            markdown: Markdown content
            
        Returns:
            True if AI comments found
        """
        return bool(
            self.SIMPLE_PATTERN.search(markdown) or
            self.BLOCK_START_PATTERN.search(markdown)
        )

    def count_ai_comments(self, markdown: str) -> int:
        """Count AI-GENERATE comments in markdown.
        
        Args:
            markdown: Markdown content
            
        Returns:
            Number of AI comments
        """
        simple_count = len(self.SIMPLE_PATTERN.findall(markdown))
        block_count = len(self.BLOCK_START_PATTERN.findall(markdown))
        return simple_count + block_count
