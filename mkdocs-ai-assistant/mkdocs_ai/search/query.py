"""Search query interface."""

from pathlib import Path
from typing import List, Dict, Any, Optional

from ..providers import AIProvider
from ..cache import CacheManager
from .embeddings import EmbeddingGenerator
from .index import SearchIndex, HybridSearch


class SemanticSearch:
    """Semantic search interface.
    
    Features:
    - Query embedding generation
    - Semantic similarity search
    - Hybrid search (semantic + keyword)
    - Result formatting and ranking
    """
    
    def __init__(
        self,
        index: SearchIndex,
        provider: AIProvider,
        cache_manager: Optional[CacheManager] = None,
    ):
        """Initialize search.
        
        Args:
            index: Search index
            provider: AI provider for embeddings
            cache_manager: Optional cache manager
        """
        self.index = index
        self.provider = provider
        self.cache_manager = cache_manager
        self.embedding_generator = EmbeddingGenerator(
            provider=provider,
            cache_manager=cache_manager,
        )
        self.hybrid_search = HybridSearch(index)
    
    async def search(
        self,
        query: str,
        top_k: int = 10,
        use_hybrid: bool = True,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for relevant content.
        
        Args:
            query: Search query
            top_k: Number of results to return
            use_hybrid: Whether to use hybrid search
            filter_metadata: Optional metadata filters
            
        Returns:
            List of search results with scores
        """
        # Generate query embedding
        query_embedding = await self.embedding_generator.generate_embedding(query)
        
        # Perform search
        if use_hybrid:
            results = self.hybrid_search.search(
                query=query,
                query_embedding=query_embedding,
                top_k=top_k,
            )
        else:
            results = self.index.search(
                query_embedding=query_embedding,
                top_k=top_k,
                filter_metadata=filter_metadata,
            )
        
        # Format results
        formatted_results = self._format_results(results, query)
        
        return formatted_results
    
    def _format_results(
        self,
        results: List[Dict[str, Any]],
        query: str,
    ) -> List[Dict[str, Any]]:
        """Format search results.
        
        Args:
            results: Raw search results
            query: Original query
            
        Returns:
            Formatted results
        """
        formatted = []
        
        for result in results:
            formatted_result = {
                'text': result.get('text', ''),
                'score': result.get('combined_score', result.get('similarity', 0)),
                'metadata': result.get('metadata', {}),
                'highlight': self._highlight_query_terms(
                    result.get('text', ''),
                    query,
                ),
            }
            
            formatted.append(formatted_result)
        
        return formatted
    
    def _highlight_query_terms(self, text: str, query: str, max_length: int = 200) -> str:
        """Highlight query terms in text.
        
        Args:
            text: Text to highlight
            query: Query terms
            max_length: Maximum highlight length
            
        Returns:
            Highlighted text snippet
        """
        query_terms = query.lower().split()
        text_lower = text.lower()
        
        # Find first occurrence of any query term
        first_pos = len(text)
        for term in query_terms:
            pos = text_lower.find(term)
            if pos != -1 and pos < first_pos:
                first_pos = pos
        
        # Extract snippet around first occurrence
        if first_pos < len(text):
            start = max(0, first_pos - 50)
            end = min(len(text), first_pos + max_length)
            snippet = text[start:end]
            
            # Add ellipsis
            if start > 0:
                snippet = "..." + snippet
            if end < len(text):
                snippet = snippet + "..."
            
            return snippet
        
        # No query terms found, return beginning
        return text[:max_length] + ("..." if len(text) > max_length else "")


class SearchBuilder:
    """Build and manage search indices."""
    
    def __init__(
        self,
        provider: AIProvider,
        cache_manager: Optional[CacheManager] = None,
        index_path: Optional[Path] = None,
    ):
        """Initialize builder.
        
        Args:
            provider: AI provider
            cache_manager: Optional cache manager
            index_path: Optional index path
        """
        self.provider = provider
        self.cache_manager = cache_manager
        self.index_path = index_path or Path(".ai-cache/search_index.json")
        self.embedding_generator = EmbeddingGenerator(
            provider=provider,
            cache_manager=cache_manager,
        )
    
    async def build_index_from_files(
        self,
        file_paths: List[Path],
    ) -> SearchIndex:
        """Build search index from markdown files.
        
        Args:
            file_paths: List of markdown file paths
            
        Returns:
            Search index
        """
        from .embeddings import DocumentProcessor
        
        index = SearchIndex(self.index_path)
        processor = DocumentProcessor(self.embedding_generator)
        
        for file_path in file_paths:
            # Read file
            content = file_path.read_text(encoding='utf-8')
            
            # Extract metadata
            metadata = {
                'path': str(file_path),
                'filename': file_path.name,
            }
            
            # Process document
            chunks = await processor.process_document(content, metadata)
            
            # Add to index
            index.add_chunks(chunks)
        
        # Update metadata
        index.metadata['total_documents'] = len(file_paths)
        
        return index
    
    async def update_index(
        self,
        index: SearchIndex,
        new_files: List[Path],
    ) -> SearchIndex:
        """Update existing index with new files.
        
        Args:
            index: Existing index
            new_files: New files to add
            
        Returns:
            Updated index
        """
        from .embeddings import DocumentProcessor
        
        processor = DocumentProcessor(self.embedding_generator)
        
        for file_path in new_files:
            content = file_path.read_text(encoding='utf-8')
            
            metadata = {
                'path': str(file_path),
                'filename': file_path.name,
            }
            
            chunks = await processor.process_document(content, metadata)
            index.add_chunks(chunks)
        
        # Update metadata
        index.metadata['total_documents'] += len(new_files)
        
        return index


async def search_documents(
    query: str,
    index_path: Path,
    provider: AIProvider,
    cache_manager: Optional[CacheManager] = None,
    top_k: int = 10,
) -> List[Dict[str, Any]]:
    """Convenience function to search documents.
    
    Args:
        query: Search query
        index_path: Path to search index
        provider: AI provider
        cache_manager: Optional cache manager
        top_k: Number of results
        
    Returns:
        Search results
    """
    # Load index
    index = SearchIndex(index_path)
    index.load()
    
    # Create search
    search = SemanticSearch(
        index=index,
        provider=provider,
        cache_manager=cache_manager,
    )
    
    # Perform search
    results = await search.search(query, top_k=top_k)
    
    return results
