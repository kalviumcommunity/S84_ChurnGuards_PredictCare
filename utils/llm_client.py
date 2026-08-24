import os
from openai import OpenAI
from dotenv import load_dotenv
from config.llm_config import DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS

load_dotenv()

class LLMClient:
    def __init__(self):
        # We still look for OPENAI_API_KEY because the user replaced the key directly in the .env file
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY environment variable is missing or invalid.")
        # Groq is fully compatible with the OpenAI SDK by changing the base_url
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
    def generate_completion(self, messages, model=DEFAULT_MODEL, temperature=TEMPERATURE, max_tokens=MAX_TOKENS):
        """
        Generate a chat completion from OpenAI.
        
        Args:
            messages: List of message dictionaries containing 'role' and 'content'.
            model: The OpenAI model to use.
            temperature: Sampling temperature.
            max_tokens: Max tokens to generate.
            
        Returns:
            The string response from the model.
        """
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
