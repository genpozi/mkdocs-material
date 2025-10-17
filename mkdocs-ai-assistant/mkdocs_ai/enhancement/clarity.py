"""Clarity and readability enhancement."""

from typing import Dict, Any, Optional, List
import re

from ..providers import AIProvider
from ..cache import CacheManager


class ClarityEnhancer:
    """Enhance clarity and readability of documentation.
    
    Features:
    - Simplify complex sentences
    - Improve word choice
    - Enhance structure and flow
    - Check readability metrics
    - Ensure consistency
    """
    
    def __init__(
        self,
        provider: AIProvider,
        cache_manager: Optional[CacheManager] = None,
    ):
        """Initialize enhancer.
        
        Args:
            provider: AI provider for improvements
            cache_manager: Optional cache manager
        """
        self.provider = provider
        self.cache_manager = cache_manager
    
    async def improve_clarity(self, text: str) -> str:
        """Improve clarity of text.
        
        Args:
            text: Text to improve
            
        Returns:
            Improved text
        """
        prompt = f"""Improve the clarity and readability of the following text.

Rules:
- Simplify complex sentences
- Use clearer word choices
- Break up long paragraphs
- Improve transitions between ideas
- Preserve all markdown formatting
- Preserve technical accuracy
- Don't add new information
- Maintain the original meaning

Text:
{text}

Return ONLY the improved text, no explanations."""
        
        # Check cache
        cache_key = f"clarity_{text[:100]}"
        if self.cache_manager:
            cached = self.cache_manager.get(
                cache_key,
                model=self.provider.model,
            )
            if cached:
                return cached
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a technical writing expert improving documentation clarity.",
            temperature=0.4,
        )
        
        improved = response.content.strip()
        
        # Cache result
        if self.cache_manager:
            self.cache_manager.set(cache_key, improved, model=self.provider.model)
        
        return improved
    
    async def simplify_sentences(self, text: str) -> str:
        """Simplify complex sentences.
        
        Args:
            text: Text with complex sentences
            
        Returns:
            Text with simplified sentences
        """
        prompt = f"""Simplify complex sentences in the following text.

Rules:
- Break long sentences into shorter ones
- Use simpler sentence structures
- Avoid nested clauses
- Preserve meaning and technical accuracy
- Preserve all markdown formatting
- Don't change simple sentences

Text:
{text}

Return ONLY the simplified text, no explanations."""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are an expert at simplifying technical writing.",
            temperature=0.3,
        )
        
        return response.content.strip()
    
    async def improve_word_choice(self, text: str) -> str:
        """Improve word choice for better clarity.
        
        Args:
            text: Text to improve
            
        Returns:
            Text with better word choices
        """
        prompt = f"""Improve word choice in the following text for better clarity.

Rules:
- Replace vague words with specific ones
- Use simpler alternatives for complex words
- Avoid jargon where possible (keep technical terms)
- Use active voice instead of passive
- Preserve all markdown formatting
- Preserve technical accuracy

Text:
{text}

Return ONLY the improved text, no explanations."""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a technical writing expert improving word choice.",
            temperature=0.3,
        )
        
        return response.content.strip()
    
    async def check_consistency(self, text: str) -> Dict[str, Any]:
        """Check terminology consistency in text.
        
        Args:
            text: Text to check
            
        Returns:
            Consistency report
        """
        prompt = f"""Analyze terminology consistency in the following text.

Text:
{text}

Identify:
- Terms used inconsistently (e.g., "user" vs "end-user")
- Capitalization inconsistencies
- Hyphenation inconsistencies
- Abbreviation inconsistencies

Return a JSON object with:
- inconsistencies: list of inconsistent terms with examples
- recommendations: list of recommended standard terms
- score: consistency score 0-100

Return ONLY valid JSON, no other text."""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a documentation consistency analyzer.",
            temperature=0.2,
        )
        
        # Parse JSON response
        import json
        try:
            report = json.loads(response.content)
            return report
        except json.JSONDecodeError:
            return {
                "inconsistencies": [],
                "recommendations": [],
                "score": 0,
            }
    
    async def fix_consistency(self, text: str) -> str:
        """Fix terminology consistency issues.
        
        Args:
            text: Text to fix
            
        Returns:
            Text with consistent terminology
        """
        prompt = f"""Fix terminology consistency issues in the following text.

Rules:
- Use consistent terms throughout
- Use consistent capitalization
- Use consistent hyphenation
- Use consistent abbreviations
- Preserve all markdown formatting
- Preserve technical accuracy

Text:
{text}

Return ONLY the corrected text, no explanations."""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a documentation consistency expert.",
            temperature=0.2,
        )
        
        return response.content.strip()
    
    async def calculate_readability(self, text: str) -> Dict[str, Any]:
        """Calculate readability metrics for text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Readability metrics
        """
        # Simple readability calculations
        sentences = self._count_sentences(text)
        words = self._count_words(text)
        syllables = self._count_syllables(text)
        
        # Flesch Reading Ease
        if sentences > 0 and words > 0:
            avg_sentence_length = words / sentences
            avg_syllables_per_word = syllables / words
            flesch_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
        else:
            flesch_score = 0
        
        # Flesch-Kincaid Grade Level
        if sentences > 0 and words > 0:
            grade_level = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
        else:
            grade_level = 0
        
        return {
            "flesch_reading_ease": max(0, min(100, flesch_score)),
            "flesch_kincaid_grade": max(0, grade_level),
            "sentences": sentences,
            "words": words,
            "avg_sentence_length": avg_sentence_length if sentences > 0 else 0,
            "avg_syllables_per_word": avg_syllables_per_word if words > 0 else 0,
            "interpretation": self._interpret_flesch_score(flesch_score),
        }
    
    def _count_sentences(self, text: str) -> int:
        """Count sentences in text.
        
        Args:
            text: Text to count
            
        Returns:
            Number of sentences
        """
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        
        # Count sentence endings
        sentences = re.findall(r'[.!?]+', text)
        return len(sentences)
    
    def _count_words(self, text: str) -> int:
        """Count words in text.
        
        Args:
            text: Text to count
            
        Returns:
            Number of words
        """
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        
        # Count words
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    
    def _count_syllables(self, text: str) -> int:
        """Estimate syllable count in text.
        
        Args:
            text: Text to count
            
        Returns:
            Estimated syllable count
        """
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        
        # Simple syllable estimation
        words = re.findall(r'\b\w+\b', text.lower())
        syllables = 0
        
        for word in words:
            # Count vowel groups
            vowel_groups = len(re.findall(r'[aeiouy]+', word))
            # Adjust for silent e
            if word.endswith('e'):
                vowel_groups -= 1
            # Minimum 1 syllable per word
            syllables += max(1, vowel_groups)
        
        return syllables
    
    def _interpret_flesch_score(self, score: float) -> str:
        """Interpret Flesch Reading Ease score.
        
        Args:
            score: Flesch score
            
        Returns:
            Interpretation string
        """
        if score >= 90:
            return "Very easy to read (5th grade level)"
        elif score >= 80:
            return "Easy to read (6th grade level)"
        elif score >= 70:
            return "Fairly easy to read (7th grade level)"
        elif score >= 60:
            return "Standard (8th-9th grade level)"
        elif score >= 50:
            return "Fairly difficult (10th-12th grade level)"
        elif score >= 30:
            return "Difficult (college level)"
        else:
            return "Very difficult (college graduate level)"
    
    async def get_improvement_suggestions(self, text: str) -> List[str]:
        """Get specific suggestions for improving clarity.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of improvement suggestions
        """
        prompt = f"""Analyze the following text and provide specific suggestions for improving clarity.

Text:
{text}

Provide 3-5 specific, actionable suggestions. Focus on:
- Sentence structure
- Word choice
- Organization
- Transitions
- Readability

Return a JSON array of suggestion strings.
Return ONLY valid JSON, no other text."""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a technical writing coach providing improvement suggestions.",
            temperature=0.4,
        )
        
        # Parse JSON response
        import json
        try:
            suggestions = json.loads(response.content)
            return suggestions if isinstance(suggestions, list) else []
        except json.JSONDecodeError:
            return []


async def improve_clarity_in_file(
    file_path: str,
    provider: AIProvider,
    cache_manager: Optional[CacheManager] = None,
) -> str:
    """Convenience function to improve clarity in a file.
    
    Args:
        file_path: Path to file
        provider: AI provider
        cache_manager: Optional cache manager
        
    Returns:
        Improved content
    """
    from pathlib import Path
    
    content = Path(file_path).read_text(encoding="utf-8")
    
    enhancer = ClarityEnhancer(provider, cache_manager)
    improved = await enhancer.improve_clarity(content)
    
    return improved
