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
    WEB_SEARCH_KEYWORDS = ["current", "latest", "news", "today", "war", "president", "election", "sports", "weather", "stock", "market", "technology", "science", "health", "covid", "pandemic", "economy", "finance", "business", "entertainment", "celebrity", "movie", "music", "art", "culture", "travel", "tourism", "food", "restaurant", "recipe", "fitness", "exercise", "workout", "yoga", "meditation", "mental health", "wellness", "self-care", "productivity", "time management", "motivation", "inspiration", "success", "career", "job", "hiring", "recruitment", "interview", "resume", "cover letter", "salary", "negotiation", "leadership", "management", "entrepreneurship", "startup", "innovation", "technology trends", "artificial intelligence", "machine learning", "data science", "programming languages", "software development", "cybersecurity", "blockchain", "cryptocurrency", "gaming", "esports", "virtual reality", "augmented reality", "space exploration", "climate change", "environment", "sustainability", "social issues", "politics", "international relations", "human rights", "education", "parenting", "relationships", "dating", "lifestyle", "fashion", "beauty", "home decor", "gardening", "diy", "hobbies", "pets", "animals", "sports", "fitness", "health", "medicine", "psychology", "philosophy", "history", "culture", "art", "literature", "music", "movies", "tv shows", "celebrities", "trending topics", "viral", "breaking news", "headlines", "current events", "world news", "local news", "technology news", "science news", "health news", "business news", "entertainment news", "sports news", "weather news", "stock market news", "political news", "social media trends", "internet trends", "memes", "viral content", "trending hashtags", "current affairs", "news updates", "latest developments", "breaking stories", "hot topics", "trending discussions", "current trends", "newsworthy events", "popular culture", "media coverage", "public opinion", "social issues", "global events", "economic news", "financial news", "technology trends", "innovation news", "science discoveries", "health breakthroughs", "sports highlights", "entertainment gossip", "celebrity news", "fashion trends", "lifestyle tips", "travel destinations", "food trends", "fitness advice", "mental health awareness", "self-care tips", "productivity hacks", "career advice", "job market trends", "leadership insights", "entrepreneurship tips", "startup news", "investment trends", "cryptocurrency updates", "gaming news", "esports highlights", "virtual reality developments", "augmented reality applications", "space exploration news", "climate change updates", "environmental news", "sustainability initiatives", "social issues discussions", "political analysis", "international relations updates", "human rights advocacy", "education reforms", "parenting advice", "relationship tips", "teach me", "guide me", "how to use", "tell me about"]
    
    # Paths
    DATA_DIR = "data"