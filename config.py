
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JWT Settings
SECRET_KEY = "ed092851a8fff66ac182a333792fb312a6b9160c05231738715bc2f7928ab279"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database Settings
DATABASE_URL = "sqlite:///./aivara.db"

# Uploads Directory
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

# Ollama API settings for LLM and Embeddings
# Using local Ollama models
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Model configuration dictionary
OLLAMA_LLM_GENERAL = os.getenv("OLLAMA_LLM_GENERAL", "llama3.2")
OLLAMA_LLM_REPORT_READING = os.getenv("OLLAMA_LLM_REPORT_READING", "qwen3-vl:2b")
OLLAMA_LLM_MEDICINE = os.getenv("OLLAMA_LLM_MEDICINE", "medbot")
OLLAMA_LLM_WOMEN_HEALTH = os.getenv("OLLAMA_LLM_WOMEN_HEALTH", "edi")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "embeddinggemma:latest")

# Vector Store (ChromaDB) settings
VECTOR_DIR = os.getenv("VECTOR_DIR", "./vectorstore")
RAG_TOP_K = int(os.getenv("RAG_TOP_K", 5))

# Text Chunking settings
TEXT_CHUNK_SIZE = int(os.getenv("TEXT_CHUNK_SIZE", 500))
TEXT_CHUNK_OVERLAP = int(os.getenv("TEXT_CHUNK_OVERLAP", 50))
