"""
Unit tests for Document Chunking and Metadata Manager.
"""

import unittest
from rag.chunking import DocumentChunker, TextChunk
from rag.metadata_manager import MetadataManager


class TestDocumentChunking(unittest.TestCase):

    def setUp(self):
        self.chunker = DocumentChunker(chunk_size=10, chunk_overlap=2)

    def test_chunk_by_words(self):
        text = "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12"
        chunks = self.chunker.chunk_by_words(text, doc_id="TKT-101", metadata={"priority": "High"})
        self.assertGreater(len(chunks), 1)
        self.assertIsInstance(chunks[0], TextChunk)
        self.assertEqual(chunks[0].metadata["parent_doc_id"], "TKT-101")
        self.assertGreater(chunks[0].token_count, 0)

    def test_chunk_by_sentences(self):
        text = "This is sentence one. This is sentence two! This is sentence three?"
        chunks = self.chunker.chunk_by_sentences(text, doc_id="DOC-1")
        self.assertTrue(len(chunks) >= 1)
        self.assertIn("sentence one", chunks[0].content)

    def test_metadata_enrichment_and_citation(self):
        meta = MetadataManager.enrich_chunk_metadata(
            chunk_metadata={"chunk_index": 1},
            customer_id="CUST-1001",
            source_type="ticket",
            sentiment="Negative"
        )
        self.assertEqual(meta["customer_id"], "CUST-1001")
        self.assertEqual(meta["sentiment"], "Negative")

        citation = MetadataManager.format_citation({"source_type": "ticket", "doc_id": "TKT-99", "customer_id": "CUST-1001"})
        self.assertEqual(citation, "[Ticket: TKT-99 [Customer: CUST-1001]]")


if __name__ == '__main__':
    unittest.main()
