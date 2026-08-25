"""
Unit tests for Advanced Analytics SQL queries.
"""

import unittest
from db_queries import ChurnGuardDB
import pandas as pd


class TestAdvancedAnalyticsQueries(unittest.TestCase):

    def setUp(self):
        self.db = ChurnGuardDB('churnguard.db')

    def test_cohort_retention_analysis(self):
        df = self.db.get_cohort_retention_analysis()
        self.assertIsInstance(df, pd.DataFrame)

    def test_arr_bridge_metrics(self):
        metrics = self.db.get_arr_bridge_metrics()
        self.assertIsInstance(metrics, dict)
        self.assertIn('total_arr', metrics)

    def test_risk_distribution_summary(self):
        df = self.db.get_risk_distribution_summary()
        self.assertIsInstance(df, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
