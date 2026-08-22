import tiktoken
from config.llm_config import DEFAULT_MODEL

def count_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
    """
    Returns the number of tokens in a text string.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def count_message_tokens(messages: list, model: str = DEFAULT_MODEL) -> int:
    """
    Returns the number of tokens used by a list of messages.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
        
    num_tokens = 0
    for message in messages:
        num_tokens += 3  # Every message follows <|start|>{role/name}\n{content}<|end|>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += 1
    num_tokens += 3  # Every reply is primed with <|start|>assistant<|message|>
    return num_tokens
