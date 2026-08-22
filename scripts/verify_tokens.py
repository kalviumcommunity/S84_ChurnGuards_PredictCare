from utils.token_counter import count_tokens, count_message_tokens
from utils.cost_tracker import CostTracker

# Test token counter
text = "Hello world, this is a test."
tokens = count_tokens(text)
print(f"Tokens in text: {tokens}")

messages = [{"role": "user", "content": text}]
msg_tokens = count_message_tokens(messages)
print(f"Tokens in message: {msg_tokens}")

# Test cost tracker
tracker = CostTracker()
tracker.add_usage(input_tokens=1000, output_tokens=500, model="gpt-4o-mini")
print("Cost summary:")
print(tracker.get_summary())
