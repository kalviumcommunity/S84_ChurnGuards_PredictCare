"""
Unit tests for Email Alert Notification formatting.
"""

import unittest
from scripts.email_alerts import format_email_body


class TestEmailAlerts(unittest.TestCase):

    def test_format_email_body(self):
        sample_alerts = [
            ("Acme Corp", 250000, 88, "Critical", "Negative"),
            ("Beta Inc", 120000, 82, "Critical", "Neutral")
        ]
        html = format_email_body(sample_alerts)
        self.assertIn("Daily Risk Command Center Report", html)
        self.assertIn("Acme Corp", html)
        self.assertIn("$250k", html)
        self.assertIn("88", html)

    def test_empty_alerts(self):
        html = format_email_body([])
        self.assertIn("Daily Risk Command Center Report", html)


if __name__ == '__main__':
    unittest.main()
