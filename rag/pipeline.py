"""
End-to-End RAG Pipeline for ChurnGuard AI.
Module 3.37: RAG Pipeline Orchestrator.
"""

from typing import List, Dict, Any, Optional
from .context_builder import ContextBuilder


class RAGPipeline:
    """Orchestrates query processing, context retrieval, and grounded response generation."""

    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.context_builder = ContextBuilder()

    def process_query(
        self,
        query: str,
        retrieved_items: List[Any],
        customer_info: str = ""
    ) -> Dict[str, Any]:
        """Execute full RAG generation pipeline and package citations."""
        context_str = self.context_builder.build_context(retrieved_items)
        prompt_bundle = self.context_builder.construct_rag_prompt(
            user_query=query,
            context_str=context_str,
            customer_info=customer_info
        )

        # Extract citations metadata
        citations = []
        for item in retrieved_items:
            if isinstance(item, (tuple, list)) and len(item) >= 2:
                meta = item[1]
                citations.append({
                    "doc_id": meta.get("doc_id") or meta.get("parent_doc_id", "Doc"),
                    "source_type": meta.get("source_type", "document"),
                    "customer_id": meta.get("customer_id", "N/A"),
                    "relevance": item[2] if len(item) > 2 else None
                })

        return {
            "query": query,
            "context": context_str,
            "system_prompt": prompt_bundle["system"],
            "user_prompt": prompt_bundle["user"],
            "citations": citations,
            "num_sources": len(citations)
        }
