"""
Unit tests for Export Manager.
"""

import unittest
import pandas as pd
from utils.export_manager import ExportManager


class TestExportManager(unittest.TestCase):

    def test_executive_summary_markdown(self):
        kpis = {
            'total_customers': 200,
            'avg_risk_score': 35.5,
            'revenue_at_risk': 250000.0,
            'churn_rate': 12.5
        }
        df = pd.DataFrame([
            {'customer_id': 'CUST-1', 'company_name': 'Alpha Inc', 'risk_score': 85, 'arr': 150000, 'health_status': 'Critical'}
        ])
        md = ExportManager.generate_executive_summary_markdown(kpis, df)
        self.assertIn("ChurnGuard AI Executive Churn", md)
        self.assertIn("Alpha Inc", md)
        self.assertIn("$250,000.00", md)

    def test_export_dataframe_to_csv_bytes(self):
        df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
        b = ExportManager.export_dataframe_to_csv_bytes(df)
        self.assertIsInstance(b, bytes)
        self.assertIn(b"a,b", b)


if __name__ == '__main__':
    unittest.main()
