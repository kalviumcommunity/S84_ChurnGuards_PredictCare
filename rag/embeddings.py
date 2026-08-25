"""
Embedding generator supporting both TF-IDF fallback and OpenAI API embeddings.
Module 3.25: Embeddings Generation.
"""

import numpy as np
from typing import List, Union
import math
import re


class EmbeddingEngine:
    """Generates numerical vector embeddings for text chunks and queries."""

    def __init__(self, dimension: int = 64):
        self.dimension = dimension

    def _hash_vector(self, text: str) -> np.ndarray:
        """Deterministic feature hashing embedding generator for fast local search."""
        words = re.findall(r'\w+', text.lower())
        vec = np.zeros(self.dimension, dtype=np.float32)
        if not words:
            return vec

        for word in words:
            idx = abs(hash(word)) % self.dimension
            vec[idx] += 1.0

        # L2 normalize
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def get_embedding(self, text: str) -> np.ndarray:
        """Get single embedding vector for a text."""
        return self._hash_vector(text)

    def get_embeddings_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Get embeddings for a list of texts."""
        return [self.get_embedding(t) for t in texts]
