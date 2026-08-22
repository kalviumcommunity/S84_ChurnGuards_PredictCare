import os
import unittest
from utils.llm_client import LLMClient
from config.llm_config import DEFAULT_MODEL

class TestLLMConnection(unittest.TestCase):
    def setUp(self):
        # We only run the actual API test if OPENAI_API_KEY is present and not the dummy one
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.should_skip = not self.api_key or self.api_key == "your_openai_api_key_here"
        
        if not self.should_skip:
            self.client = LLMClient()

    def test_basic_completion(self):
        if self.should_skip:
            self.skipTest("Skipping API test: OPENAI_API_KEY is missing or dummy.")
            
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'hello world' and nothing else."}
        ]
        
        response = self.client.generate_completion(messages, max_tokens=10)
        self.assertIn("hello", response.lower())
        self.assertIn("world", response.lower())

if __name__ == "__main__":
    unittest.main()
