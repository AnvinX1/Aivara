
import os
import sys
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from services.ollama_service import call_ollama_llm, get_model_for_explanation
import config

def generate_forecast(
    patient_id: str,
    current_report: Dict[str, Any],
    historical_reports: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate health forecast using Ollama LLM (llama3.2) based on patient's historical data.
    
    Args:
        patient_id: Patient ID
        current_report: Current report data with health markers
        historical_reports: List of historical reports (sorted by date, oldest first)
    
    Returns:
        Dictionary with forecast data including trends, risks, recommendations, and confidence
    """
    
    # Build historical trends data
    trends_data = []
    for report in historical_reports:
        report_date = report.get("upload_timestamp", "")
        if isinstance(report_date, datetime):
            report_date = report_date.strftime("%Y-%m-%d")
        elif isinstance(report_date, str):
            report_date = report_date[:10]  # Extract date part
        
        trends_data.append({
            "date": report_date,
            "hemoglobin": report.get("hemoglobin"),
            "wbc": report.get("wbc"),
            "platelets": report.get("platelets"),
            "rbc": report.get("rbc"),
        })
    
    # Get current values
    current_values = {
        "hemoglobin": current_report.get("hemoglobin"),
        "wbc": current_report.get("wbc"),
        "platelets": current_report.get("platelets"),
        "rbc": current_report.get("rbc"),
    }
    
    # Parse AI analysis if available
    ai_analysis = ""
    if current_report.get("analysis_result_json"):
        try:
            analysis = json.loads(current_report.get("analysis_result_json", "{}"))
            ai_analysis = analysis.get("llm_explanation", "") or analysis.get("summary", "")
        except:
            ai_analysis = ""
    
    # Build prompt for LLM
    prompt = f"""You are a medical AI assistant specializing in health trend analysis and forecasting.

Based on the following patient health marker history and current report, provide a comprehensive health forecast.

PATIENT HISTORY:
"""
    
    if trends_data:
        prompt += "Historical Health Markers:\n"
        for trend in trends_data:
            prompt += f"  Date: {trend['date']}\n"
            if trend.get("hemoglobin"): prompt += f"    Hemoglobin: {trend['hemoglobin']} g/dL\n"
            if trend.get("wbc"): prompt += f"    WBC: {trend['wbc']} x10³/μL\n"
            if trend.get("platelets"): prompt += f"    Platelets: {trend['platelets']} x10³/μL\n"
            if trend.get("rbc"): prompt += f"    RBC: {trend['rbc']} x10⁶/μL\n"
            prompt += "\n"
    else:
        prompt += "No historical data available.\n\n"
    
    prompt += f"""CURRENT STATUS:
  Hemoglobin: {current_values.get('hemoglobin', 'N/A')} g/dL (Normal: 13.5-17.5)
  WBC: {current_values.get('wbc', 'N/A')} x10³/μL (Normal: 4.5-11.0)
  Platelets: {current_values.get('platelets', 'N/A')} x10³/μL (Normal: 150-450)
  RBC: {current_values.get('rbc', 'N/A')} x10⁶/μL (Normal: 4.32-5.72)

AI ANALYSIS SUMMARY:
{ai_analysis if ai_analysis else "No AI analysis available"}

Please provide a structured forecast in the following JSON format:
{{
  "trend_analysis": {{
    "hemoglobin_trend": "improving/stable/declining" with explanation,
    "wbc_trend": "improving/stable/declining" with explanation,
    "platelets_trend": "improving/stable/declining" with explanation,
    "rbc_trend": "improving/stable/declining" with explanation
  }},
  "future_predictions": {{
    "next_3_months": "What to expect in next 3 months",
    "next_6_months": "What to expect in next 6 months",
    "key_concerns": ["List of potential concerns"]
  }},
  "risk_assessment": {{
    "overall_risk": "low/medium/high",
    "risk_factors": ["List of risk factors identified"],
    "risk_explanation": "Detailed explanation of risk assessment"
  }},
  "recommendations": [
    "Specific recommendation 1",
    "Specific recommendation 2",
    ...
  ],
  "confidence_score": 0.0-1.0 (explain your confidence level)
}}

Provide the forecast as valid JSON only, no additional text before or after.
"""
    
    try:
        model = get_model_for_explanation()  # Use llama3.2 for forecasting
        forecast_text = call_ollama_llm(prompt, model)
        
        if not forecast_text:
            return {
                "forecast_data": json.dumps({
                    "error": "Failed to generate forecast. LLM service unavailable.",
                    "trend_analysis": {},
                    "future_predictions": {},
                    "risk_assessment": {"overall_risk": "unknown"},
                    "recommendations": [],
                    "confidence_score": 0.0
                }),
                "confidence_score": 0.0
            }
        
        # Try to extract JSON from response
        forecast_json = None
        try:
            # Look for JSON in the response
            start_idx = forecast_text.find('{')
            end_idx = forecast_text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = forecast_text[start_idx:end_idx]
                forecast_json = json.loads(json_str)
            else:
                forecast_json = json.loads(forecast_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, create a structured response from text
            forecast_json = {
                "raw_response": forecast_text,
                "trend_analysis": {
                    "note": "Unable to parse structured trends from LLM response"
                },
                "future_predictions": {
                    "next_3_months": "See raw_response for details",
                    "next_6_months": "See raw_response for details",
                    "key_concerns": []
                },
                "risk_assessment": {
                    "overall_risk": "unknown",
                    "risk_factors": [],
                    "risk_explanation": forecast_text
                },
                "recommendations": [],
                "confidence_score": 0.5  # Medium confidence if parsing failed
            }
        
        # Extract confidence score
        confidence = forecast_json.get("confidence_score", 0.5)
        if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
            confidence = 0.5  # Default to medium confidence
        
        return {
            "forecast_data": json.dumps(forecast_json),
            "confidence_score": float(confidence)
        }
        
    except Exception as e:
        print(f"Error generating forecast: {e}")
        return {
            "forecast_data": json.dumps({
                "error": f"Forecast generation failed: {str(e)}",
                "trend_analysis": {},
                "future_predictions": {},
                "risk_assessment": {"overall_risk": "unknown"},
                "recommendations": [],
                "confidence_score": 0.0
            }),
            "confidence_score": 0.0
        }

