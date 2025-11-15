import streamlit as st
import requests
import json
from datetime import datetime
import os

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

def get_report_by_id(report_id):
    """Get a specific report by ID"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/reports/{report_id}",
            headers=get_headers()
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get("detail", "Failed to fetch report")
    except Exception as e:
        return False, f"Error: {str(e)}"

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
    # User is logged in
    st.sidebar.success(f"Logged in as: {st.session_state.user_email}")
    if st.sidebar.button("Logout"):
        st.session_state.access_token = None
        st.session_state.user_email = None
        st.session_state.user_id = None
        st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload Report", "📋 My Reports", "📊 Report Details"])
    
    with tab1:
        st.header("Upload Medical Report")
        st.markdown("Upload a PDF or image file containing your medical report for analysis.")
        
        report_name = st.text_input("Report Name", placeholder="e.g., Blood Test Report - January 2024")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "png", "jpg", "jpeg", "tiff", "bmp", "gif"],
            help="Supported formats: PDF, PNG, JPG, JPEG, TIFF, BMP, GIF"
        )
        
        if st.button("Upload Report", type="primary"):
            if report_name and uploaded_file:
                with st.spinner("Uploading and analyzing report..."):
                    success, result = upload_report(report_name, uploaded_file)
                    if success:
                        st.success("Report uploaded and analyzed successfully!")
                        st.json(result)
                    else:
                        error_msg = result if isinstance(result, str) else str(result)
                        st.error(f"Upload failed: {error_msg}")
                        if "pdfplumber" in error_msg.lower() or "pytesseract" in error_msg.lower() or "ocr" in error_msg.lower():
                            st.info("ℹ️ Note: OCR functionality requires additional dependencies. PDF processing needs 'pdfplumber' and image processing needs 'pytesseract' and Tesseract OCR installed.")
            else:
                st.warning("Please provide a report name and upload a file")
    
    with tab2:
        st.header("My Reports")
        
        if st.button("Refresh Reports"):
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
                
                df = st.dataframe(report_data, use_container_width=True)
                
                # Allow user to select a report to view details
                report_ids = [r["id"] for r in reports]
                selected_report_id = st.selectbox(
                    "Select a report to view details:",
                    options=report_ids,
                    format_func=lambda x: f"Report #{x}"
                )
                
                if selected_report_id:
                    st.session_state.selected_report_id = selected_report_id
            else:
                st.info("No reports found. Upload a report to get started.")
        else:
            st.error(f"Failed to fetch reports: {reports}")
    
    with tab3:
        st.header("Report Details")
        
        if "selected_report_id" in st.session_state:
            report_id = st.session_state.selected_report_id
        else:
            report_id = st.number_input("Enter Report ID", min_value=1, value=1)
        
        if st.button("Load Report Details"):
            with st.spinner("Loading report details..."):
                success, report = get_report_by_id(report_id)
                if success:
                    st.success("Report loaded successfully!")
                    
                    # Display report information
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Report Information")
                        st.write(f"**Report ID:** {report['id']}")
                        st.write(f"**Report Name:** {report['report_name']}")
                        st.write(f"**Created At:** {report.get('upload_timestamp', report.get('created_at', 'N/A'))}")
                        st.write(f"**File Path:** {report.get('file_path', 'N/A')}")
                    
                    with col2:
                        st.subheader("Health Markers")
                        st.metric("Hemoglobin", report.get("hemoglobin", "N/A"))
                        st.metric("WBC", report.get("wbc", "N/A"))
                        st.metric("Platelets", report.get("platelets", "N/A"))
                        st.metric("RBC", report.get("rbc", "N/A"))
                    
                    # Display analysis results
                    if report.get("analysis_result_json"):
                        st.subheader("AI Analysis Results")
                        try:
                            analysis = json.loads(report["analysis_result_json"])
                            st.json(analysis)
                        except:
                            st.text(report["analysis_result_json"])
                    
                    # Display doctor review if available
                    if report.get("doctor_review"):
                        st.subheader("Doctor Review")
                        st.write(f"**Review Status:** {report.get('review_status', 'N/A')}")
                        st.write(f"**Review Notes:** {report.get('doctor_review', 'N/A')}")
                        if report.get("reviewed_at"):
                            st.write(f"**Reviewed At:** {report['reviewed_at']}")
                else:
                    st.error(f"Failed to load report: {report}")

