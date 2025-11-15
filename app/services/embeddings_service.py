
import os
import sys
import requests
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir)) # Points to /content/aivara_app/aivara-backend
load_dotenv(os.path.join(_project_root, '.env'))

# Try to import SentenceTransformer for fallback
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not installed. Will use Ollama embeddings only.")

# Import config and Ollama service
sys.path.insert(0, _project_root)
import config
from services.ollama_service import get_embedding_via_ollama

# Global variable to store the local SentenceTransformer model (fallback)
_local_sentence_transformer_model = None

def _get_local_model():
    """Gets the local SentenceTransformer model for fallback."""
    global _local_sentence_transformer_model
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        return None
    
    if _local_sentence_transformer_model is None:
        print("Loading local SentenceTransformer model 'sentence-transformers/all-MiniLM-L6-v2'...")
        try:
            _local_sentence_transformer_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            print("Local SentenceTransformer model loaded successfully.")
        except Exception as e:
            print(f"Error loading local SentenceTransformer model: {e}")
            _local_sentence_transformer_model = False # Indicate permanent failure to load
    return _local_sentence_transformer_model

def get_embedding(text: str) -> List[float]:
    """
    Generates text embeddings using Ollama embeddinggemma:latest model, with fallback to SentenceTransformer.

    Args:
        text (str): The input text to embed.

    Returns:
        List[float]: The embedding vector.

    Raises:
        RuntimeError: If embedding generation fails with both Ollama and local model.
    """
    # Try Ollama API first (using embeddinggemma:latest)
    try:
        embedding = get_embedding_via_ollama(text)
        if embedding:
            print(f"Embedding successfully retrieved from Ollama (embeddinggemma:latest).")
            return embedding
    except Exception as e:
        print(f"Ollama embeddings API request failed: {e}")
    
    # Fallback to local SentenceTransformer model
    print("Falling back to local SentenceTransformer model...")
    if SENTENCE_TRANSFORMERS_AVAILABLE:
        model = _get_local_model()
        if model and model is not False: # Check if loading didn't fail permanently
            try:
                embedding = model.encode(text).tolist()
                print("Embedding successfully generated using local SentenceTransformer model.")
                return embedding
            except Exception as e:
                print(f"Error generating embedding with local model: {e}")
        else:
            print("Local SentenceTransformer model failed to load previously.")
    else:
        print("SentenceTransformers not available as fallback.")

    raise RuntimeError("Failed to generate embedding: Ollama unavailable and SentenceTransformer fallback failed.")

if __name__ == '__main__':
    # Example usage
    sample_text = "This is a test sentence for embedding generation."
    print(f"\n--- Testing get_embedding function ---\n")

    # Set dummy environment variables for testing local model fallback
    # If you have actual OpenRouter keys, set them in your environment or .env file
    # os.environ["OPENROUTER_API_KEY"] = "sk-yourkey"
    # os.environ["OPENROUTER_EMBED_MODEL"] = "openai/text-embedding-3-small"

    try:
        embedding_vector = get_embedding(sample_text)
        print(f"Generated embedding (first 5 elements): {embedding_vector[:5]}...")
        print(f"Embedding length: {len(embedding_vector)}")
    except RuntimeError as e:
        print(f"Failed to get embedding: {e}")
