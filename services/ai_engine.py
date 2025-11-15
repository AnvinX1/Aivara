
import os
import sys
import json
import requests
from typing import Dict, Any, Optional

# Add project root directory to sys.path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import config

# LLM Client Configuration (using OpenRouter)
# Using free models (Llama/Mistral) by default
# Environment variables for OpenRouter API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# Default to free Llama model - can be overridden with env var
# Options: meta-llama/Llama-3.2-3B-Instruct-free, meta-llama/Llama-3.1-8B-Instruct-free, mistralai/mistral-7b-instruct:free
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/Llama-3.2-3B-Instruct-free")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")

def _call_llm(prompt: str) -> str | None:
    """
    Calls the configured LLM API (OpenRouter) with the given prompt.
    """
    if not OPENROUTER_API_KEY:
        print("OPENROUTER_API_KEY not set. Cannot call LLM API.")
        return None

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # "HTTP-Referer": "YOUR_APP_URL", # Optional: Replace with your actual app URL
        # "X-Title": "YOUR_APP_NAME", # Optional: Replace with your actual app name
    }
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(OPENROUTER_BASE_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        if result and "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            print(f"LLM API returned an unexpected format: {result}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"LLM API request failed: {e}")
        return None
    except Exception as e:
        print(f"Error processing LLM API response: {e}")
        return None

def make_explanation(parsed_data: Dict[str, Any], context_text: str | None = None, 
                     historical_context: str | None = None) -> Dict[str, Any]:
    """
    Generates an LLM-based explanation for the health markers.
    
    Args:
        parsed_data: Dictionary of health markers and their values
        context_text: Context from the current report (e.g., analysis summary)
        historical_context: Historical context from patient's previous reports (RAG-retrieved)
    """
    prompt_parts = [
        "You are an AI assistant specialized in explaining medical report results to a patient in a simple, calm, and reassuring manner. Avoid medical jargon where possible.",
        "Provide a brief summary and simple explanation for the following health markers. Focus on whether they are within normal limits and what that generally means."
    ]

    if historical_context:
        prompt_parts.append("Here is relevant information from the patient's previous medical reports that may help provide context:")
        prompt_parts.append(historical_context)
        prompt_parts.append("Use this historical context to provide more informed explanations, especially if there are trends or changes to note.")

    if context_text:
        prompt_parts.append(f"Here is some additional context from the current report: {context_text}")

    marker_details = []
    for marker, value in parsed_data.items():
        if value is not None:
            marker_details.append(f"{marker.replace('_', ' ').capitalize()}: {value}")
        else:
            marker_details.append(f"{marker.replace('_', ' ').capitalize()}: Not found")

    prompt_parts.append("\nHealth Markers:\n" + "\n".join(marker_details))
    prompt_parts.append("\nGenerate a patient-friendly explanation:")

    full_prompt = "\n".join(prompt_parts)
    # print("\n--- LLM Prompt ---")
    # print(full_prompt)
    # print("\n------------------")

    explanation_text = _call_llm(full_prompt)

    if explanation_text:
        return {"llm_explanation": explanation_text}
    else:
        return {"llm_explanation": "Could not generate an LLM explanation at this time."}

def analyze_health_markers(markers: Dict[str, float | None], patient_id: Optional[str] = None, 
                          query: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyzes a given set of health markers based on predefined rules and thresholds.
    Returns a dictionary with analysis results, including a summary and specific observations.
    Also includes an LLM-generated explanation with optional RAG context from historical reports.
    
    Args:
        markers: Dictionary of health markers and their values
        patient_id: Optional patient ID for retrieving historical context via RAG
        query: Optional query string for RAG context retrieval (if None, generated from markers)
    """
    analysis_results = {
        "summary": "No significant anomalies detected.",
        "observations": []
    }

    # Define reference ranges (example values - these should be clinically accurate)
    reference_ranges = {
        "hemoglobin": {"low": 12.0, "normal_min": 12.0, "normal_max": 17.5, "high": 17.5},
        "wbc": {"low": 4.0, "normal_min": 4.0, "normal_max": 11.0, "high": 11.0}, # x10^3/uL
        "platelets": {"low": 150, "normal_min": 150, "normal_max": 450, "high": 450}, # x10^3/uL
        "rbc": {"low": 4.5, "normal_min": 4.5, "normal_max": 5.9, "high": 5.9} # x10^6/uL
    }

    abnormalities_found = False

    for marker, value in markers.items():
        if value is None:
            analysis_results["observations"].append(f"No value found for {marker.replace('_', ' ').capitalize()}.")
            continue

        ranges = reference_ranges.get(marker)
        if not ranges:
            analysis_results["observations"].append(f"No reference range defined for {marker.replace('_', ' ').capitalize()}.")
            continue

        if value < ranges["low"]:
            analysis_results["observations"].append(f"{marker.replace('_', ' ').capitalize()} is Low: {value} (Normal range: {ranges['normal_min']} - {ranges['normal_max']}).")
            abnormalities_found = True
        elif value > ranges["high"]:
            analysis_results["observations"].append(f"{marker.replace('_', ' ').capitalize()} is High: {value} (Normal range: {ranges['normal_min']} - {ranges['normal_max']}).")
            abnormalities_found = True
        else:
            analysis_results["observations"].append(f"{marker.replace('_', ' ').capitalize()} is within Normal range: {value}.")

    if abnormalities_found:
        analysis_results["summary"] = "Potential anomalies detected in one or more health markers. Please consult a doctor."

    # Retrieve historical context using RAG if patient_id is provided
    historical_context = None
    if patient_id:
        try:
            from app.services.vector_store import patient_context as get_patient_context
            
            # Generate query from markers if not provided
            if query is None:
                marker_query_parts = []
                for marker, value in markers.items():
                    if value is not None:
                        marker_query_parts.append(f"{marker.replace('_', ' ')} {value}")
                if marker_query_parts:
                    query = f"Previous reports with {', '.join(marker_query_parts)}"
                else:
                    query = "Previous medical reports and health history"
            
            # Retrieve historical context
            historical_context = get_patient_context(patient_id=patient_id, query=query, k=config.RAG_TOP_K)
            
            if not historical_context:
                # Fallback: try a more general query
                historical_context = get_patient_context(
                    patient_id=patient_id, 
                    query="Previous medical reports and test results", 
                    k=config.RAG_TOP_K
                )
        except Exception as e:
            # Log error but don't fail analysis if RAG retrieval fails
            print(f"Warning: Failed to retrieve historical context for patient {patient_id}: {e}")
            historical_context = None

    # Generate LLM explanation with historical context
    llm_explanation_data = make_explanation(
        markers, 
        context_text=analysis_results["summary"],
        historical_context=historical_context
    )
    analysis_results.update(llm_explanation_data)

    return analysis_results

if __name__ == '__main__':
    print("--- Testing analyze_health_markers with LLM explanation ---")

    # Mock LLM API Key for local testing if not set
    if not os.getenv("OPENROUTER_API_KEY"):
        os.environ["OPENROUTER_API_KEY"] = "sk-mock-key" # Set a mock key if not present
    # Restore original key later if needed
    original_openrouter_key = os.getenv("OPENROUTER_API_KEY")
    original_openrouter_model = os.getenv("OPENROUTER_MODEL")
    original_openrouter_base_url = os.getenv("OPENROUTER_BASE_URL")

    # Set mock values for testing purposes if they are not already set
    os.environ["OPENROUTER_API_KEY"] = "sk-or-your-actual-openrouter-key"
    os.environ["OPENROUTER_MODEL"] = "google/gemini-flash-1.5"
    os.environ["OPENROUTER_BASE_URL"] = "https://openrouter.ai/api/v1/chat/completions"

    # Test Case 1: All markers normal
    normal_markers = {"hemoglobin": 14.5, "wbc": 7.0, "platelets": 300.0, "rbc": 5.2}
    print(f"\nAnalyzing normal markers: {normal_markers}")
    normal_analysis = analyze_health_markers(normal_markers)
    print("Analysis Result:")
    for obs in normal_analysis["observations"]:
        print(f"  - {obs}")
    print(f"Summary: {normal_analysis['summary']}")
    print(f"LLM Explanation: {normal_analysis.get('llm_explanation')}")

    # Test Case 2: Low Hemoglobin, High WBC
    abnormal_markers_1 = {"hemoglobin": 11.0, "wbc": 12.5, "platelets": 280.0, "rbc": 5.0}
    print(f"\nAnalyzing abnormal markers (Low Hb, High WBC): {abnormal_markers_1}")
    abnormal_analysis_1 = analyze_health_markers(abnormal_markers_1)
    print("Analysis Result:")
    for obs in abnormal_analysis_1["observations"]:
        print(f"  - {obs}")
    print(f"Summary: {abnormal_analysis_1['summary']}")
    print(f"LLM Explanation: {abnormal_analysis_1.get('llm_explanation')}")

    # Test Case 3: Missing marker value, High Platelets
    abnormal_markers_2 = {"hemoglobin": 13.0, "wbc": None, "platelets": 500.0, "rbc": 4.8}
    print(f"\nAnalyzing abnormal markers (Missing WBC, High Platelets): {abnormal_markers_2}")
    abnormal_analysis_2 = analyze_health_markers(abnormal_markers_2)
    print("Analysis Result:")
    for obs in abnormal_analysis_2["observations"]:
        print(f"  - {obs}")
    print(f"Summary: {abnormal_analysis_2['summary']}")
    print(f"LLM Explanation: {abnormal_analysis_2.get('llm_explanation')}")

    print("\nAll analyze_health_markers test cases completed.")

    # Restore original environment variables if they were set
    if original_openrouter_key is not None:
        os.environ["OPENROUTER_API_KEY"] = original_openrouter_key
    else:
        del os.environ["OPENROUTER_API_KEY"]
    if original_openrouter_model is not None:
        os.environ["OPENROUTER_MODEL"] = original_openrouter_model
    else:
        del os.environ["OPENROUTER_MODEL"]
    if original_openrouter_base_url is not None:
        os.environ["OPENROUTER_BASE_URL"] = original_openrouter_base_url
    else:
        del os.environ["OPENROUTER_BASE_URL"]
