import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Model settings
    OLLAMA_MODEL = "mistral:latest"  # or "phi3:mini", "llama3.2"
    OLLAMA_BASE_URL = "http://localhost:11434"
    
    # API Keys
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    
    # RAG settings
    CHUNK_SIZE = 500
    MAX_DOCUMENT_CHARS = 8000
    TEMPERATURE_DOCUMENT = 0.1  # Low for factual answers
    TEMPERATURE_CHAT = 0.7       # Higher for creative answers
    
    # Web search (disabled by default - enable when needed)
    AUTO_WEB_SEARCH = False
    WEB_SEARCH_KEYWORDS = ["current", "latest", "news", "today", "war"]
    
    # Paths
    DATA_DIR = "data"