"""Grammar and spelling enhancement."""

from typing import List, Dict, Any, Optional
import re

from ..providers import AIProvider
from ..cache import CacheManager


class GrammarEnhancer:
    """Enhance grammar and spelling in documentation.
    
    Features:
    - Grammar error detection and correction
    - Spelling mistake correction
    - Punctuation fixes
    - Sentence structure improvements
    """
    
    def __init__(
        self,
        provider: AIProvider,
        cache_manager: Optional[CacheManager] = None,
    ):
        """Initialize enhancer.
        
        Args:
            provider: AI provider for corrections
            cache_manager: Optional cache manager
        """
        self.provider = provider
        self.cache_manager = cache_manager
    
    async def fix_grammar(self, text: str) -> str:
        """Fix grammar errors in text.
        
        Args:
            text: Text to fix
            
        Returns:
            Text with grammar fixes
        """
        prompt = f"""Fix grammar errors in the following text.

Rules:
- Fix subject-verb agreement
- Fix tense consistency
- Fix article usage (a, an, the)
- Fix pronoun usage
- Preserve all markdown formatting
- Don't change technical terms
- Don't add new content

Text:
{text}

Return ONLY the corrected text, no explanations."""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a grammar expert fixing documentation errors.",
            temperature=0.2,
        )
        
        return response.content.strip()
    
    async def fix_spelling(self, text: str) -> str:
        """Fix spelling mistakes in text.
        
        Args:
            text: Text to fix
            
        Returns:
            Text with spelling fixes
        """
        prompt = f"""Fix spelling mistakes in the following text.

Rules:
- Correct misspelled words
- Use American English spelling
- Preserve technical terms and proper nouns
- Preserve all markdown formatting
- Don't change correctly spelled words

Text:
{text}

Return ONLY the corrected text, no explanations."""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a spelling expert correcting documentation.",
            temperature=0.2,
        )
        
        return response.content.strip()
    
    async def fix_punctuation(self, text: str) -> str:
        """Fix punctuation errors in text.
        
        Args:
            text: Text to fix
            
        Returns:
            Text with punctuation fixes
        """
        prompt = f"""Fix punctuation errors in the following text.

Rules:
- Add missing periods, commas, etc.
- Fix comma splices
- Fix run-on sentences
- Ensure proper capitalization
- Preserve all markdown formatting
- Don't change sentence structure

Text:
{text}

Return ONLY the corrected text, no explanations."""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a punctuation expert fixing documentation.",
            temperature=0.2,
        )
        
        return response.content.strip()
    
    async def detect_errors(self, text: str) -> List[Dict[str, Any]]:
        """Detect grammar and spelling errors without fixing them.
        
        Args:
            text: Text to check
            
        Returns:
            List of detected errors with details
        """
        prompt = f"""Detect grammar and spelling errors in the following text.

Text:
{text}

For each error, provide:
- type: "grammar" or "spelling"
- error: the incorrect text
- correction: the correct text
- explanation: brief explanation of the error
- line: approximate line number (if possible)

Return a JSON array of errors. If no errors, return empty array [].
Return ONLY valid JSON, no other text."""
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are a grammar and spelling error detector.",
            temperature=0.2,
        )
        
        # Parse JSON response
        import json
        try:
            errors = json.loads(response.content)
            return errors if isinstance(errors, list) else []
        except json.JSONDecodeError:
            return []
    
    async def fix_all(self, text: str) -> str:
        """Fix all grammar, spelling, and punctuation errors.
        
        Args:
            text: Text to fix
            
        Returns:
            Fully corrected text
        """
        prompt = f"""Fix all grammar, spelling, and punctuation errors in the following text.

Rules:
- Fix grammar errors (subject-verb agreement, tense, articles, pronouns)
- Fix spelling mistakes
- Fix punctuation errors
- Preserve all markdown formatting
- Preserve technical terms and code
- Don't add new content or change meaning
- Don't rewrite sentences unless necessary for grammar

Text:
{text}

Return ONLY the corrected text, no explanations."""
        
        # Check cache
        cache_key = f"grammar_fix_{text[:100]}"
        if self.cache_manager:
            cached = self.cache_manager.get(
                cache_key,
                model=self.provider.model,
            )
            if cached:
                return cached
        
        response = await self.provider.generate(
            prompt=prompt,
            system_prompt="You are an expert editor fixing grammar, spelling, and punctuation.",
            temperature=0.2,
        )
        
        corrected = response.content.strip()
        
        # Cache result
        if self.cache_manager:
            self.cache_manager.set(cache_key, corrected, model=self.provider.model)
        
        return corrected
    
    def get_common_errors(self) -> Dict[str, str]:
        """Get common grammar and spelling errors to watch for.
        
        Returns:
            Dictionary of common errors and their corrections
        """
        return {
            # Common grammar errors
            "it's": "its (possessive)",
            "your": "you're (you are)",
            "their": "there/they're",
            "affect": "effect",
            "then": "than",
            
            # Common spelling errors
            "recieve": "receive",
            "occured": "occurred",
            "seperate": "separate",
            "definately": "definitely",
            "accomodate": "accommodate",
            
            # Technical writing
            "alot": "a lot",
            "cant": "can't",
            "dont": "don't",
            "wont": "won't",
            "shouldnt": "shouldn't",
        }


class SpellingChecker:
    """Check spelling in documentation.
    
    Lightweight spelling checker for quick checks.
    """
    
    def __init__(self):
        """Initialize checker."""
        self.custom_dictionary = set()
    
    def add_word(self, word: str):
        """Add word to custom dictionary.
        
        Args:
            word: Word to add
        """
        self.custom_dictionary.add(word.lower())
    
    def add_words(self, words: List[str]):
        """Add multiple words to custom dictionary.
        
        Args:
            words: Words to add
        """
        for word in words:
            self.add_word(word)
    
    def is_technical_term(self, word: str) -> bool:
        """Check if word is a technical term.
        
        Args:
            word: Word to check
            
        Returns:
            True if word is a technical term
        """
        # Common technical patterns
        technical_patterns = [
            r'^[A-Z][a-z]+[A-Z]',  # CamelCase
            r'^[a-z]+_[a-z]+',      # snake_case
            r'^[A-Z_]+$',           # CONSTANT_CASE
            r'^\w+\.\w+',           # module.function
            r'^@\w+',               # @decorator
            r'^\$\w+',              # $variable
        ]
        
        for pattern in technical_patterns:
            if re.match(pattern, word):
                return True
        
        return word.lower() in self.custom_dictionary
    
    def extract_words(self, text: str) -> List[str]:
        """Extract words from text, excluding code and technical terms.
        
        Args:
            text: Text to extract from
            
        Returns:
            List of words to check
        """
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        
        # Filter technical terms
        return [w for w in words if not self.is_technical_term(w)]


async def fix_grammar_in_file(
    file_path: str,
    provider: AIProvider,
    cache_manager: Optional[CacheManager] = None,
) -> str:
    """Convenience function to fix grammar in a file.
    
    Args:
        file_path: Path to file
        provider: AI provider
        cache_manager: Optional cache manager
        
    Returns:
        Corrected content
    """
    from pathlib import Path
    
    content = Path(file_path).read_text(encoding="utf-8")
    
    enhancer = GrammarEnhancer(provider, cache_manager)
    corrected = await enhancer.fix_all(content)
    
    return corrected
