
import os
import sys
from typing import List, Dict, Any
from dotenv import load_dotenv

# Monkey-patch numpy to handle `np.float_` removal for chromadb compatibility
# This MUST be done before chromadb is imported.
import numpy as np
if not hasattr(np, 'float_'):
    np.float_ = np.float64

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    chromadb = None
    CHROMADB_AVAILABLE = False
    print("Warning: chromadb not installed. Vector store features will be disabled.")

# Add project root directory to sys.path within vector_store.py for its own imports.
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_current_dir)) # Points to /content/aivara_app/aivara-backend
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Load environment variables from .env file
load_dotenv(os.path.join(_project_root, '.env'))

import config

# Optional import - handle gracefully if embeddings service fails
try:
    from app.services.embeddings_service import get_embedding
except Exception as e:
    print(f"Warning: Failed to import embeddings_service: {e}")
    print("Vector store features will be disabled. Please fix dependencies or use OpenRouter API.")
    def get_embedding(text: str):
        raise RuntimeError("Embeddings service not available. Fix dependencies or configure OpenRouter API.")

# Global variables for ChromaDB client and collection
_chroma_client = None
_chroma_collection = None

def _get_chroma_collection():
    global _chroma_client, _chroma_collection
    if not CHROMADB_AVAILABLE:
        raise RuntimeError("ChromaDB is not installed. Please install chromadb to use vector store features.")
    if _chroma_collection is None:
        print(f"Initializing ChromaDB persistent client in {config.VECTOR_DIR}...")
        _chroma_client = chromadb.PersistentClient(path=config.VECTOR_DIR)
        _chroma_collection = _chroma_client.get_or_create_collection(name="aivara_collection")
        print("ChromaDB collection 'aivara_collection' initialized.")
    return _chroma_collection

def upsert_docs(items: List[Dict[str, Any]]) -> None:
    """
    Adds or updates documents (chunks) in the vector store.
    Each item in 'items' must contain 'id', 'text', 'patient_id', and 'meta' (dict).
    """
    collection = _get_chroma_collection()

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for item in items:
        doc_id = str(item['id'])
        text = item['text']
        patient_id = str(item['patient_id'])
        meta = item.get('meta', {})

        # Ensure patient_id is in metadata for filtering
        meta['patient_id'] = patient_id

        try:
            embedding = get_embedding(text)
            ids.append(doc_id)
            embeddings.append(embedding)
            documents.append(text)
            metadatas.append(meta)
        except RuntimeError as e:
            print(f"Warning: Skipping document {doc_id} due to embedding failure: {e}")

    if ids:
        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Upserted {len(ids)} documents into ChromaDB.")
    else:
        print("No documents to upsert.")

def search(patient_id: str, query: str, k: int = config.RAG_TOP_K) -> List[Dict[str, Any]]:
    """
    Searches the vector store for relevant document chunks for a given patient and query.
    Returns a list of dictionaries with 'text', 'score', and 'meta'.
    """
    collection = _get_chroma_collection()

    try:
        query_embedding = get_embedding(query)
    except RuntimeError as e:
        print(f"Error generating embedding for query: {e}")
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        where={"patient_id": patient_id},
        include=['documents', 'distances', 'metadatas']
    )

    if results['documents']:
        # Combine documents, distances, and metadatas into a list of dicts
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                "text": results['documents'][0][i],
                "score": results['distances'][0][i],
                "meta": results['metadatas'][0][i]
            })
        return formatted_results
    return []

def patient_context(patient_id: str, query: str, k: int = config.RAG_TOP_K) -> str:
    """
    Retrieves and concatenates top-k relevant text chunks for a patient's context.
    """
    relevant_chunks = search(patient_id, query, k)
    if relevant_chunks:
        context_text = "\n\n".join([chunk['text'] for chunk in relevant_chunks])
        return context_text
    return ""

if __name__ == '__main__':
    print("\n--- Testing vector_store.py ---\n")

    # Mock environment variables for embeddings_service to fall back to local model
    # if OpenRouter API key is not set for local testing.
    original_openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    original_openrouter_embed_model = os.getenv("OPENROUTER_EMBED_MODEL")

    # Temporarily set mock OpenRouter env vars to force local model usage for testing
    # if no real key is configured.
    os.environ["OPENROUTER_API_KEY"] = "mock_key"
    os.environ["OPENROUTER_EMBED_MODEL"] = "mock_model_name"

    # Temporarily set VECTOR_DIR for testing purposes
    original_vector_dir = config.VECTOR_DIR
    test_vector_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_vector_db")
    config.VECTOR_DIR = test_vector_dir

    # Clean up any previous test vector store
    if os.path.exists(test_vector_dir):
        import shutil
        shutil.rmtree(test_vector_dir)
        print(f"Cleaned up previous test vector store: {test_vector_dir}")

    # Dummy data for upsertion
    dummy_items = [
        {"id": "doc1", "text": "Patient John Doe has a history of high blood pressure and diabetes.", "patient_id": "patient_123", "meta": {"report_id": 1, "page": 1}},
        {"id": "doc2", "text": "Latest blood test results show HbA1c of 7.2% and LDL of 130 mg/dL.", "patient_id": "patient_123", "meta": {"report_id": 1, "page": 2}},
        {"id": "doc3", "text": "Regular exercise and diet control are recommended for managing diabetes.", "patient_id": "patient_123", "meta": {"report_id": 2, "page": 1}},
        {"id": "doc4", "text": "Sarah's annual check-up shows normal vitals. No major concerns.", "patient_id": "patient_456", "meta": {"report_id": 3, "page": 1}},
    ]

    try:
        # 1. Upsert documents
        print("\nUpserting dummy documents...")
        upsert_docs(dummy_items)

        # 2. Search for relevant chunks for a specific patient and query
        print("\nSearching for 'diabetes management' for patient_123...")
        search_query = "What are the recommendations for diabetes management?"
        results = search(patient_id="patient_123", query=search_query, k=2)
        print(f"Search Results (Patient 123):\n{results}")
        assert len(results) > 0

        # 3. Get patient context
        print("\nGetting patient context for 'blood sugar control' for patient_123...")
        context_query = "What is the patient's blood sugar control status?"
        context = patient_context(patient_id="patient_123", query=context_query, k=2)
        print(f"Patient Context (Patient 123):\n{context}")
        assert ("HbA1c of 7.2%" in context or "managing diabetes" in context)

        # Search for another patient
        print("\nSearching for 'annual check-up' for patient_456...")
        results_sarah = search(patient_id="patient_456", query="annual check-up", k=1)
        print(f"Search Results (Patient 456):\n{results_sarah}")
        assert len(results_sarah) > 0

        print("\nVector store tests completed successfully!")

    except Exception as e:
        print(f"An error occurred during testing: {e}")

    finally:
        # Clean up test vector store
        if os.path.exists(test_vector_dir):
            import shutil
            shutil.rmtree(test_vector_dir)
            print(f"Cleaned up test vector store: {test_vector_dir}")

        # Restore original environment variables
        if original_openrouter_api_key is not None:
            os.environ["OPENROUTER_API_KEY"] = original_openrouter_api_key
        else:
            if "OPENROUTER_API_KEY" in os.environ:
                del os.environ["OPENROUTER_API_KEY"]
        if original_openrouter_embed_model is not None:
            os.environ["OPENROUTER_EMBED_MODEL"] = original_openrouter_embed_model
        else:
            if "OPENROUTER_EMBED_MODEL" in os.environ:
                del os.environ["OPENROUTER_EMBED_MODEL"]

        config.VECTOR_DIR = original_vector_dir
