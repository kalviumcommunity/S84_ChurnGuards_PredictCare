"""
Unit tests for Vector Store and Embedding Engine.
"""

import unittest
import numpy as np
from rag.vector_store import VectorStore
from rag.embeddings import EmbeddingEngine


class TestVectorStore(unittest.TestCase):

    def setUp(self):
        self.store = VectorStore(dimension=32)

    def test_embedding_generation(self):
        engine = EmbeddingEngine(dimension=32)
        vec = engine.get_embedding("Critical ticket regarding database latency")
        self.assertEqual(len(vec), 32)
        self.assertAlmostEqual(float(np.linalg.norm(vec)), 1.0, places=4)

    def test_add_and_search(self):
        texts = [
            "Customer wants to cancel subscription due to pricing issues",
            "Customer upgraded to enterprise annual plan",
            "Urgent API timeout failure in customer production"
        ]
        metadatas = [
            {"customer_id": "CUST-1", "type": "churn_risk"},
            {"customer_id": "CUST-2", "type": "expansion"},
            {"customer_id": "CUST-3", "type": "technical"}
        ]
        self.store.add_texts(texts, metadatas)
        self.assertEqual(self.store.count(), 3)

        results = self.store.similarity_search_with_score("pricing and cancellation", k=1)
        self.assertEqual(len(results), 1)
        self.assertIn("cancel subscription", results[0][0])
        self.assertEqual(results[0][1]["customer_id"], "CUST-1")

    def test_metadata_filtering(self):
        texts = ["Ticket A", "Ticket B"]
        metas = [{"customer_id": "CUST-A"}, {"customer_id": "CUST-B"}]
        self.store.add_texts(texts, metas)

        results = self.store.similarity_search_with_score("Ticket", k=5, filter_dict={"customer_id": "CUST-B"})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1]["customer_id"], "CUST-B")


if __name__ == '__main__':
    import numpy as np
    unittest.main()
