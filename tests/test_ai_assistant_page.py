"""
Unit tests for AI Assistant page module structure.
"""

import unittest
import importlib


class TestAIAssistantPage(unittest.TestCase):

    def test_ai_assistant_importable(self):
        mod = importlib.import_module("app_pages.6_ai_assistant")
        self.assertTrue(hasattr(mod, "render_ai_assistant_page"))


if __name__ == '__main__':
    unittest.main()
