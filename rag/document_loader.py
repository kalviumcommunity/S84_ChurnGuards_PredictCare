"""
Document Loader for ChurnGuard AI RAG Pipeline.
Module 3.19: Document Loading & Normalization.
Supports JSON tickets, CSV interactions, TXT notes, and Markdown summaries.
"""

import os
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pandas as pd


@dataclass
class Document:
    """Represents a unified document unit for retrieval and citation."""
    page_content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    doc_id: Optional[str] = None

    def __post_init__(self):
        if not self.doc_id and 'doc_id' in self.metadata:
            self.doc_id = str(self.metadata['doc_id'])


class DocumentLoader:
    """Multi-format customer document loader for support logs, notes, and emails."""

    def __init__(self, base_dir: str = 'data'):
        self.base_dir = base_dir

    def load_from_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> Document:
        """Create a single Document object from raw text."""
        return Document(page_content=text.strip(), metadata=metadata or {})

    def load_tickets_json(self, file_path: Optional[str] = None) -> List[Document]:
        """Load support tickets from a JSON file into structured Document objects."""
        path = file_path or os.path.join(self.base_dir, 'tickets.json')
        if not os.path.exists(path):
            return []

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        docs = []
        for item in data:
            doc_id = item.get('ticket_id', f"TKT-{len(docs)+1}")
            customer_id = item.get('customer_id', 'UNKNOWN')
            subject = item.get('subject', 'No Subject')
            priority = item.get('priority', 'Normal')
            status = item.get('status', 'Open')
            sentiment = item.get('sentiment', 'Neutral')
            created_date = item.get('created_date', '')

            content = (
                f"Support Ticket [{doc_id}] for Customer [{customer_id}]\n"
                f"Subject: {subject}\n"
                f"Priority: {priority} | Status: {status} | Sentiment: {sentiment}\n"
                f"Created Date: {created_date}"
            )

            metadata = {
                'doc_id': doc_id,
                'customer_id': str(customer_id),
                'source_type': 'ticket',
                'priority': priority,
                'status': status,
                'sentiment': sentiment,
                'created_date': created_date
            }
            docs.append(Document(page_content=content, metadata=metadata, doc_id=doc_id))
        return docs

    def load_interactions_csv(self, file_path: Optional[str] = None) -> List[Document]:
        """Load interaction logs from CSV into Document objects."""
        path = file_path or os.path.join(self.base_dir, 'interactions.csv')
        if not os.path.exists(path):
            # Fallback to sample if available
            path = 'sample_interactions.csv'
            if not os.path.exists(path):
                return []

        df = pd.read_csv(path)
        docs = []
        for _, row in df.iterrows():
            doc_id = str(row.get('interaction_id', f"INT-{len(docs)+1}"))
            customer_id = str(row.get('customer_id', 'UNKNOWN'))
            itype = row.get('interaction_type', 'Log')
            desc = row.get('description', '')
            timestamp = row.get('timestamp', '')

            content = (
                f"Customer Interaction [{doc_id}] for Customer [{customer_id}]\n"
                f"Type: {itype}\n"
                f"Description: {desc}\n"
                f"Timestamp: {timestamp}"
            )
            metadata = {
                'doc_id': doc_id,
                'customer_id': customer_id,
                'source_type': 'interaction',
                'interaction_type': itype,
                'timestamp': str(timestamp)
            }
            docs.append(Document(page_content=content, metadata=metadata, doc_id=doc_id))
        return docs

    def load_all_customer_documents(self) -> List[Document]:
        """Load all available tickets and interactions into a unified document collection."""
        all_docs = []
        all_docs.extend(self.load_tickets_json())
        all_docs.extend(self.load_interactions_csv())
        return all_docs
