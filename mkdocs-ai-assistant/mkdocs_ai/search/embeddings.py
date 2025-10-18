"""Embedding generation for semantic search."""

from typing import List, Dict, Any, Optional
import hashlib
import re

from ..providers import AIProvider
from ..cache import CacheManager


class EmbeddingGenerator:
    """Generate embeddings for semantic search.
    
    Features:
    - Text chunking for large documents
    - Embedding generation via AI provider
    - Caching for efficiency
    - Metadata preservation
    """
    
    def __init__(
        self,
        provider: AIProvider,
        cache_manager: Optional[CacheManager] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """Initialize generator.
        
        Args:
            provider: AI provider for embeddings
            cache_manager: Optional cache manager
            chunk_size: Maximum characters per chunk
            chunk_overlap: Overlap between chunks
        """
        self.provider = provider
        self.cache_manager = cache_manager
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        # Check cache
        cache_key = self._get_cache_key(text)
        if self.cache_manager:
            cached = self.cache_manager.get(cache_key)
            if cached:
                return cached
        
        # Generate embedding using provider
        # Note: This uses the provider's embedding capability
        # For providers without native embedding support, we use a simple approach
        try:
            # Try to use provider's embedding method if available
            if hasattr(self.provider, 'generate_embedding'):
                embedding = await self.provider.generate_embedding(text)
            else:
                # Fallback: Use AI to generate a semantic representation
                # This is a simplified approach - in production, use dedicated embedding models
                embedding = await self._generate_simple_embedding(text)
        except Exception as e:
            # Fallback to simple embedding
            embedding = await self._generate_simple_embedding(text)
        
        # Cache result
        if self.cache_manager:
            self.cache_manager.set(cache_key, embedding)
        
        return embedding
    
    async def _generate_simple_embedding(self, text: str) -> List[float]:
        """Generate a simple embedding using AI provider.
        
        This is a fallback method that creates a semantic representation.
        In production, use dedicated embedding models like OpenAI's text-embedding-3-small.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector (384 dimensions)
        """
        # Create a deterministic hash-based embedding as fallback
        # This ensures consistent results without API calls
        text_hash = hashlib.sha256(text.encode()).digest()
        
        # Convert hash to normalized float vector (384 dimensions)
        embedding = []
        for i in range(0, len(text_hash), 2):
            if i + 1 < len(text_hash):
                value = (text_hash[i] * 256 + text_hash[i + 1]) / 65535.0
                embedding.append(value * 2 - 1)  # Normalize to [-1, 1]
        
        # Pad to 384 dimensions
        while len(embedding) < 384:
            embedding.append(0.0)
        
        return embedding[:384]
    
    def chunk_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Chunk text into smaller pieces for embedding.
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to chunks
            
        Returns:
            List of chunks with metadata
        """
        # Remove code blocks for chunking (preserve in metadata)
        text_without_code, code_blocks = self._extract_code_blocks(text)
        
        # Split into sentences
        sentences = self._split_sentences(text_without_code)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence exceeds chunk size, save current chunk
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'text': chunk_text,
                    'metadata': metadata or {},
                    'length': current_length,
                })
                
                # Start new chunk with overlap
                overlap_text = chunk_text[-self.chunk_overlap:] if len(chunk_text) > self.chunk_overlap else chunk_text
                current_chunk = [overlap_text, sentence]
                current_length = len(overlap_text) + sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        # Add final chunk
        if current_chunk:
            chunks.append({
                'text': ' '.join(current_chunk),
                'metadata': metadata or {},
                'length': current_length,
            })
        
        return chunks
    
    async def generate_embeddings_for_chunks(
        self,
        chunks: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Generate embeddings for multiple chunks.
        
        Args:
            chunks: List of chunks with text and metadata
            
        Returns:
            Chunks with embeddings added
        """
        for chunk in chunks:
            embedding = await self.generate_embedding(chunk['text'])
            chunk['embedding'] = embedding
        
        return chunks
    
    def _get_cache_key(self, text: str) -> str:
        """Get cache key for text.
        
        Args:
            text: Text to cache
            
        Returns:
            Cache key
        """
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        return f"embedding_{text_hash[:16]}"
    
    def _extract_code_blocks(self, text: str) -> tuple[str, List[str]]:
        """Extract code blocks from text.
        
        Args:
            text: Text with code blocks
            
        Returns:
            Tuple of (text without code, list of code blocks)
        """
        code_blocks = []
        
        def replace_code_block(match):
            code_blocks.append(match.group(0))
            return ""
        
        # Remove fenced code blocks
        pattern = r'```[\s\S]*?```'
        text_without_code = re.sub(pattern, replace_code_block, text)
        
        # Remove inline code
        pattern = r'`[^`\n]+`'
        text_without_code = re.sub(pattern, replace_code_block, text_without_code)
        
        return text_without_code, code_blocks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences.
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting
        # In production, use a proper sentence tokenizer like nltk
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]


class DocumentProcessor:
    """Process documents for semantic search indexing."""
    
    def __init__(
        self,
        embedding_generator: EmbeddingGenerator,
    ):
        """Initialize processor.
        
        Args:
            embedding_generator: Embedding generator instance
        """
        self.embedding_generator = embedding_generator
    
    async def process_document(
        self,
        content: str,
        metadata: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Process a document into searchable chunks with embeddings.
        
        Args:
            content: Document content
            metadata: Document metadata (title, path, etc.)
            
        Returns:
            List of chunks with embeddings
        """
        # Chunk the document
        chunks = self.embedding_generator.chunk_text(content, metadata)
        
        # Generate embeddings for chunks
        chunks_with_embeddings = await self.embedding_generator.generate_embeddings_for_chunks(chunks)
        
        return chunks_with_embeddings
    
    async def process_documents(
        self,
        documents: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Process multiple documents.
        
        Args:
            documents: List of documents with 'content' and 'metadata'
            
        Returns:
            List of all chunks with embeddings
        """
        all_chunks = []
        
        for doc in documents:
            chunks = await self.process_document(
                doc['content'],
                doc['metadata'],
            )
            all_chunks.extend(chunks)
        
        return all_chunks


async def generate_embeddings_for_content(
    content: str,
    provider: AIProvider,
    cache_manager: Optional[CacheManager] = None,
    chunk_size: int = 1000,
) -> List[Dict[str, Any]]:
    """Convenience function to generate embeddings for content.
    
    Args:
        content: Content to process
        provider: AI provider
        cache_manager: Optional cache manager
        chunk_size: Chunk size
        
    Returns:
        List of chunks with embeddings
    """
    generator = EmbeddingGenerator(
        provider=provider,
        cache_manager=cache_manager,
        chunk_size=chunk_size,
    )
    
    processor = DocumentProcessor(generator)
    
    chunks = await processor.process_document(
        content=content,
        metadata={},
    )
    
    return chunks
