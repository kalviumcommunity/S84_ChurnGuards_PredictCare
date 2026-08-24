"""
Test runner for ChurnGuard ETL Data Pipeline.
Can be run directly via `python test_etl_pipeline.py` or via unittest test discovery.
"""

import unittest
from tests.test_etl_pipeline import (
    TestDataIngestion,
    TestDataCleaning,
    TestFeatureEngineering,
    TestETLPipelineIntegration
)

if __name__ == '__main__':
    unittest.main()
