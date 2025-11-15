# Aivara Backend API

## Project Overview

**Aivara** is an intelligent healthcare analytics platform designed to transform how patients interact with their medical reports. The backend provides a comprehensive REST API that enables users to upload medical reports, extract health information using OCR, analyze health markers with AI, and receive doctor reviews—all while maintaining a secure, patient-centric approach.

The system leverages **Retrieval-Augmented Generation (RAG)** for intelligent context-aware analysis, combining rule-based health marker detection with LLM-powered explanations. Medical reports are stored both in a traditional SQL database and in a vector store (ChromaDB) for semantic search and retrieval, enabling sophisticated query capabilities across a patient's medical history.

## Architecture Overview

### System Flow (Current Implementation)

1. **User Registration & Authentication**: Patients and doctors register and authenticate using JWT tokens
2. **Report Upload**: Medical reports (PDF/image) are uploaded and stored securely
3. **OCR Processing**: Text is extracted from reports using `pdfplumber` (PDFs) or `pytesseract` (images)
4. **Health Marker Extraction**: Regex-based parser extracts key health markers (Hemoglobin, WBC, Platelets, RBC)
5. **AI Analysis**: 
   - Rule-based analysis compares values against reference ranges
   - LLM (via OpenRouter) generates patient-friendly explanations
6. **Vector Storage**: Extracted text is embedded and stored in ChromaDB for RAG capabilities
7. **Doctor Review**: Doctors can review reports, add notes, and update review status
8. **ABHA Integration**: Mock endpoint ready for future Ayushman Bharat Health Account integration

### Future Vision (Once Completed)

When fully implemented, the system will support:

- **Semantic Search**: Query patient history using natural language (e.g., "What were my blood test results in the last 6 months?")
- **RAG-Enhanced Analysis**: Context-aware analysis using historical report data
- **Multi-Report Comparison**: Track health marker trends over time
- **Intelligent Alerts**: Proactive notifications for concerning health patterns
- **Doctor Dashboard**: Comprehensive interface for medical professionals to manage patient reviews
- **ABHA Integration**: Seamless sync with India's national health records
- **Advanced OCR**: Support for complex report formats and handwritten notes
- **Export Capabilities**: Generate PDF summaries and reports
- **API Analytics**: Usage tracking and performance monitoring

## Technology Stack

### Core Framework
- **FastAPI**: 🚀 Modern, high-performance web framework for building APIs with Python 3.8+ based on standard Python type hints
- **Uvicorn**: ⚡ ASGI server for running FastAPI applications

### Database & Storage
- **SQLAlchemy**: 🐍 Python SQL toolkit and ORM for relational data
- **SQLite**: 💾 Lightweight database for development (easily switchable to PostgreSQL/MySQL for production)
- **ChromaDB**: 🔍 Vector database for storing embeddings and enabling semantic search
- **File System**: 📁 Local storage for uploaded medical reports

### Authentication & Security
- **python-jose**: 🔒 JWT (JSON Web Token) handling for secure authentication
- **bcrypt**: 🔑 Direct password hashing (replaces passlib for better compatibility)
- **OAuth2**: 🔐 Secure token-based authentication flow

### AI & ML
- **OpenRouter API**: 🤖 Access to multiple LLMs (Gemini, GPT-4, etc.) for AI analysis
- **Sentence Transformers**: 📊 Local embedding model (`sentence-transformers/all-MiniLM-L6-v2`) for fallback
- **ChromaDB**: 🧮 Vector similarity search for RAG

### OCR & Document Processing
- **pdfplumber**: 📄 Extract text from PDF documents (both text-based and scanned)
- **pytesseract**: 🔍 Python wrapper for Tesseract OCR engine (for image-based reports)
- **Pillow (PIL)**: 🖼️ Image processing library for OCR preprocessing

### Data Validation
- **Pydantic**: ✅ Data validation and settings management using Python type hints
- **email-validator**: 📧 Email validation for user registration

### Additional
- **python-multipart**: 📤 Handle file uploads (multipart/form-data)
- **requests**: 🌐 HTTP client for API calls to OpenRouter
- **numpy**: 🔢 Numerical operations for embeddings

## Project Structure

```
aivara-backend/
│
├── app/                          # FastAPI application entry point
│   ├── __init__.py
│   ├── main.py                   # FastAPI app initialization, startup events
│   └── services/                 # Application-level services
│       ├── embeddings_service.py # Embedding generation (OpenRouter API + SentenceTransformers fallback)
│       └── vector_store.py       # ChromaDB integration for RAG (upsert, search, patient_context)
│
├── api/                          # API routing layer
│   ├── __init__.py
│   ├── router.py                 # Main API router that includes all route modules
│   └── routes/                   # Individual route modules
│       ├── __init__.py
│       ├── auth.py               # User authentication (register, login)
│       ├── reports.py            # Report management (upload, list, get by ID)
│       ├── analysis.py           # AI re-analysis endpoint
│       ├── doctor.py             # Doctor registration, login, report reviews
│       └── abha.py               # ABHA (Ayushman Bharat) integration mock endpoint
│
├── db/                           # Database configuration
│   ├── __init__.py
│   └── database.py               # SQLAlchemy engine, session factory, Base model, table creation
│
├── models/                       # SQLAlchemy ORM models (database schema)
│   ├── __init__.py
│   ├── user.py                   # User model (patients)
│   ├── doctor.py                 # Doctor model (medical professionals)
│   └── report.py                 # Report model (medical reports with health markers)
│
├── schemas/                      # Pydantic models (API request/response validation)
│   ├── __init__.py
│   ├── auth.py                   # Token, TokenData schemas
│   ├── user.py                   # UserCreate, UserResponse, DoctorCreate, DoctorResponse
│   └── report.py                 # ReportCreate, ReportResponse, ReportReview
│
├── services/                     # Business logic services
│   ├── __init__.py
│   ├── ocr_service.py            # Text extraction from PDFs and images
│   ├── parser_service.py         # Health marker extraction using regex patterns
│   ├── ai_engine.py              # Health marker analysis (rule-based + LLM explanations)
│   └── storage_service.py        # File storage management (save uploaded reports)
│
├── dependencies.py               # FastAPI dependencies (get_db, password hashing, JWT, get_current_user)
├── config.py                     # Application configuration (JWT, database, uploads, OpenRouter, ChromaDB)
│
├── uploads/                      # Directory for storing uploaded medical reports (user-specific subdirectories)
├── vectorstore/                  # ChromaDB persistent storage directory (auto-created)
├── aivara.db                     # SQLite database file (auto-created)
│
├── streamlit_app.py              # Streamlit frontend for testing the API
├── start_servers.ps1             # PowerShell script to start both backend and frontend
│
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker containerization configuration
├── run.sh                        # Bash script to start backend server
├── README.md                     # This file
└── STREAMLIT_README.md           # Documentation for Streamlit frontend
```

### Directory Functionality

#### `/app` - Application Entry Point
- **`main.py`**: Initializes the FastAPI application, sets up startup events (database table creation), and includes the API router
- **`services/`**: Application-level services that support the core functionality
  - **`embeddings_service.py`**: Generates text embeddings using OpenRouter API (with fallback to local SentenceTransformer model)
  - **`vector_store.py`**: Manages ChromaDB operations for storing and retrieving embedded document chunks (RAG foundation)

#### `/api` - API Routing Layer
- **`router.py`**: Central router that combines all route modules with appropriate prefixes and tags
- **`routes/`**: Individual route handlers organized by domain
  - **`auth.py`**: User registration and authentication endpoints
  - **`reports.py`**: Medical report upload, retrieval, and management
  - **`analysis.py`**: Re-analysis of existing reports with updated AI analysis
  - **`doctor.py`**: Doctor-specific endpoints (registration, authentication, report reviews)
  - **`abha.py`**: Mock endpoint for future ABHA integration

#### `/db` - Database Layer
- **`database.py`**: SQLAlchemy configuration including engine creation, session factory, declarative base, and automatic table creation

#### `/models` - Data Models
- **`user.py`**: User (patient) model with email, hashed password, full name, timestamps, and relationship to reports
- **`doctor.py`**: Doctor model with email, password, full name, specialization, and relationship to reviewed reports
- **`report.py`**: Report model with file path, extracted health markers (Hemoglobin, WBC, Platelets, RBC), analysis results (JSON), doctor notes, review status, and relationships to users/doctors

#### `/schemas` - API Schemas
- **`auth.py`**: Token schemas for authentication responses
- **`user.py`**: Request/response schemas for user and doctor operations
- **`report.py`**: Schemas for report creation, responses, and doctor reviews

#### `/services` - Business Logic
- **`ocr_service.py`**: Handles text extraction from PDFs (`pdfplumber`) and images (`pytesseract`), with graceful handling of missing dependencies
- **`parser_service.py`**: Extracts health markers using regex patterns (supports various label formats)
- **`ai_engine.py`**: Analyzes health markers against reference ranges, generates rule-based observations, and calls LLM for patient-friendly explanations
- **`storage_service.py`**: Saves uploaded files to user-specific directories with unique filenames

#### Root Files
- **`dependencies.py`**: FastAPI dependency injection functions (database sessions, password hashing with bcrypt, JWT token creation/verification, current user retrieval)
- **`config.py`**: Centralized configuration for JWT, database URL, uploads directory, OpenRouter API settings, and ChromaDB settings
- **`streamlit_app.py`**: Complete Streamlit frontend for testing all API endpoints with a user-friendly interface

## Key Features

### Current Implementation

1. **User & Doctor Authentication**
   - Secure registration with email validation and password hashing (bcrypt)
   - JWT-based authentication with configurable token expiration
   - Separate authentication flows for patients and doctors

2. **Medical Report Processing Pipeline**
   - **Upload**: Secure file storage with user-specific directories
   - **OCR**: Automatic text extraction from PDF and image formats
   - **Parsing**: Intelligent extraction of health markers using pattern matching
   - **Analysis**: Dual-layer analysis combining rule-based detection and AI explanations
   - **Storage**: Data stored in both SQL database and vector store for future RAG queries

3. **AI-Powered Health Analysis**
   - Rule-based comparison against clinical reference ranges
   - LLM-generated patient-friendly explanations (via OpenRouter)
   - Structured analysis results with summaries and observations

4. **Doctor Review System**
   - Doctors can review patient reports
   - Add professional notes and update review status
   - Track review history and doctor assignments

5. **Vector Store Integration (RAG Foundation)**
   - ChromaDB integration for storing embedded report text
   - Patient-specific search capabilities
   - Ready for semantic search and context retrieval

6. **ABHA Integration (Mock)**
   - Placeholder endpoint for future Ayushman Bharat Health Account integration

## API Endpoints

### Authentication (`/auth`)

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/auth/register` | `POST` | Register a new user (patient) | No |
| `/auth/token` | `POST` | Obtain JWT access token for user login | No |

### Reports (`/reports`)

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/reports/upload` | `POST` | Upload a medical report (PDF/image) for OCR, parsing, and AI analysis | Yes (User) |
| `/reports/` | `GET` | Retrieve all reports for the authenticated user | Yes (User) |
| `/reports/{report_id}` | `GET` | Retrieve a specific report by ID | Yes (User) |

### AI Analysis (`/ai`)

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/ai/analyze/{report_id}` | `POST` | Trigger re-analysis of a specific report with updated AI analysis | Yes (User) |

### Doctor Review (`/doctor`)

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/doctor/register_doctor` | `POST` | Register a new doctor account | No |
| `/doctor/token_doctor` | `POST` | Obtain JWT access token for doctor login | No |
| `/doctor/reports/{report_id}/review` | `POST` | Submit or update a doctor's review for a specific report | Yes (Doctor) |

### ABHA Integration (`/abha`)

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/abha/sync` | `POST` | Mock endpoint for ABHA synchronization | No |

## Local Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR (optional, for image-based OCR)

### Installation Steps

1. **Navigate to the Backend Directory**:
   ```bash
   cd aivara-backend
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR (Optional, for Image OCR)**:
   
   **Windows:**
   - Download from [GitHub - UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - Add to PATH during installation
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get update && sudo apt-get install -y tesseract-ocr
   ```
   
   **macOS:**
   ```bash
   brew install tesseract
   ```

4. **Configure Environment Variables (Optional)**:
   
   For full AI functionality, set these environment variables:
   ```bash
   export OPENROUTER_API_KEY="your-api-key"
   export OPENROUTER_MODEL="google/gemini-flash-1.5"
   export OPENROUTER_EMBED_MODEL="openai/text-embedding-3-small"
   ```
   
   **Windows PowerShell:**
   ```powershell
   $env:OPENROUTER_API_KEY="your-api-key"
   $env:OPENROUTER_MODEL="google/gemini-flash-1.5"
   $env:OPENROUTER_EMBED_MODEL="openai/text-embedding-3-small"
   ```

5. **Run the Backend Server**:

   **Using Python directly:**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   **Using the provided script (Linux/macOS):**
   ```bash
   bash run.sh
   ```

   **Using PowerShell script (Windows):**
   ```powershell
   .\start_servers.ps1
   ```

   The server will start on `http://localhost:8000`. API documentation is available at `http://localhost:8000/docs`.

### Starting the Streamlit Frontend (Optional)

To test the API with a user-friendly interface:

```bash
streamlit run streamlit_app.py --server.port 8501
```

Then open `http://localhost:8501` in your browser.

## How the System Works

### Report Processing Workflow

1. **User Uploads Report**
   - User authenticates and uploads a PDF or image file
   - File is saved to `uploads/{user_id}/` with a unique filename

2. **OCR Processing**
   - PDF files: Text extracted using `pdfplumber`
   - Image files: Text extracted using `pytesseract` (Tesseract OCR)
   - Extracted text is stored for analysis

3. **Health Marker Extraction**
   - Regex-based parser scans extracted text for health markers
   - Looks for patterns like "Hemoglobin 14.5 g/dL", "WBC 7.2", etc.
   - Supports multiple label formats (Hb, HGB, WBC, White Blood Cell, etc.)

4. **AI Analysis**
   - **Rule-Based Analysis**: Compares extracted values against clinical reference ranges
     - Hemoglobin: 12.0-17.5 g/dL
     - WBC: 4.0-11.0 x10³/µL
     - Platelets: 150-450 x10³/µL
     - RBC: 4.5-5.9 x10⁶/µL
   - **LLM Explanation**: If OpenRouter API key is configured, generates patient-friendly explanations
   - Results include summary, observations, and AI-generated explanation

5. **Vector Storage (RAG Foundation)**
   - Extracted text is embedded using OpenRouter API or local SentenceTransformer model
   - Embeddings stored in ChromaDB with patient-specific metadata
   - Enables future semantic search and context retrieval

6. **Database Storage**
   - Report metadata, health markers, and analysis results stored in SQLite
   - Relationships maintained between users, reports, and doctors

### Authentication Flow

1. **Registration**: User provides email, password (min 8 chars), and full name
   - Password is hashed using bcrypt
   - User record created in database

2. **Login**: User provides email and password
   - Password verified against stored hash
   - JWT token generated with email in subject
   - Token expires after 30 minutes (configurable)

3. **Protected Endpoints**: JWT token included in Authorization header
   - Token validated and user retrieved from database
   - User context available for request processing

### Doctor Review Flow

1. **Doctor Registration**: Similar to user registration with additional specialization field
2. **Doctor Login**: Separate authentication endpoint for doctors
3. **Review Submission**: Doctor can:
   - Associate themselves with a report
   - Add professional notes
   - Update review status (pending, reviewed, etc.)

## Production Deployment

### Docker Deployment

The application includes a `Dockerfile` for containerization:

```dockerfile
FROM python:3.12-slim-buster
# ... (see Dockerfile for details)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Important Production Considerations:**

1. **Database**: Replace SQLite with PostgreSQL or MySQL for production
   - Update `DATABASE_URL` in `config.py` or via environment variable
   - Use connection pooling and proper database migrations

2. **Security**:
   - Change `SECRET_KEY` in `config.py` to a secure random value
   - Use environment variables for sensitive configuration
   - Enable HTTPS/TLS
   - Implement rate limiting
   - Add CORS configuration for frontend domains

3. **File Storage**: Consider cloud storage (AWS S3, Azure Blob, etc.) instead of local filesystem
   - Update `storage_service.py` to use cloud storage SDK

4. **Vector Store**: ChromaDB can run in server mode for production
   - Update `VECTOR_DIR` or use ChromaDB client connection string

5. **Environment Variables**: Set all sensitive configuration via environment:
   ```bash
   SECRET_KEY=your-secure-secret-key
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   OPENROUTER_API_KEY=your-api-key
   UPLOADS_DIR=/path/to/uploads
   VECTOR_DIR=/path/to/vectorstore
   ```

6. **Monitoring**: Add logging, error tracking (Sentry), and performance monitoring

## Testing

### Using the Streamlit Frontend

The `streamlit_app.py` provides a complete testing interface:
- User registration and login
- Report upload with real-time feedback
- View all reports in a table
- Detailed report view with health markers and analysis
- Error handling with clear messages

### Using the API Documentation

FastAPI automatically generates interactive API documentation:
- Visit `http://localhost:8000/docs` for Swagger UI
- Visit `http://localhost:8000/redoc` for ReDoc

### Manual API Testing

Use `curl`, Postman, or any HTTP client:
```bash
# Register a user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "full_name": "Test User"}'

# Login
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"

# Upload report (replace TOKEN with actual token)
curl -X POST "http://localhost:8000/reports/upload" \
  -H "Authorization: Bearer TOKEN" \
  -F "report_name=Blood Test" \
  -F "file=@/path/to/report.pdf"
```

## Future Enhancements

### Planned Features

1. **Semantic Search**: Query patient history using natural language queries
2. **Trend Analysis**: Track health markers over time with visualizations
3. **RAG-Enhanced Analysis**: Use historical context for more accurate analysis
4. **Multi-Report Comparison**: Compare reports side-by-side
5. **Export Functionality**: Generate PDF summaries and reports
6. **Notification System**: Alerts for concerning health patterns
7. **ABHA Integration**: Full integration with India's health records system
8. **Advanced OCR**: Support for complex formats and handwritten notes
9. **Doctor Dashboard**: Comprehensive interface for medical professionals
10. **API Analytics**: Usage tracking and performance metrics

## Contributing

When contributing to this project:

1. Follow the existing code structure and patterns
2. Add appropriate error handling and logging
3. Update this README if adding new features
4. Test all endpoints thoroughly
5. Ensure compatibility with existing database schema

## License

[Specify your license here]

## Support

For issues, questions, or contributions, please [specify your support channels].

---

**Last Updated**: 2024  
**Version**: 1.0.0
