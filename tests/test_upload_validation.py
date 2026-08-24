"""
Unit tests for CSV/JSON upload schema validation (PR 15).
"""

import unittest
import pandas as pd
from utils.validators import (
    SchemaValidator,
    validate_customers_schema,
    validate_tickets_schema,
    validate_interactions_schema
)


class TestUploadSchemaValidation(unittest.TestCase):
    
    def test_valid_customers_schema(self):
        df = pd.DataFrame({
            'customer_id': ['CUST-1001', 'CUST-1002'],
            'company_name': ['Acme Corp', 'Beta Inc'],
            'industry': ['Tech', 'Finance'],
            'arr': [150000, 250000],
            'contract_type': ['Annual', 'Monthly'],
            'renewal_date': ['2026-12-31', '2026-11-30'],
            'csm_name': ['Alice', 'Bob']
        })
        result = validate_customers_schema(df)
        self.assertTrue(result['is_valid'])
        self.assertEqual(len(result['errors']), 0)
        self.assertEqual(result['row_count'], 2)

    def test_customers_missing_required_column(self):
        # Missing 'arr' and 'renewal_date'
        df = pd.DataFrame({
            'company_name': ['Acme Corp']
        })
        result = validate_customers_schema(df)
        self.assertFalse(result['is_valid'])
        self.assertIn('arr', result['missing_required'])
        self.assertIn('renewal_date', result['missing_required'])
        self.assertTrue(any('Missing required column' in err for err in result['errors']))

    def test_customers_invalid_arr_type(self):
        df = pd.DataFrame({
            'company_name': ['Acme Corp', 'Beta Inc'],
            'arr': ['invalid_number', 'not_an_arr'],
            'renewal_date': ['2026-12-31', '2026-11-30']
        })
        result = validate_customers_schema(df)
        self.assertFalse(result['is_valid'])
        self.assertTrue(any('non-numeric' in err for err in result['errors']))

    def test_empty_customers_dataframe(self):
        df = pd.DataFrame()
        result = validate_customers_schema(df)
        self.assertFalse(result['is_valid'])
        self.assertTrue(any('empty' in err for err in result['errors']))

    def test_valid_tickets_json_list(self):
        tickets = [
            {
                'ticket_id': 'TKT-001',
                'customer_id': 'CUST-1001',
                'subject': 'Login issue',
                'priority': 'Critical',
                'status': 'Open',
                'sentiment': 'Negative',
                'created_date': '2026-08-01T10:00:00'
            }
        ]
        result = validate_tickets_schema(tickets)
        self.assertTrue(result['is_valid'])
        self.assertEqual(len(result['errors']), 0)

    def test_tickets_missing_required_field(self):
        tickets = [
            {
                'customer_id': 'CUST-1001',
                'subject': 'Login issue'
                # missing ticket_id, priority, status
            }
        ]
        result = validate_tickets_schema(tickets)
        self.assertFalse(result['is_valid'])
        self.assertIn('ticket_id', result['missing_required'])
        self.assertIn('priority', result['missing_required'])
        self.assertIn('status', result['missing_required'])

    def test_valid_interactions_dataframe(self):
        df = pd.DataFrame({
            'interaction_id': ['INT-1', 'INT-2'],
            'customer_id': ['CUST-1001', 'CUST-1002'],
            'interaction_type': ['Support Call', 'QBR'],
            'description': ['Quarterly review', 'Technical support'],
            'timestamp': ['2026-08-01 10:00:00', '2026-08-02 11:30:00']
        })
        result = validate_interactions_schema(df)
        self.assertTrue(result['is_valid'])
        self.assertEqual(len(result['errors']), 0)

    def test_interactions_missing_timestamp(self):
        df = pd.DataFrame({
            'customer_id': ['CUST-1001'],
            'interaction_type': ['Support Call']
            # missing timestamp
        })
        result = validate_interactions_schema(df)
        self.assertFalse(result['is_valid'])
        self.assertIn('timestamp', result['missing_required'])


if __name__ == '__main__':
    unittest.main()
