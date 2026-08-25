"""
Chunking strategies for ChurnGuard RAG Pipeline.
Module 3.21: Document Chunking.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
import re


@dataclass
class TextChunk:
    chunk_id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    token_count: int = 0


class DocumentChunker:
    """Chunks documents into retrievable units with sliding window or semantic boundaries."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def approximate_token_count(self, text: str) -> int:
        """Estimate token count (approx 1 word = 1.3 tokens)."""
        words = len(text.split())
        return max(1, int(words * 1.3))

    def chunk_by_words(self, text: str, doc_id: str = "DOC", metadata: Dict[str, Any] = None) -> List[TextChunk]:
        """Split text by word boundaries with overlap."""
        words = text.split()
        if not words:
            return []

        chunks = []
        step = max(1, self.chunk_size - self.chunk_overlap)
        
        for i in range(0, len(words), step):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            chunk_idx = len(chunks) + 1
            chunk_meta = dict(metadata or {})
            chunk_meta['chunk_index'] = chunk_idx
            chunk_meta['parent_doc_id'] = doc_id
            
            chunk = TextChunk(
                chunk_id=f"{doc_id}_chk_{chunk_idx}",
                content=chunk_text,
                metadata=chunk_meta,
                token_count=self.approximate_token_count(chunk_text)
            )
            chunks.append(chunk)

            if i + self.chunk_size >= len(words):
                break

        return chunks

    def chunk_by_sentences(self, text: str, doc_id: str = "DOC", metadata: Dict[str, Any] = None) -> List[TextChunk]:
        """Split text by sentences while respecting maximum token limit."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_sentences = []
        current_len = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            words_in_sent = len(sentence.split())
            if current_len + words_in_sent > self.chunk_size and current_sentences:
                chunk_text = " ".join(current_sentences)
                chunk_idx = len(chunks) + 1
                meta = dict(metadata or {})
                meta['chunk_index'] = chunk_idx
                meta['parent_doc_id'] = doc_id
                chunks.append(TextChunk(
                    chunk_id=f"{doc_id}_chk_{chunk_idx}",
                    content=chunk_text,
                    metadata=meta,
                    token_count=self.approximate_token_count(chunk_text)
                ))
                current_sentences = [sentence]
                current_len = words_in_sent
            else:
                current_sentences.append(sentence)
                current_len += words_in_sent

        if current_sentences:
            chunk_text = " ".join(current_sentences)
            chunk_idx = len(chunks) + 1
            meta = dict(metadata or {})
            meta['chunk_index'] = chunk_idx
            meta['parent_doc_id'] = doc_id
            chunks.append(TextChunk(
                chunk_id=f"{doc_id}_chk_{chunk_idx}",
                content=chunk_text,
                metadata=meta,
                token_count=self.approximate_token_count(chunk_text)
            ))

        return chunks
