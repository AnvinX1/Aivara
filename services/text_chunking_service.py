import os
import sys
import re
from typing import List, Dict, Any

# Add project root directory to sys.path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import config

def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[Dict[str, Any]]:
    """
    Splits text into overlapping chunks suitable for embedding and vector storage.
    
    Args:
        text: The text to chunk
        chunk_size: Maximum size of each chunk in characters (defaults to config.TEXT_CHUNK_SIZE)
        overlap: Number of characters to overlap between chunks (defaults to config.TEXT_CHUNK_OVERLAP)
    
    Returns:
        List of dictionaries, each containing:
        - 'text': The chunk text
        - 'chunk_index': Zero-based index of the chunk
        - 'start_pos': Starting character position in original text
        - 'end_pos': Ending character position in original text
    """
    # Use config defaults if not provided
    if chunk_size is None:
        chunk_size = config.TEXT_CHUNK_SIZE
    if overlap is None:
        overlap = config.TEXT_CHUNK_OVERLAP
    
    # Handle edge cases
    if not text or not text.strip():
        return []
    
    text = text.strip()
    
    # If text is shorter than chunk_size, return as single chunk
    if len(text) <= chunk_size:
        return [{
            'text': text,
            'chunk_index': 0,
            'start_pos': 0,
            'end_pos': len(text)
        }]
    
    chunks = []
    start = 0
    chunk_index = 0
    
    while start < len(text):
        # Calculate end position
        end = start + chunk_size
        
        # If this is not the last chunk and we haven't reached the end
        if end < len(text):
            # Try to break at sentence boundary
            # Look for sentence endings (., !, ?) followed by space or newline
            # Search within the last 20% of the chunk
            search_start = max(start + int(chunk_size * 0.8), start)
            sentence_end = re.search(r'[.!?]\s+', text[search_start:end])
            
            if sentence_end:
                # Break at sentence boundary
                end = search_start + sentence_end.end()
        else:
            # Last chunk - take all remaining text
            end = len(text)
        
        # Extract chunk
        chunk_text_segment = text[start:end].strip()
        
        # Only add non-empty chunks
        if chunk_text_segment:
            chunks.append({
                'text': chunk_text_segment,
                'chunk_index': chunk_index,
                'start_pos': start,
                'end_pos': end
            })
            chunk_index += 1
        
        # Move start position with overlap
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)  # Ensure we make progress
    
    return chunks

def chunk_text_for_vector_store(text: str, report_id: int, patient_id: str, 
                                report_name: str = None, upload_timestamp: str = None) -> List[Dict[str, Any]]:
    """
    Chunks text and formats it for vector store upsertion.
    
    Args:
        text: The text to chunk
        report_id: ID of the report
        patient_id: ID of the patient (user)
        report_name: Optional name of the report
        upload_timestamp: Optional timestamp of upload
    
    Returns:
        List of dictionaries formatted for upsert_docs, each containing:
        - 'id': Unique chunk ID (report_{report_id}_chunk_{chunk_index})
        - 'text': The chunk text
        - 'patient_id': Patient ID as string
        - 'meta': Metadata dictionary with report info
    """
    chunks = chunk_text(text)
    
    formatted_chunks = []
    for chunk in chunks:
        chunk_id = f"report_{report_id}_chunk_{chunk['chunk_index']}"
        
        meta = {
            'report_id': report_id,
            'chunk_index': chunk['chunk_index'],
            'start_pos': chunk['start_pos'],
            'end_pos': chunk['end_pos']
        }
        
        if report_name:
            meta['report_name'] = report_name
        if upload_timestamp:
            meta['upload_timestamp'] = upload_timestamp
        
        formatted_chunks.append({
            'id': chunk_id,
            'text': chunk['text'],
            'patient_id': str(patient_id),
            'meta': meta
        })
    
    return formatted_chunks

if __name__ == '__main__':
    print("--- Testing text_chunking_service.py ---\n")
    
    # Test 1: Empty text
    print("Test 1: Empty text")
    result = chunk_text("")
    assert result == [], f"Expected empty list, got {result}"
    print("✓ Empty text handled correctly\n")
    
    # Test 2: Short text
    print("Test 2: Short text (< chunk_size)")
    short_text = "This is a short text."
    result = chunk_text(short_text, chunk_size=100)
    assert len(result) == 1, f"Expected 1 chunk, got {len(result)}"
    assert result[0]['text'] == short_text
    print(f"✓ Short text: {result}\n")
    
    # Test 3: Long text with sentence boundaries
    print("Test 3: Long text with sentence boundaries")
    long_text = """
    Patient Name: John Doe. Date: 2024-01-15.
    Blood Test Results: Hemoglobin 14.5 g/dL. WBC count is 7.2 x10^3/uL.
    Platelets: 280 x10^3/uL. RBC: 5.0 x10^6/uL.
    All values are within normal range. Doctor's notes: Patient is healthy.
    Follow-up appointment recommended in 6 months.
    """ * 10  # Make it long enough to require chunking
    
    result = chunk_text(long_text, chunk_size=200, overlap=50)
    assert len(result) > 1, f"Expected multiple chunks, got {len(result)}"
    print(f"✓ Long text chunked into {len(result)} chunks\n")
    
    # Test 4: Formatted chunks for vector store
    print("Test 4: Formatted chunks for vector store")
    formatted = chunk_text_for_vector_store(
        "Test text for vector store. This should be chunked properly.",
        report_id=1,
        patient_id="user_123",
        report_name="Blood Test",
        upload_timestamp="2024-01-15T10:00:00"
    )
    assert len(formatted) > 0, "Expected formatted chunks"
    assert 'id' in formatted[0] and 'text' in formatted[0] and 'patient_id' in formatted[0] and 'meta' in formatted[0]
    print(f"✓ Formatted chunks: {len(formatted)} chunks created\n")
    print(f"First chunk ID: {formatted[0]['id']}")
    print(f"First chunk meta: {formatted[0]['meta']}\n")
    
    print("All text chunking tests passed!")

