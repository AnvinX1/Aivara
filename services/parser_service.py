
import re
from typing import Dict, Any

def parse_health_markers(text: str) -> Dict[str, Any]:
    """
    Parses a given text to extract specific health markers.
    Handles variations in labeling and units.
    """
    markers = {
        "hemoglobin": None,
        "wbc": None,
        "platelets": None,
        "rbc": None,
    }

    # Normalize text to lower case for easier matching and remove extra spaces
    normalized_text = text.lower().replace('\n', ' ').strip()
    normalized_text = re.sub(r'\s+', ' ', normalized_text)

    # Hemoglobin
    # Examples: hemoglobin 14.5 g/dl, hb 12.1, hgb: 13.0
    hb_patterns = [
        r'hemoglobin\W*(\d+\.?\d*)[^\d]*g/?[dl|l]',
        r'hb\W*(\d+\.?\d*)',
        r'hgb\W*(\d+\.?\d*)'
    ]
    for pattern in hb_patterns:
        match = re.search(pattern, normalized_text)
        if match:
            markers['hemoglobin'] = float(match.group(1))
            break

    # WBC (White Blood Cell Count)
    # Examples: wbc 7.2 x10^3/uL, white blood cell 8.0
    wbc_patterns = [
        r'wbc\W*(\d+\.?\d*)',
        r'white blood cells?\W*(\d+\.?\d*)'
    ]
    for pattern in wbc_patterns:
        match = re.search(pattern, normalized_text)
        if match:
            markers['wbc'] = float(match.group(1))
            break

    # Platelets
    # Examples: platelets 250 x10^3/uL, plts 280
    platelets_patterns = [
        r'platelets?\W*(\d+\.?\d*)',
        r'plts?\W*(\d+\.?\d*)'
    ]
    for pattern in platelets_patterns:
        match = re.search(pattern, normalized_text)
        if match:
            markers['platelets'] = float(match.group(1))
            break

    # RBC (Red Blood Cell Count)
    # Examples: rbc 5.0 x10^6/uL, red blood cell 4.8
    rbc_patterns = [
        r'rbc\W*(\d+\.?\d*)',
        r'red blood cells?\W*(\d+\.?\d*)'
    ]
    for pattern in rbc_patterns:
        match = re.search(pattern, normalized_text)
        if match:
            markers['rbc'] = float(match.group(1))
            break

    return markers

if __name__ == '__main__':
    print("--- Testing parse_health_markers ---")

    # Test cases
    test_text_1 = "Patient Report: Hemoglobin 14.2 g/dL, WBC 7.5 x10^3/uL, Platelets: 280, RBC 4.9"
    result_1 = parse_health_markers(test_text_1)
    print(f"Test Case 1: {test_text_1}\nResult: {result_1}")
    assert result_1 == {'hemoglobin': 14.2, 'wbc': 7.5, 'platelets': 280.0, 'rbc': 4.9}

    test_text_2 = "Labs: HGB: 12.0, White Blood Cell 6.8, PLTS 200, Red Blood Cells 4.5"
    result_2 = parse_health_markers(test_text_2)
    print(f"\nTest Case 2: {test_text_2}\nResult: {result_2}")
    assert result_2 == {'hemoglobin': 12.0, 'wbc': 6.8, 'platelets': 200.0, 'rbc': 4.5}

    test_text_3 = "Only some markers: Hemoglobin 13.5, WBC: 9.1"
    result_3 = parse_health_markers(test_text_3)
    print(f"\nTest Case 3: {test_text_3}\nResult: {result_3}")
    assert result_3 == {'hemoglobin': 13.5, 'wbc': 9.1, 'platelets': None, 'rbc': None}

    test_text_4 = "No markers in this text."
    result_4 = parse_health_markers(test_text_4)
    print(f"\nTest Case 4: {test_text_4}\nResult: {result_4}")
    assert result_4 == {'hemoglobin': None, 'wbc': None, 'platelets': None, 'rbc': None}

    print("All test cases passed!")
