"""
Unit tests for RAG DocumentLoader.
"""

import unittest
import tempfile
import json
import os
import pandas as pd
from rag.document_loader import DocumentLoader, Document


class TestDocumentLoader(unittest.TestCase):

    def test_load_from_text(self):
        loader = DocumentLoader()
        doc = loader.load_from_text("Customer reported slow database query response.", {"customer_id": "CUST-101"})
        self.assertIsInstance(doc, Document)
        self.assertIn("slow database query", doc.page_content)
        self.assertEqual(doc.metadata["customer_id"], "CUST-101")

    def test_load_tickets_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sample_tickets = [
                {
                    "ticket_id": "TKT-100",
                    "customer_id": "CUST-100",
                    "subject": "Export error",
                    "priority": "Critical",
                    "status": "Open",
                    "sentiment": "Negative",
                    "created_date": "2026-08-20T10:00:00"
                }
            ]
            path = os.path.join(tmpdir, "tickets.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(sample_tickets, f)

            loader = DocumentLoader(base_dir=tmpdir)
            docs = loader.load_tickets_json(path)
            self.assertEqual(len(docs), 1)
            self.assertEqual(docs[0].doc_id, "TKT-100")
            self.assertEqual(docs[0].metadata["priority"], "Critical")
            self.assertIn("Export error", docs[0].page_content)

    def test_load_interactions_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            df = pd.DataFrame([
                {
                    "interaction_id": "INT-501",
                    "customer_id": "CUST-100",
                    "interaction_type": "Support Call",
                    "description": "Reviewed Q3 renewal options with VP",
                    "timestamp": "2026-08-21 15:00:00"
                }
            ])
            path = os.path.join(tmpdir, "interactions.csv")
            df.to_csv(path, index=False)

            loader = DocumentLoader(base_dir=tmpdir)
            docs = loader.load_interactions_csv(path)
            self.assertEqual(len(docs), 1)
            self.assertEqual(docs[0].doc_id, "INT-501")
            self.assertIn("Support Call", docs[0].page_content)


if __name__ == '__main__':
    unittest.main()
