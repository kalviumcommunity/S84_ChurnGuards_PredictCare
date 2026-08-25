"""
Unit tests for Pipeline CLI Scheduler.
"""

import unittest
import os
from scripts.scheduler import job_email_alerts, job_snapshot_manager


class TestPipelineScheduler(unittest.TestCase):

    def test_job_definitions(self):
        self.assertTrue(callable(job_email_alerts))
        self.assertTrue(callable(job_snapshot_manager))

    def test_scripts_exist(self):
        root_dir = os.path.dirname(os.path.dirname(__file__))
        scripts_dir = os.path.join(root_dir, 'scripts')
        self.assertTrue(os.path.exists(os.path.join(scripts_dir, 'email_alerts.py')))
        self.assertTrue(os.path.exists(os.path.join(root_dir, 'snapshot_manager.py')))


if __name__ == '__main__':
    unittest.main()
