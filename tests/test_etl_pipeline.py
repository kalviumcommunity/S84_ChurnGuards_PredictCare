"""
Unit and integration tests for ChurnGuard ETL Data Pipeline (PR 17).
Covers data ingestion, data cleaning, and feature engineering.
"""

import os
import tempfile
import json
import unittest
import pandas as pd
import numpy as np

from scripts.data_ingestion import load_data
from scripts.data_cleaning import clean_data
from scripts.feature_engineering import engineer_features


class TestDataIngestion(unittest.TestCase):
    """Tests for scripts/data_ingestion.py"""

    @classmethod
    def setUpClass(cls):
        """Ensure test data files exist in data directory."""
        if not os.path.exists('data/customers.csv') or not os.path.exists('data/interactions.csv'):
            import subprocess
            subprocess.run(['python', 'scripts/generate_mock_data.py'], capture_output=True)

    def test_load_data_existing_directory(self):
        """Verify load_data successfully loads standard datasets from data directory."""
        customers, tickets, interactions, churn_history = load_data('data')
        self.assertIsInstance(customers, pd.DataFrame)
        self.assertIsInstance(tickets, pd.DataFrame)
        self.assertIsInstance(interactions, pd.DataFrame)
        self.assertIsInstance(churn_history, pd.DataFrame)
        
        self.assertFalse(customers.empty, "Customers dataframe should not be empty")
        self.assertFalse(tickets.empty, "Tickets dataframe should not be empty")
        self.assertFalse(interactions.empty, "Interactions dataframe should not be empty")

    def test_load_data_nonexistent_directory(self):
        """Verify load_data handles missing directory gracefully without throwing exceptions."""
        customers, tickets, interactions, churn_history = load_data('non_existent_folder_xyz')
        self.assertTrue(customers.empty)
        self.assertTrue(tickets.empty)
        self.assertTrue(interactions.empty)
        self.assertTrue(churn_history.empty)

    def test_load_data_custom_temp_directory(self):
        """Verify load_data correctly parses custom CSV and JSON files in a temporary folder."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cust_df = pd.DataFrame({'customer_id': ['CUST-1'], 'company_name': ['Test Co'], 'arr': [100000]})
            cust_df.to_csv(os.path.join(tmpdir, 'customers.csv'), index=False)

            tickets_data = [{'ticket_id': 'TKT-1', 'customer_id': 'CUST-1', 'priority': 'High'}]
            with open(os.path.join(tmpdir, 'tickets.json'), 'w') as f:
                json.dump(tickets_data, f)

            customers, tickets, interactions, churn_history = load_data(tmpdir)
            self.assertEqual(len(customers), 1)
            self.assertEqual(len(tickets), 1)
            self.assertTrue(interactions.empty)
            self.assertTrue(churn_history.empty)


class TestDataCleaning(unittest.TestCase):
    """Tests for scripts/data_cleaning.py"""

    def test_clean_data_date_conversions(self):
        """Verify clean_data converts string dates to pandas datetime objects."""
        customers = pd.DataFrame({'customer_id': ['CUST-1'], 'renewal_date': ['2026-12-31']})
        tickets = pd.DataFrame({
            'ticket_id': ['TKT-1'],
            'created_date': ['2026-08-01T10:00:00'],
            'resolved_date': ['2026-08-02T12:00:00']
        })
        interactions = pd.DataFrame({'interaction_id': ['INT-1'], 'timestamp': ['2026-08-10 14:00:00']})
        churn_history = pd.DataFrame({'customer_id': ['CHURN-1'], 'churn_date': ['2026-05-15']})

        c, t, i, ch = clean_data(customers, tickets, interactions, churn_history)

        self.assertTrue(pd.api.types.is_datetime64_any_dtype(c['renewal_date']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(t['created_date']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(t['resolved_date']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(i['timestamp']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(ch['churn_date']))

    def test_clean_data_empty_inputs(self):
        """Verify clean_data safely processes empty DataFrames without raising errors."""
        empty_c = pd.DataFrame()
        empty_t = pd.DataFrame()
        empty_i = pd.DataFrame()
        empty_ch = pd.DataFrame()

        c, t, i, ch = clean_data(empty_c, empty_t, empty_i, empty_ch)
        self.assertTrue(c.empty)
        self.assertTrue(t.empty)
        self.assertTrue(i.empty)
        self.assertTrue(ch.empty)


class TestFeatureEngineering(unittest.TestCase):
    """Tests for scripts/feature_engineering.py"""

    def setUp(self):
        self.customers = pd.DataFrame({
            'customer_id': ['CUST-101', 'CUST-102', 'CUST-103'],
            'company_name': ['Alpha Corp', 'Beta Inc', 'Gamma LLC'],
            'arr': [200000, 150000, 300000],
            'sentiment': ['Positive', 'Negative', 'Neutral']
        })

    def test_base_risk_score_and_ticket_impact(self):
        """Verify tickets priority and sentiment correctly update the risk score."""
        tickets = pd.DataFrame({
            'ticket_id': ['TKT-1', 'TKT-2', 'TKT-3'],
            'customer_id': ['CUST-101', 'CUST-102', 'CUST-102'],
            'priority': ['Low', 'Critical', 'High'],
            'status': ['Open', 'Open', 'Open'],
            'sentiment': ['Neutral', 'Negative', 'Negative']
        })
        interactions = pd.DataFrame({
            'interaction_id': ['INT-1', 'INT-2'],
            'customer_id': ['CUST-101', 'CUST-102'],
            'timestamp': [pd.Timestamp.now() - pd.Timedelta(days=5), pd.Timestamp.now() - pd.Timedelta(days=40)]
        })

        cust_feat, tkt_feat = engineer_features(self.customers.copy(), tickets, interactions)

        # CUST-101: Base 20, 0 critical, 0 high, 0 neg ticket, active (<=30d) -> Risk: 20
        c101 = cust_feat[cust_feat['customer_id'] == 'CUST-101'].iloc[0]
        self.assertEqual(c101['risk_score'], 20)
        self.assertEqual(c101['health_status'], 'Low Risk')

        # CUST-102: Base 20 + 1 Critical (15) + 1 High (10) + 2 Neg tickets (10) + Inactive >30d (20) = 75
        c102 = cust_feat[cust_feat['customer_id'] == 'CUST-102'].iloc[0]
        self.assertEqual(c102['risk_score'], 75)
        self.assertEqual(c102['health_status'], 'Critical')

    def test_risk_score_capping(self):
        """Verify risk score never exceeds 100 even with excessive risk factors."""
        heavy_tickets = pd.DataFrame({
            'ticket_id': [f'TKT-{i}' for i in range(15)],
            'customer_id': ['CUST-101'] * 15,
            'priority': ['Critical'] * 15,
            'status': ['Open'] * 15,
            'sentiment': ['Negative'] * 15
        })
        interactions = pd.DataFrame({
            'interaction_id': ['INT-1'],
            'customer_id': ['CUST-101'],
            'timestamp': [pd.Timestamp.now() - pd.Timedelta(days=60)]
        })

        cust_feat, _ = engineer_features(self.customers.copy(), heavy_tickets, interactions)
        c101 = cust_feat[cust_feat['customer_id'] == 'CUST-101'].iloc[0]
        self.assertLessEqual(c101['risk_score'], 100)

    def test_health_status_thresholds(self):
        """Verify health status labels correctly map to risk thresholds."""
        tickets = pd.DataFrame()
        interactions = pd.DataFrame()

        cust_feat, _ = engineer_features(self.customers.copy(), tickets, interactions)
        for _, row in cust_feat.iterrows():
            if row['risk_score'] >= 75:
                self.assertEqual(row['health_status'], 'Critical')
            elif row['risk_score'] >= 50:
                self.assertEqual(row['health_status'], 'Medium')
            else:
                self.assertEqual(row['health_status'], 'Low Risk')

    def test_mathematical_churn_probability(self):
        """Verify churn probability is calculated, capped (0.01 to 0.99), and rounded to 4 decimals."""
        tickets = pd.DataFrame({
            'ticket_id': ['TKT-1'],
            'customer_id': ['CUST-101'],
            'priority': ['Critical'],
            'status': ['Open'],
            'sentiment': ['Negative']
        })
        interactions = pd.DataFrame({
            'interaction_id': ['INT-1'],
            'customer_id': ['CUST-101'],
            'timestamp': [pd.Timestamp.now() - pd.Timedelta(days=10)]
        })

        cust_feat, _ = engineer_features(self.customers.copy(), tickets, interactions)
        self.assertIn('predicted_churn_prob', cust_feat.columns)
        
        for prob in cust_feat['predicted_churn_prob']:
            self.assertGreaterEqual(prob, 0.01)
            self.assertLessEqual(prob, 0.99)
            # Verify 4 decimal places
            self.assertEqual(round(prob, 4), prob)

    def test_empty_customers_generates_mock_dataset(self):
        """Verify engineer_features generates fallback customer dataset when given an empty DataFrame."""
        empty_cust = pd.DataFrame()
        empty_tickets = pd.DataFrame()
        empty_interactions = pd.DataFrame()

        cust_feat, tkt_feat = engineer_features(empty_cust, empty_tickets, empty_interactions)
        self.assertFalse(cust_feat.empty)
        self.assertEqual(len(cust_feat), 200)
        self.assertIn('risk_score', cust_feat.columns)
        self.assertIn('predicted_churn_prob', cust_feat.columns)


class TestETLPipelineIntegration(unittest.TestCase):
    """End-to-end test chaining Ingestion -> Cleaning -> Feature Engineering."""

    def test_end_to_end_pipeline_execution(self):
        """Verify full ETL pipeline runs seamlessly from data loading to feature outputs."""
        customers, tickets, interactions, churn_history = load_data('data')
        c_clean, t_clean, i_clean, ch_clean = clean_data(customers, tickets, interactions, churn_history)
        c_final, t_final = engineer_features(c_clean, t_clean, i_clean)

        self.assertEqual(len(c_final), len(customers))
        self.assertIn('risk_score', c_final.columns)
        self.assertIn('health_status', c_final.columns)
        self.assertIn('predicted_churn_prob', c_final.columns)
        self.assertFalse(c_final['predicted_churn_prob'].isna().any())


if __name__ == '__main__':
    unittest.main()
