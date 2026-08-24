import os
from dotenv import load_dotenv

load_dotenv()

# Default LLM settings (Updated for Groq)
DEFAULT_MODEL = "groq/compound-mini"
MAX_TOKENS = 1000
TEMPERATURE = 0.3

# Embedding settings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Retrieval settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
