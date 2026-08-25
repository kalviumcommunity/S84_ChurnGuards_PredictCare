"""
Unit tests for RAG Context Builder and Pipeline.
"""

import unittest
from rag.context_builder import ContextBuilder
from rag.pipeline import RAGPipeline


class TestRAGPipeline(unittest.TestCase):

    def test_build_context_and_prompts(self):
        items = [
            (
                "Customer escalated ticket #1234 regarding missing report data.",
                {"doc_id": "TKT-1234", "source_type": "ticket", "customer_id": "CUST-1"},
                0.89
            )
        ]
        context = ContextBuilder.build_context(items)
        self.assertIn("TKT-1234", context)
        self.assertIn("Relevance: 0.89", context)

        prompts = ContextBuilder.construct_rag_prompt(
            user_query="Why is customer CUST-1 unhappy?",
            context_str=context,
            customer_info="Company: Acme Corp | ARR: $120,000"
        )
        self.assertIn("ChurnGuard AI Assistant", prompts["system"])
        self.assertIn("Why is customer CUST-1 unhappy?", prompts["user"])

    def test_pipeline_execution(self):
        pipeline = RAGPipeline()
        items = [
            ("Call log: Discussed contract renewal delay.", {"doc_id": "INT-99", "source_type": "interaction", "customer_id": "CUST-5"}, 0.92)
        ]
        result = pipeline.process_query(
            query="What happened in the renewal call?",
            retrieved_items=items,
            customer_info="Company: Beta Inc"
        )
        self.assertEqual(result["num_sources"], 1)
        self.assertEqual(result["citations"][0]["doc_id"], "INT-99")
        self.assertIn("Beta Inc", result["user_prompt"])


if __name__ == '__main__':
    unittest.main()
