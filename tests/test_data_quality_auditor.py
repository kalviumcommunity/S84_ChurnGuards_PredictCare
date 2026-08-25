"""
Unit tests for Data Quality Auditor.
"""

import unittest
import pandas as pd
from utils.data_quality_auditor import DataQualityAuditor


class TestDataQualityAuditor(unittest.TestCase):

    def test_valid_dataset(self):
        df = pd.DataFrame({
            'customer_id': ['C-1', 'C-2'],
            'company_name': ['Co A', 'Co B'],
            'arr': [100000, 200000]
        })
        report = DataQualityAuditor.audit_customer_dataset(df)
        self.assertTrue(report['is_valid'])
        self.assertEqual(report['quality_score'], 100)
        self.assertEqual(len(report['errors']), 0)

    def test_missing_column_and_duplicates(self):
        df = pd.DataFrame({
            'customer_id': ['C-1', 'C-1'],
            'company_name': ['Co A', 'Co A']
        })
        report = DataQualityAuditor.audit_customer_dataset(df)
        self.assertFalse(report['is_valid'])
        self.assertIn("Missing mandatory column: 'arr'", report['errors'])
        self.assertIn("duplicate customer_id", report['errors'][1])


if __name__ == '__main__':
    unittest.main()
