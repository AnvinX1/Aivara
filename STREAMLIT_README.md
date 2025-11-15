# Aivara Backend - Streamlit Frontend

This directory contains a Streamlit frontend application for testing the Aivara Backend API.

## Quick Start

### 1. Start the Backend Server

The backend server should be running on `http://localhost:8000`. To start it:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or use the provided script:
```bash
bash run.sh
```

### 2. Start the Streamlit Frontend

In a new terminal, run:

```bash
streamlit run streamlit_app.py --server.port 8501
```

The Streamlit app will be available at: `http://localhost:8501`

## Features

The Streamlit frontend provides:

1. **User Authentication**
   - User registration
   - User login with JWT tokens
   - Secure session management

2. **Report Management**
   - Upload medical reports (PDF or image files)
   - View all your reports
   - View detailed report information
   - View AI analysis results

3. **Health Marker Analysis**
   - Automatic extraction of health markers (Hemoglobin, WBC, Platelets, RBC)
   - AI-powered analysis and explanations
   - Visual display of health metrics

## Usage

### Register a New User

1. Go to the "Register" tab in the sidebar
2. Enter your email, password (min 8 characters), and full name
3. Click "Register"

### Login

1. Go to the "Login" tab in the sidebar
2. Enter your email and password
3. Click "Login"

### Upload a Report

1. After logging in, go to the "Upload Report" tab
2. Enter a report name
3. Select a PDF or image file
4. Click "Upload Report"
5. Wait for processing and analysis to complete

### View Reports

1. Go to the "My Reports" tab to see all your reports
2. Select a report from the dropdown to view details
3. Go to the "Report Details" tab to see full information including AI analysis

## Notes

### OCR Dependencies

For full functionality, the following dependencies are recommended:

- **PDF Processing**: `pdfplumber` (usually already installed)
- **Image OCR**: `pytesseract` and Tesseract OCR (system dependency)

If these are not installed, you'll see helpful error messages when trying to upload reports. The backend will still run, but OCR functionality will be limited.

### Backend API

The backend API documentation is available at: `http://localhost:8000/docs`

You can test the API directly using the interactive Swagger UI.

## Troubleshooting

### Backend not starting

- Check if port 8000 is already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check for import errors in the console

### Streamlit not connecting to backend

- Verify the backend is running on port 8000
- Check the backend status indicator in the Streamlit sidebar
- Ensure no firewall is blocking localhost connections

### OCR not working

- Install `pdfplumber` for PDF processing: `pip install pdfplumber`
- Install `pytesseract` for image OCR: `pip install pytesseract`
- Install Tesseract OCR system dependency:
  - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`

## API Endpoints Used

- `POST /auth/register` - User registration
- `POST /auth/token` - User login
- `POST /reports/upload` - Upload medical report
- `GET /reports/` - Get all user reports
- `GET /reports/{report_id}` - Get specific report details

For more endpoints, see the backend API documentation at `http://localhost:8000/docs`.




