"""
Context Builder for RAG queries.
Module 3.38-3.39: Context Injection & Grounded Prompts.
"""

from typing import List, Dict, Any, Tuple


class ContextBuilder:
    """Formats retrieved document chunks into structured LLM context with citations."""

    @staticmethod
    def build_context(retrieved_items: List[Tuple[str, Dict[str, Any], float]]) -> str:
        """
        Takes retrieved items (content, metadata, score) and formats them into a numbered context block.
        """
        if not retrieved_items:
            return "No relevant customer interactions or tickets found in database."

        context_blocks = []
        for idx, (content, meta, score) in enumerate(retrieved_items, start=1):
            source = meta.get('source_type', 'document').capitalize()
            doc_id = meta.get('doc_id') or meta.get('parent_doc_id', f'item_{idx}')
            cust_id = meta.get('customer_id', 'N/A')
            relevance = f"{score:.2f}" if isinstance(score, (int, float)) else "N/A"

            header = f"--- [Source #{idx} | {source} ID: {doc_id} | Customer: {cust_id} | Relevance: {relevance}] ---"
            context_blocks.append(f"{header}\n{content.strip()}")

        return "\n\n".join(context_blocks)

    @staticmethod
    def construct_rag_prompt(user_query: str, context_str: str, customer_info: str = "") -> Dict[str, str]:
        """Construct system and user messages for grounded LLM answer generation."""
        system_prompt = (
            "You are ChurnGuard AI Assistant, an expert Customer Success & Churn Prevention Analyst. "
            "Your role is to analyze customer risk, tickets, and engagement logs to provide actionable, "
            "grounded insights.\n"
            "Rules:\n"
            "1. Base your answers strictly on the provided Context.\n"
            "2. Always cite the Source # and ID for your claims.\n"
            "3. If the context does not contain enough information, state it clearly."
        )

        user_prompt = f"Customer Profile Info:\n{customer_info}\n\nContext Documents:\n{context_str}\n\nUser Question:\n{user_query}"
        return {
            "system": system_prompt,
            "user": user_prompt
        }
