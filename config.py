
import os

# JWT Settings
SECRET_KEY = "ed092851a8fff66ac182a333792fb312a6b9160c05231738715bc2f7928ab279"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database Settings
DATABASE_URL = "sqlite:///./aivara.db"

# Uploads Directory
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

# OpenRouter API settings for LLM and Embeddings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", None)
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-flash-1.5")
OPENROUTER_EMBED_MODEL = os.getenv("OPENROUTER_EMBED_MODEL", "openai/text-embedding-3-small")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Vector Store (ChromaDB) settings
VECTOR_DIR = os.getenv("VECTOR_DIR", "./vectorstore")
RAG_TOP_K = int(os.getenv("RAG_TOP_K", 5))
