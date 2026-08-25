"""
Unit tests for ML Churn Prediction and CLV Forecasting pipeline.
"""

import unittest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Ridge


class TestMLChurnPrediction(unittest.TestCase):

    def setUp(self):
        np.random.seed(42)
        self.df = pd.DataFrame({
            'arr_log': np.log1p(np.random.randint(50000, 2000000, 50)),
            'risk_score': np.random.randint(10, 95, 50),
            'sentiment_score': np.random.choice([1, 0, -1], 50),
            'is_churned': np.random.choice([0, 1], 50, p=[0.7, 0.3]),
            'historical_clv': np.random.uniform(100000, 5000000, 50)
        })

    def test_churn_classifier_training(self):
        features = ['arr_log', 'risk_score', 'sentiment_score']
        X = self.df[features]
        y = self.df['is_churned']

        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        probs = model.predict_proba(X)[:, 1]

        self.assertEqual(len(probs), len(self.df))
        self.assertTrue((probs >= 0.0).all() and (probs <= 1.0).all())

    def test_clv_forecasting(self):
        features = ['arr_log', 'risk_score', 'sentiment_score']
        X = self.df[features]
        y = self.df['historical_clv']

        reg = Ridge(alpha=1.0)
        reg.fit(X, y)
        preds = reg.predict(X)

        self.assertEqual(len(preds), len(self.df))
        self.assertTrue((preds > 0).all())


if __name__ == '__main__':
    unittest.main()
