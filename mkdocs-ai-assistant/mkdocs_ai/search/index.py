"""Vector index for semantic search."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import math


class SearchIndex:
    """Vector index for semantic search.
    
    Features:
    - JSON-based storage (portable)
    - Cosine similarity search
    - Metadata filtering
    - Incremental updates
    """
    
    def __init__(self, index_path: Optional[Path] = None):
        """Initialize index.
        
        Args:
            index_path: Path to index file (JSON)
        """
        self.index_path = index_path or Path(".ai-cache/search_index.json")
        self.chunks: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {
            "version": "1.0",
            "total_chunks": 0,
            "total_documents": 0,
        }
    
    def add_chunk(self, chunk: Dict[str, Any]):
        """Add a chunk to the index.
        
        Args:
            chunk: Chunk with text, embedding, and metadata
        """
        # Add unique ID if not present
        if 'id' not in chunk:
            chunk['id'] = len(self.chunks)
        
        self.chunks.append(chunk)
        self.metadata['total_chunks'] = len(self.chunks)
    
    def add_chunks(self, chunks: List[Dict[str, Any]]):
        """Add multiple chunks to the index.
        
        Args:
            chunks: List of chunks
        """
        for chunk in chunks:
            self.add_chunk(chunk)
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar chunks.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of chunks with similarity scores
        """
        # Filter chunks by metadata if specified
        filtered_chunks = self.chunks
        if filter_metadata:
            filtered_chunks = [
                chunk for chunk in self.chunks
                if self._matches_filter(chunk.get('metadata', {}), filter_metadata)
            ]
        
        # Calculate similarity scores
        results = []
        for chunk in filtered_chunks:
            if 'embedding' not in chunk:
                continue
            
            similarity = self._cosine_similarity(
                query_embedding,
                chunk['embedding'],
            )
            
            results.append({
                **chunk,
                'similarity': similarity,
            })
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Return top k results
        return results[:top_k]
    
    def save(self):
        """Save index to disk."""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'metadata': self.metadata,
            'chunks': self.chunks,
        }
        
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """Load index from disk."""
        if not self.index_path.exists():
            return
        
        with open(self.index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.metadata = data.get('metadata', self.metadata)
        self.chunks = data.get('chunks', [])
    
    def clear(self):
        """Clear the index."""
        self.chunks = []
        self.metadata['total_chunks'] = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            'total_chunks': len(self.chunks),
            'total_documents': self.metadata.get('total_documents', 0),
            'index_size_mb': self._get_index_size_mb(),
            'avg_chunk_length': self._get_avg_chunk_length(),
        }
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score (0-1)
        """
        if len(vec1) != len(vec2):
            return 0.0
        
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        # Calculate cosine similarity
        similarity = dot_product / (magnitude1 * magnitude2)
        
        # Normalize to 0-1 range
        return (similarity + 1) / 2
    
    def _matches_filter(self, metadata: Dict[str, Any], filter_dict: Dict[str, Any]) -> bool:
        """Check if metadata matches filter.
        
        Args:
            metadata: Chunk metadata
            filter_dict: Filter criteria
            
        Returns:
            True if matches
        """
        for key, value in filter_dict.items():
            if key not in metadata or metadata[key] != value:
                return False
        return True
    
    def _get_index_size_mb(self) -> float:
        """Get index size in MB.
        
        Returns:
            Size in MB
        """
        if not self.index_path.exists():
            return 0.0
        
        size_bytes = self.index_path.stat().st_size
        return size_bytes / (1024 * 1024)
    
    def _get_avg_chunk_length(self) -> float:
        """Get average chunk length.
        
        Returns:
            Average length
        """
        if not self.chunks:
            return 0.0
        
        total_length = sum(chunk.get('length', 0) for chunk in self.chunks)
        return total_length / len(self.chunks)


class HybridSearch:
    """Hybrid search combining semantic and keyword search."""
    
    def __init__(self, index: SearchIndex):
        """Initialize hybrid search.
        
        Args:
            index: Search index
        """
        self.index = index
    
    def search(
        self,
        query: str,
        query_embedding: List[float],
        top_k: int = 10,
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> List[Dict[str, Any]]:
        """Perform hybrid search.
        
        Args:
            query: Query text
            query_embedding: Query embedding
            top_k: Number of results
            semantic_weight: Weight for semantic similarity
            keyword_weight: Weight for keyword matching
            
        Returns:
            List of results with combined scores
        """
        # Get semantic search results
        semantic_results = self.index.search(query_embedding, top_k=top_k * 2)
        
        # Calculate keyword scores
        query_terms = set(query.lower().split())
        
        for result in semantic_results:
            text = result.get('text', '').lower()
            text_terms = set(text.split())
            
            # Calculate keyword overlap
            overlap = len(query_terms & text_terms)
            keyword_score = overlap / len(query_terms) if query_terms else 0
            
            # Combine scores
            semantic_score = result.get('similarity', 0)
            combined_score = (
                semantic_weight * semantic_score +
                keyword_weight * keyword_score
            )
            
            result['keyword_score'] = keyword_score
            result['combined_score'] = combined_score
        
        # Sort by combined score
        semantic_results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return semantic_results[:top_k]


def create_index_from_documents(
    documents: List[Dict[str, Any]],
    index_path: Optional[Path] = None,
) -> SearchIndex:
    """Create a search index from documents.
    
    Args:
        documents: List of documents with embeddings
        index_path: Optional path to save index
        
    Returns:
        Search index
    """
    index = SearchIndex(index_path)
    
    for doc in documents:
        # Add document chunks to index
        if 'chunks' in doc:
            index.add_chunks(doc['chunks'])
        elif 'embedding' in doc:
            # Single document without chunks
            index.add_chunk(doc)
    
    # Update document count
    index.metadata['total_documents'] = len(documents)
    
    return index
