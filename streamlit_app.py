import streamlit as st
import requests
import json
from datetime import datetime
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Backend API URL
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

def get_headers():
    """Get headers with authentication token if available"""
    headers = {}
    if st.session_state.access_token:
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
    return headers

def register_user(email, password, full_name):
    """Register a new user"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={
                "email": email,
                "password": password,
                "full_name": full_name
            },
            timeout=10
        )
        if response.status_code == 201:
            return True, "Registration successful! Please login."
        else:
            # Try to parse JSON, but handle non-JSON responses
            try:
                error_detail = response.json().get("detail", "Registration failed")
            except (ValueError, requests.exceptions.JSONDecodeError):
                # If response is not JSON, use the text content
                error_detail = response.text if response.text else f"Registration failed with status {response.status_code}"
            return False, error_detail
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to backend server. Please ensure the backend is running on http://localhost:8000"
    except requests.exceptions.Timeout:
        return False, "Request timed out. Please try again."
    except Exception as e:
        return False, f"Error: {str(e)}"

def login_user(email, password):
    """Login user and get access token"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/token",
            data={
                "username": email,
                "password": password
            },
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.access_token = data["access_token"]
            st.session_state.user_email = email
            return True, "Login successful!"
        else:
            # Try to parse JSON, but handle non-JSON responses
            try:
                error_detail = response.json().get("detail", "Login failed")
            except (ValueError, requests.exceptions.JSONDecodeError):
                error_detail = response.text if response.text else f"Login failed with status {response.status_code}"
            return False, error_detail
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to backend server. Please ensure the backend is running on http://localhost:8000"
    except requests.exceptions.Timeout:
        return False, "Request timed out. Please try again."
    except Exception as e:
        return False, f"Error: {str(e)}"

def upload_report(report_name, file):
    """Upload a medical report"""
    try:
        files = {"file": (file.name, file, file.type)}
        data = {"report_name": report_name}
        response = requests.post(
            f"{API_BASE_URL}/reports/upload",
            headers=get_headers(),
            files=files,
            data=data
        )
        if response.status_code == 201:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Upload failed")
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_reports():
    """Get all reports for the current user"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/reports/",
            headers=get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Failed to fetch reports")
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_report_by_id(report_id, include_extracted_text=False):
    """Get a specific report by ID"""
    try:
        params = {"include_extracted_text": include_extracted_text}
        response = requests.get(
            f"{API_BASE_URL}/reports/{report_id}",
            headers=get_headers(),
            params=params
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Failed to fetch report")
    except Exception as e:
        return False, f"Error: {str(e)}"

def reanalyze_report(report_id):
    """Reanalyze a report"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/ai/analyze/{report_id}",
            headers=get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Failed to reanalyze report")
    except Exception as e:
        return False, f"Error: {e}"

def get_medicine_suggestions(report_id):
    """Get medicine suggestions for a report"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/reports/{report_id}/medicine-suggestions",
            headers=get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Failed to get medicine suggestions")
    except Exception as e:
        return False, f"Error: {e}"

def get_women_health_suggestions(report_id):
    """Get women's health suggestions for a report"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/reports/{report_id}/women-health",
            headers=get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Failed to get women's health suggestions")
    except Exception as e:
        return False, f"Error: {e}"

# Main App
st.set_page_config(page_title="Aivara Healthcare Analytics", page_icon="🏥", layout="wide")

st.title("🏥 Aivara Healthcare Analytics Platform")
st.markdown("### Medical Report Analysis & Management")

# Check if backend is running
try:
    response = requests.get(f"{API_BASE_URL}/docs", timeout=2)
    backend_status = "🟢 Online"
except requests.exceptions.ConnectionError:
    backend_status = "🔴 Offline"
    st.error("⚠️ Backend server is not running. Please start the backend server first.")
    st.info("To start the backend, run: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`")
    st.stop()
except Exception as e:
    backend_status = "🟡 Unknown"
    st.warning(f"⚠️ Could not verify backend status: {str(e)}")

st.sidebar.markdown(f"**Backend Status:** {backend_status}")

# Authentication Section
if st.session_state.access_token is None:
    st.sidebar.header("Authentication")
    tab1, tab2 = st.sidebar.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", type="primary"):
            if login_email and login_password:
                success, message = login_user(login_email, login_password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please enter both email and password")
    
    with tab2:
        st.subheader("Register")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_name = st.text_input("Full Name", key="reg_name")
        if st.button("Register", type="primary"):
            if reg_email and reg_password and reg_name:
                if len(reg_password) < 8:
                    st.error("Password must be at least 8 characters long")
                else:
                    success, message = register_user(reg_email, reg_password, reg_name)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            else:
                st.warning("Please fill in all fields")
else:
    # User is logged in - Single Page Layout
    st.sidebar.success(f"Logged in as: {st.session_state.user_email}")
    if st.sidebar.button("Logout"):
        st.session_state.access_token = None
        st.session_state.user_email = None
        st.session_state.user_id = None
        st.rerun()
    
    # ==================== SECTION 1: UPLOAD REPORT ====================
    st.header("📤 Upload Medical Report")
    st.markdown("Upload a PDF or image file containing your medical report for analysis.")
    
    upload_col1, upload_col2 = st.columns([2, 1])
    with upload_col1:
        report_name = st.text_input("Report Name", placeholder="e.g., Blood Test Report - January 2024", key="upload_report_name")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "png", "jpg", "jpeg", "tiff", "bmp", "gif"],
            help="Supported formats: PDF, PNG, JPG, JPEG, TIFF, BMP, GIF",
            key="upload_file"
        )
    
    with upload_col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        upload_btn = st.button("📤 Upload & Analyze", type="primary", use_container_width=True)  # Note: use_container_width still works for buttons
    
    if upload_btn:
        if report_name and uploaded_file:
            with st.spinner("Uploading and analyzing report with AI models..."):
                success, result = upload_report(report_name, uploaded_file)
                if success:
                    st.success("Report uploaded and analyzed successfully!")
                    # Auto-select the uploaded report
                    if "id" in result:
                        st.session_state.selected_report_id = result["id"]
                        st.rerun()
                else:
                    error_msg = result if isinstance(result, str) else str(result)
                    st.error(f"Upload failed: {error_msg}")
                    if "pdfplumber" in error_msg.lower() or "pytesseract" in error_msg.lower() or "ocr" in error_msg.lower():
                        st.info("ℹ️ Note: OCR functionality requires additional dependencies. PDF processing needs 'pdfplumber' and image processing needs 'pytesseract' and Tesseract OCR installed.")
        else:
            st.warning("Please provide a report name and upload a file")
    
    st.divider()
    
    # ==================== SECTION 2: MY REPORTS LIST ====================
    st.header("📋 My Medical Reports")
    
    refresh_col1, refresh_col2 = st.columns([1, 4])
    with refresh_col1:
        if st.button("🔄 Refresh", use_container_width=True):  # Note: use_container_width still works for buttons
            st.rerun()
    
    success, reports = get_reports()
    if success:
        if reports:
            st.success(f"Found {len(reports)} report(s)")
            
            # Display reports in a table
            report_data = []
            for report in reports:
                report_data.append({
                    "ID": report["id"],
                    "Report Name": report["report_name"],
                    "Created At": report.get("upload_timestamp", report.get("created_at", "N/A")),
                    "Hemoglobin": report.get("hemoglobin", "N/A"),
                    "WBC": report.get("wbc", "N/A"),
                    "Platelets": report.get("platelets", "N/A"),
                    "RBC": report.get("rbc", "N/A"),
                })
            
            st.dataframe(report_data, width='stretch', height=200)
            
            # Allow user to select a report to view details
            report_ids = [r["id"] for r in reports]
            if "selected_report_id" not in st.session_state or st.session_state.selected_report_id not in report_ids:
                st.session_state.selected_report_id = report_ids[0] if report_ids else None
            
            selected_report_id = st.selectbox(
                "Select a report to view detailed analysis:",
                options=report_ids,
                format_func=lambda x: f"Report #{x} - {next((r['report_name'] for r in reports if r['id'] == x), 'Unknown')}",
                key="report_selector",
                index=report_ids.index(st.session_state.selected_report_id) if st.session_state.selected_report_id in report_ids else 0
            )
            
            if selected_report_id:
                st.session_state.selected_report_id = selected_report_id
        else:
            st.info("No reports found. Upload a report to get started.")
    else:
        st.error(f"Failed to fetch reports: {reports}")
    
    st.divider()
    
    # ==================== SECTION 3: REPORT DETAILS ====================
    if "selected_report_id" in st.session_state and st.session_state.selected_report_id:
        report_id = st.session_state.selected_report_id
        
        # Load report details if not in session state
        if "current_report" not in st.session_state or st.session_state.current_report.get("id") != report_id:
            with st.spinner("Loading report details..."):
                success, report = get_report_by_id(report_id)
                if success:
                    st.session_state.current_report = report
        
        if "current_report" in st.session_state and st.session_state.current_report.get("id") == report_id:
            report = st.session_state.current_report
            
            st.header(f"📊 Report Details - {report['report_name']}")
            
            # Action buttons
            action_col1, action_col2, action_col3 = st.columns(3)
            with action_col1:
                if st.button("🔄 Reload Report", use_container_width=True):  # Note: use_container_width still works for buttons
                    with st.spinner("Reloading report..."):
                        success, report = get_report_by_id(report_id)
                        if success:
                            st.session_state.current_report = report
                            st.rerun()
            
            with action_col2:
                if st.button("🔄 Reanalyze with AI", use_container_width=True):  # Note: use_container_width still works for buttons
                    with st.spinner("Reanalyzing report with updated AI models..."):
                        success, report = reanalyze_report(report_id)
                        if success:
                            st.session_state.current_report = report
                            st.success("Report reanalyzed successfully!")
                            st.rerun()
                        else:
                            st.error(f"Failed to reanalyze: {report}")
            
            with action_col3:
                if st.button("🔍 Load Extracted Text", use_container_width=True):  # Note: use_container_width still works for buttons
                    with st.spinner("Extracting text..."):
                        success_text, report_text = get_report_by_id(report_id, include_extracted_text=True)
                        if success_text and report_text.get("extracted_text"):
                            st.session_state.extracted_text = report_text["extracted_text"]
                        else:
                            st.error("Failed to extract text.")
            
            # Report Information and Health Markers
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.subheader("📄 Report Information")
                st.write(f"**Report ID:** {report['id']}")
                st.write(f"**Report Name:** {report['report_name']}")
                st.write(f"**Created At:** {report.get('upload_timestamp', report.get('created_at', 'N/A'))}")
                st.write(f"**File Path:** {report.get('file_path', 'N/A')}")
            
            with info_col2:
                st.subheader("🔬 Health Markers")
                hb = report.get("hemoglobin")
                wbc = report.get("wbc")
                platelets = report.get("platelets")
                rbc = report.get("rbc")
                
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric("Hemoglobin", f"{hb:.2f}" if isinstance(hb, (int, float)) else "N/A")
                    st.metric("WBC", f"{wbc:.2f}" if isinstance(wbc, (int, float)) else "N/A")
                with metric_col2:
                    st.metric("Platelets", f"{platelets:.0f}" if isinstance(platelets, (int, float)) else "N/A")
                    st.metric("RBC", f"{rbc:.2f}" if isinstance(rbc, (int, float)) else "N/A")
            
            # Health Markers Visualization
            markers_data = {
                "Hemoglobin": report.get("hemoglobin"),
                "WBC": report.get("wbc"),
                "Platelets": report.get("platelets") / 100 if isinstance(report.get("platelets"), (int, float)) else None,
                "RBC": report.get("rbc"),
            }
            
            valid_markers = {k: v for k, v in markers_data.items() if v is not None}
            
            if valid_markers:
                st.subheader("📊 Health Markers Visualization")
                
                normal_ranges = {
                    "Hemoglobin": {"min": 12.0, "max": 17.5},
                    "WBC": {"min": 4.0, "max": 11.0},
                    "Platelets": {"min": 1.5, "max": 4.5},
                    "RBC": {"min": 4.5, "max": 5.9},
                }
                
                fig = go.Figure()
                marker_names = list(valid_markers.keys())
                marker_values = list(valid_markers.values())
                
                colors = []
                for name in marker_names:
                    value = valid_markers[name]
                    if name in normal_ranges:
                        norm_range = normal_ranges[name]
                        if norm_range["min"] <= value <= norm_range["max"]:
                            colors.append("#4CAF50")
                        elif value < norm_range["min"]:
                            colors.append("#FF9800")
                        else:
                            colors.append("#F44336")
                    else:
                        colors.append("#2196F3")
                
                fig.add_trace(go.Bar(
                    x=marker_names,
                    y=marker_values,
                    marker_color=colors,
                    text=[f"{v:.2f}" if isinstance(v, float) else str(v) for v in marker_values],
                    textposition="outside",
                    name="Current Values"
                ))
                
                for i, name in enumerate(marker_names):
                    if name in normal_ranges:
                        norm_range = normal_ranges[name]
                        fig.add_shape(
                            type="rect",
                            x0=i-0.4, x1=i+0.4,
                            y0=norm_range["min"], y1=norm_range["max"],
                            fillcolor="rgba(76, 175, 80, 0.2)",
                            line=dict(width=0),
                            layer="below"
                        )
                
                fig.update_layout(
                    title="Health Markers vs Normal Ranges",
                    xaxis_title="Health Markers",
                    yaxis_title="Values",
                    height=400,
                    showlegend=False,
                    xaxis=dict(tickangle=-45)
                )
                
                st.plotly_chart(fig, width='stretch')
                
                legend_col1, legend_col2, legend_col3 = st.columns(3)
                with legend_col1:
                    st.markdown("🟢 **Normal Range**")
                with legend_col2:
                    st.markdown("🟠 **Below Normal**")
                with legend_col3:
                    st.markdown("🔴 **Above Normal**")
            
            st.divider()
            
            # AI Analysis Results
            if report.get("analysis_result_json"):
                st.subheader("🤖 AI Analysis Results")
                try:
                    analysis = json.loads(report["analysis_result_json"])
                    
                    if "summary" in analysis:
                        st.info(f"**Summary:** {analysis['summary']}")
                    
                    if "observations" in analysis and analysis["observations"]:
                        st.write("**Observations:**")
                        for obs in analysis["observations"]:
                            if "Low" in obs:
                                st.warning(f"⚠️ {obs}")
                            elif "High" in obs:
                                st.error(f"🔴 {obs}")
                            elif "Normal" in obs:
                                st.success(f"✅ {obs}")
                            else:
                                st.write(f"• {obs}")
                    
                    # General AI Explanation (llama3.2)
                    if "llm_explanation" in analysis and analysis["llm_explanation"]:
                        with st.expander("💡 General Health Explanation (llama3.2)", expanded=True):
                            st.write(analysis["llm_explanation"])
                    
                    # Report Reading Insights (qwen3-vl:2b)
                    if "report_reading_insights" in analysis:
                        with st.expander("📖 Report Reading Insights (qwen3-vl:2b)", expanded=False):
                            st.write(analysis["report_reading_insights"])
                    else:
                        # Generate report reading insights if not available
                        with st.expander("📖 Report Reading Insights (qwen3-vl:2b)", expanded=False):
                            if st.button("Generate Report Reading", key="gen_report_reading"):
                                with st.spinner("Analyzing report with qwen3-vl:2b..."):
                                    # This will be handled by the backend endpoint
                                    st.info("Report reading analysis will be generated. Please reanalyze the report.")
                    
                    with st.expander("📄 Full Analysis JSON", expanded=False):
                        st.json(analysis)
                except Exception as e:
                    st.text(report["analysis_result_json"])
                    st.error(f"Error parsing analysis: {e}")
            
            st.divider()
            
            # Medicine Suggestions (medbot)
            st.subheader("💊 Allopathic Medicine Suggestions (medbot)")
            if st.button("Get Medicine Suggestions", key="get_medicine"):
                with st.spinner("Generating medicine suggestions with medbot (10000+ medications)..."):
                    success, suggestions = get_medicine_suggestions(report_id)
                    if success:
                        st.session_state.medicine_suggestions = suggestions.get("suggestions", suggestions)
                        st.success("Medicine suggestions generated!")
                    else:
                        st.error(f"Failed to get suggestions: {suggestions}")
            
            if "medicine_suggestions" in st.session_state:
                st.info(st.session_state.medicine_suggestions)
                st.warning("⚠️ **Important:** These are general suggestions only. Always consult with a qualified healthcare provider before taking any medication.")
            
            st.divider()
            
            # Women's Health Suggestions (edi)
            st.subheader("🌸 Women's Health Suggestions (edi)")
            if st.button("Get Women's Health Suggestions", key="get_women_health"):
                with st.spinner("Generating women's health suggestions with edi..."):
                    success, suggestions = get_women_health_suggestions(report_id)
                    if success:
                        st.session_state.women_health_suggestions = suggestions.get("suggestions", suggestions)
                        st.success("Women's health suggestions generated!")
                    else:
                        st.error(f"Failed to get suggestions: {suggestions}")
            
            if "women_health_suggestions" in st.session_state:
                st.info(st.session_state.women_health_suggestions)
                st.warning("⚠️ **Important:** These are general suggestions only. Always consult with a qualified healthcare provider for personalized advice.")
            
            st.divider()
            
            # Extracted Text (for debugging)
            with st.expander("🔍 Extracted Text (for debugging)", expanded=False):
                if "extracted_text" in st.session_state:
                    st.text_area("OCR Extracted Text", st.session_state.extracted_text, height=200, disabled=True, key="display_extracted_text")
                elif report.get("extracted_text"):
                    st.text_area("OCR Extracted Text", report["extracted_text"], height=200, disabled=True, key="display_extracted_text_from_report")
                else:
                    st.info("Click 'Load Extracted Text' button above to view the OCR-extracted text.")
            
            st.divider()
            
            # Historical Trends
            if success and reports and len(reports) > 1:
                st.subheader("📈 Historical Trends")
                
                trend_data = []
                for r in reports:
                    trend_data.append({
                        "Report ID": r["id"],
                        "Report Name": r["report_name"],
                        "Date": r.get("upload_timestamp", r.get("created_at", ""))[:10] if r.get("upload_timestamp") else "",
                        "Hemoglobin": r.get("hemoglobin"),
                        "WBC": r.get("wbc"),
                        "Platelets": r.get("platelets"),
                        "RBC": r.get("rbc"),
                    })
                
                df_trend = pd.DataFrame(trend_data)
                df_trend = df_trend.sort_values("Date") if "Date" in df_trend.columns else df_trend.sort_values("Report ID")
                
                marker_names_trend = ["Hemoglobin", "WBC", "Platelets", "RBC"]
                valid_trend_data = {}
                
                for marker in marker_names_trend:
                    values = df_trend[marker].dropna().tolist()
                    if values:
                        valid_trend_data[marker] = values
                
                if valid_trend_data:
                    fig_trend = go.Figure()
                    
                    normal_ranges_trend = {
                        "Hemoglobin": {"min": 12.0, "max": 17.5},
                        "WBC": {"min": 4.0, "max": 11.0},
                        "Platelets": {"min": 150, "max": 450},
                        "RBC": {"min": 4.5, "max": 5.9},
                    }
                    
                    for marker, values in valid_trend_data.items():
                        x_vals = list(range(len(values)))
                        fig_trend.add_trace(go.Scatter(
                            x=x_vals,
                            y=values,
                            mode='lines+markers',
                            name=marker,
                            line=dict(width=2)
                        ))
                        
                        if marker in normal_ranges_trend:
                            norm_range = normal_ranges_trend[marker]
                            fig_trend.add_hrect(
                                y0=norm_range["min"],
                                y1=norm_range["max"],
                                fillcolor="rgba(76, 175, 80, 0.1)",
                                layer="below",
                                line_width=0,
                                annotation_text=f"{marker} Normal Range",
                                annotation_position="top left"
                            )
                    
                    fig_trend.update_layout(
                        title="Health Markers Trend Over Time",
                        xaxis_title="Report Number",
                        yaxis_title="Values",
                        height=400,
                        hovermode='x unified',
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    
                    st.plotly_chart(fig_trend, use_container_width=True)

