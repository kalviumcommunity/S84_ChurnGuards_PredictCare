"""
In-memory & persistent Vector Store with Cosine Similarity Search.
Module 3.30-3.33: Vector Storage & Similarity Search.
"""

from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from .embeddings import EmbeddingEngine


class VectorStore:
    """Lightweight vector index with cosine similarity search and metadata filtering."""

    def __init__(self, dimension: int = 64):
        self.embedding_engine = EmbeddingEngine(dimension=dimension)
        self.vectors: List[np.ndarray] = []
        self.documents: List[str] = []
        self.metadatas: List[Dict[str, Any]] = []
        self.ids: List[str] = []

    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None, ids: Optional[List[str]] = None):
        """Embed and add texts with associated metadata to the vector store."""
        if not texts:
            return

        for i, text in enumerate(texts):
            doc_id = ids[i] if ids and i < len(ids) else f"doc_{len(self.ids) + 1}"
            meta = metadatas[i] if metadatas and i < len(metadatas) else {}
            vec = self.embedding_engine.get_embedding(text)

            self.vectors.append(vec)
            self.documents.append(text)
            self.metadatas.append(meta)
            self.ids.append(doc_id)

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[str, Dict[str, Any], float]]:
        """
        Search for top-k most similar documents to the query vector.
        Returns list of (document_text, metadata, cosine_similarity_score).
        """
        if not self.vectors:
            return []

        query_vec = self.embedding_engine.get_embedding(query)
        results = []

        for idx, vec in enumerate(self.vectors):
            meta = self.metadatas[idx]

            # Apply metadata filters if provided
            if filter_dict:
                match = True
                for key, val in filter_dict.items():
                    if meta.get(key) != val:
                        match = False
                        break
                if not match:
                    continue

            # Cosine similarity (vectors are already normalized)
            score = float(np.dot(query_vec, vec))
            results.append((self.documents[idx], meta, score))

        # Sort by score descending
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:k]

    def count(self) -> int:
        return len(self.documents)

    def clear(self):
        self.vectors = []
        self.documents = []
        self.metadatas = []
        self.ids = []
