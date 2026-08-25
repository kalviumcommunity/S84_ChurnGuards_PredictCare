"""
Metadata Manager for RAG Chunking.
Module 3.22: Chunk Metadata.
"""

from typing import Dict, Any, List


class MetadataManager:
    """Standardizes, enriches, and validates metadata associated with text chunks."""

    @staticmethod
    def enrich_chunk_metadata(
        chunk_metadata: Dict[str, Any],
        customer_id: str,
        source_type: str,
        sentiment: str = "Neutral",
        urgency: str = "Normal",
        tags: List[str] = None
    ) -> Dict[str, Any]:
        enriched = dict(chunk_metadata or {})
        enriched.update({
            'customer_id': str(customer_id),
            'source_type': source_type,
            'sentiment': sentiment,
            'urgency': urgency,
            'tags': tags or []
        })
        return enriched

    @staticmethod
    def format_citation(metadata: Dict[str, Any]) -> str:
        """Generate human-readable source citation string for RAG answers."""
        source_type = metadata.get('source_type', 'Document').capitalize()
        doc_id = metadata.get('parent_doc_id') or metadata.get('doc_id', 'Unknown ID')
        customer_id = metadata.get('customer_id', '')
        cust_str = f" [Customer: {customer_id}]" if customer_id else ""
        return f"[{source_type}: {doc_id}{cust_str}]"
