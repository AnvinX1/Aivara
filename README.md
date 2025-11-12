
# Aivara Backend API

## Project Overview

The Aivara Backend is the core engine for the Aivara healthcare analytics platform. It provides a robust and secure set of API endpoints to manage user and doctor accounts, facilitate medical report uploads, perform advanced OCR and AI-driven health marker analysis, store and retrieve data, and enable doctor reviews. Built with speed and scalability in mind, it serves as the foundation for the Aivara frontend application.

## Technology Stack

-   **FastAPI**: 🚀 A modern, fast (high-performance) web framework for building APIs with Python 3.8+ based on standard Python type hints.
-   **SQLAlchemy**: 🐍 The Python SQL Toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
-   **Pydantic**: ✅ Data validation and settings management using Python type hints; used for defining request and response schemas.
-   **python-jose**: 🔒 Provides secure JWT (JSON Web Token) handling for authentication.
-   **passlib**: 🔑 A comprehensive password hashing framework for Python, used here with `bcrypt` for secure password storage.
-   **Pillow**: 🖼️ The friendly PIL (Python Imaging Library) fork, used for image processing during OCR.
-   **pytesseract**: 🤖 Python wrapper for Google's Tesseract-OCR Engine, enabling text extraction from images.
-   **pdfplumber**: 📄 Pluck data from PDFs. Works with both text and scanned PDFs.
-   **python-multipart**: 📤 Library for handling `multipart/form-data` uploads, essential for file uploads in FastAPI.

## Key Features

-   **User & Doctor Authentication**: Secure registration and login functionalities using JWT for both patients and medical professionals.
-   **Medical Report OCR & Parsing**: Automated text extraction from uploaded PDF and image-based medical reports, powered by `pdfplumber` and `pytesseract`.
-   **AI-Driven Health Marker Analysis**: Intelligent extraction and rule-based analysis of key health markers (Hemoglobin, WBC, Platelets, RBC) from parsed reports.
-   **Report Storage**: Secure storage of uploaded medical reports and their extracted data.
-   **Doctor Review System**: Functionality for doctors to review analyzed reports, add professional notes, and update review statuses.
-   **ABHA Integration (Mock)**: A placeholder endpoint for future integration with India's Ayushman Bharat Health Account.

## Local Setup

To run the Aivara backend locally, follow these steps:

1.  **Navigate to the Backend Directory**:

    ```bash
    cd /content/aivara_app/aivara-backend
    ```

2.  **Install Python Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Tesseract OCR (System Dependency)**:
    This is required for image-based OCR. For Ubuntu/Debian-based systems:

    ```bash
    sudo apt-get update && sudo apt-get install -y tesseract-ocr
    ```

4.  **Run the Backend Server**:
    The `run.sh` script handles killing any existing process, removing the old database (for a clean start), and launching the Uvicorn server.

    ```bash
    bash run.sh
    ```

    The server will start in the background on `http://0.0.0.0:8000`. You can view API documentation at `http://localhost:8000/docs`.

## API Endpoints

Here are the main API endpoints provided by the backend:

| Endpoint                                   | Method | Description                                                               |
| :----------------------------------------- | :----- | :------------------------------------------------------------------------ |
| `/auth/register`                           | `POST`   | Register a new user.                                                      |
| `/auth/token`                              | `POST`   | Obtain an access token for user login.                                    |
| `/reports/upload`                          | `POST`   | Upload a medical report (PDF/image) for OCR, parsing, and AI analysis.  |
| `/reports/`                                | `GET`    | Retrieve all reports for the authenticated user.                          |
| `/reports/{report_id}`                     | `GET`    | Retrieve a specific report by ID for the authenticated user.              |
| `/ai/analyze/{report_id}`                  | `POST`   | Trigger re-analysis of a specific report by the AI engine.                |
| `/doctor/register_doctor`                  | `POST`   | Register a new doctor.                                                    |
| `/doctor/token_doctor`                     | `POST`   | Obtain an access token for doctor login.                                  |
| `/doctor/reports/{report_id}/review`       | `POST`   | Submit or update a doctor's review for a specific report.                 |
| `/abha/sync`                               | `POST`   | Mock endpoint for ABHA (Ayushman Bharat Health Account) synchronization.  |

## Production Deployment

The application can be containerized using Docker for production deployment. A `Dockerfile` is provided in this directory with the following structure:

-   **Base Image**: `python:3.12-slim-buster` for a lightweight Python environment.
-   **Dependencies**: `requirements.txt` is copied and `pip install` is run to install all Python packages.
-   **Application Code**: The entire backend project is copied into the `/app` directory within the container.
-   **Port Exposure**: Port `8000` is exposed, as this is where Uvicorn serves the FastAPI application.
-   **Startup Command**: `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]` runs the FastAPI application using Uvicorn.

For production, ensure environment variables like `SECRET_KEY` and `DATABASE_URL` are properly configured (e.g., via Docker Compose, Kubernetes secrets, or your deployment platform's environment variable management). The `DATABASE_URL` should point to a persistent database solution (e.g., PostgreSQL, MySQL) rather than a local SQLite file.
