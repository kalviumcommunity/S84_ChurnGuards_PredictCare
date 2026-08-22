from config.llm_config import DEFAULT_MODEL

class CostTracker:
    # Pricing per 1k tokens in USD (as of standard gpt-4o-mini pricing)
    PRICING = {
        "gpt-4o-mini": {"input": 0.000150, "output": 0.000600},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        # Add more models as needed
    }

    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0

    def add_usage(self, input_tokens: int, output_tokens: int, model: str = DEFAULT_MODEL):
        """
        Record usage for a request and update total cost.
        """
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        
        rates = self.PRICING.get(model, self.PRICING["gpt-4o-mini"])
        cost = (input_tokens / 1000.0) * rates["input"] + (output_tokens / 1000.0) * rates["output"]
        self.total_cost += cost
        
    def get_summary(self) -> dict:
        """
        Return a summary of usage and cost.
        """
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_cost_usd": self.total_cost
        }
