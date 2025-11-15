
import os
import requests
from typing import List
from sentence_transformers import SentenceTransformer

# Global variable to store the local SentenceTransformer model
_local_sentence_transformer_model = None

def _get_local_model():
    global _local_sentence_transformer_model
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
    Generates text embeddings using OpenRouter API or a local SentenceTransformer model.

    Args:
        text (str): The input text to embed.

    Returns:
        List[float]: The embedding vector.

    Raises:
        RuntimeError: If embedding generation fails with both OpenRouter and local model.
    """

    # Try OpenRouter API first (if model specified)
    # Note: Free embedding models are limited on OpenRouter
    # If not configured, will fall back to local SentenceTransformer model (free)
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    openrouter_embed_model = os.getenv("OPENROUTER_EMBED_MODEL", None)  # Default to None to use free local model
    openrouter_base_url_for_embed = "https://openrouter.ai/api/v1/embeddings"

    if openrouter_api_key and openrouter_embed_model:
        headers = {
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": openrouter_embed_model,
            "input": text
        }
        try:
            print(f"Attempting to get embedding from OpenRouter with model: {openrouter_embed_model}...")
            response = requests.post(openrouter_base_url_for_embed, headers=headers, json=payload, timeout=10)
            response.raise_for_status() # Raise an exception for HTTP errors
            result = response.json()
            if "data" in result and len(result["data"]) > 0 and "embedding" in result["data"][0]:
                print("Embedding successfully retrieved from OpenRouter.")
                return result["data"][0]["embedding"]
            else:
                print(f"OpenRouter API returned an unexpected format: {result}")
        except requests.exceptions.RequestException as e:
            print(f"OpenRouter API request failed: {e}")
        except Exception as e:
            print(f"Error processing OpenRouter API response: {e}")

    print("Falling back to local SentenceTransformer model...")
    # Fallback to local SentenceTransformer model
    model = _get_local_model()
    if model is not False: # Check if loading didn't fail permanently
        try:
            embedding = model.encode(text).tolist()
            print("Embedding successfully generated using local model.")
            return embedding
        except Exception as e:
            print(f"Error generating embedding with local model: {e}")
    else:
        print("Local SentenceTransformer model failed to load previously.")

    raise RuntimeError("Failed to generate embedding: No API key/model or local model failure.")

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
