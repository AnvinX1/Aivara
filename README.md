# Aivara Backend API

## Project Overview

**Aivara** is an intelligent healthcare analytics platform designed to transform how patients interact with their medical reports. The system provides a comprehensive full-stack solution with a FastAPI backend and a modern Next.js/React frontend, enabling users to upload medical reports, extract health information using OCR, analyze health markers with specialized AI models, share reports with doctors, and receive professional reviews—all while maintaining a secure, patient-centric approach.

The system leverages **Retrieval-Augmented Generation (RAG)** for intelligent context-aware analysis, combining rule-based health marker detection with LLM-powered explanations using local Ollama models. Medical reports are stored both in a traditional SQL database and in a vector store (ChromaDB) for semantic search and retrieval, enabling sophisticated query capabilities across a patient's medical history. The platform includes a complete doctor-patient workflow with hospital management, report sharing, and health forecasting capabilities.

## Architecture Overview

### System Flow (Current Implementation)

1. **User Registration & Authentication**: Patients and doctors register and authenticate using JWT tokens with role-based access control
2. **Report Upload**: Medical reports (PDF/image) are uploaded and stored securely in user-specific directories
3. **OCR Processing**: Text is extracted from reports using `pdfplumber` (PDFs) or `pytesseract` (images)
4. **Health Marker Extraction**: Regex-based parser extracts key health markers (Hemoglobin, WBC, Platelets, RBC)
5. **AI Analysis with Specialized Models**: 
   - Rule-based analysis compares values against reference ranges
   - **llama3.2**: General health explanations and analysis
   - **qwen3-vl:2b**: Specialized report reading and understanding
   - **medbot**: Medicine and treatment suggestions
   - **edi**: Women's healthcare-specific recommendations
   - All models run locally via Ollama for privacy and cost-effectiveness
6. **Vector Storage**: Extracted text is embedded using `embeddinggemma:latest` and stored in ChromaDB for RAG capabilities
7. **Hospital & Doctor Management**: Hospitals can be registered with details (name, address, city, state), and doctors register with their license numbers and specializations
8. **Report Sharing**: Patients can select hospitals and doctors to share their reports for professional review
9. **Doctor Review Workflow**: Doctors receive shared reports, review AI analysis, add professional notes, approve/reject findings, and send feedback to patients
10. **Health Forecasting**: LLM-powered predictive analytics to forecast future health outcomes based on historical data
11. **Notification System**: Automated notifications for doctors (new reports) and patients (review updates)
12. **ABHA Integration**: Mock endpoint ready for future Ayushman Bharat Health Account integration

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
- **Ollama**: 🤖 Local LLM server running specialized models for privacy and cost-effectiveness
  - **llama3.2**: General health explanations and analysis
  - **qwen3-vl:2b**: Specialized medical report reading and understanding
  - **medbot**: Medicine and treatment suggestions
  - **edi**: Women's healthcare-specific recommendations
  - **embeddinggemma:latest**: Text embedding generation for vector storage
- **Sentence Transformers**: 📊 Local embedding model (`sentence-transformers/all-MiniLM-L6-v2`) for fallback
- **ChromaDB**: 🧮 Vector similarity search for RAG

### OCR & Document Processing
- **pdfplumber**: 📄 Extract text from PDF documents (both text-based and scanned)
- **pytesseract**: 🔍 Python wrapper for Tesseract OCR engine (for image-based reports)
- **Pillow (PIL)**: 🖼️ Image processing library for OCR preprocessing

### Data Validation
- **Pydantic**: ✅ Data validation and settings management using Python type hints
- **email-validator**: 📧 Email validation for user registration

### Frontend Stack
- **Next.js 16**: ⚛️ React framework with App Router for server-side rendering and static generation
- **React 18**: 🎨 UI library with hooks and modern patterns
- **TypeScript**: 📘 Type-safe JavaScript for better developer experience
- **Tailwind CSS v4**: 🎨 Utility-first CSS framework for responsive design
- **shadcn/ui**: 🎯 High-quality React component library
- **Recharts**: 📊 Composable charting library for health data visualization
- **GSAP**: ✨ Animation library for smooth UI transitions
- **react-markdown**: 📝 Markdown rendering for AI-generated content with syntax highlighting
- **Axios**: 🌐 HTTP client for API communication

### Additional
- **python-multipart**: 📤 Handle file uploads (multipart/form-data)
- **requests**: 🌐 HTTP client for API calls
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
│       ├── auth.py               # Patient authentication (register, login)
│       ├── reports.py            # Report management (upload, list, get by ID, share to doctors)
│       ├── analysis.py           # AI re-analysis endpoint
│       ├── doctor.py             # Doctor registration, login, report reviews, pending reports
│       ├── hospital.py           # Hospital listing and doctor retrieval by hospital
│       ├── forecasting.py        # Health forecasting and prediction endpoints
│       └── abha.py               # ABHA (Ayushman Bharat) integration mock endpoint
│
├── db/                           # Database configuration
│   ├── __init__.py
│   └── database.py               # SQLAlchemy engine, session factory, Base model, table creation
│
├── models/                       # SQLAlchemy ORM models (database schema)
│   ├── __init__.py
│   ├── user.py                   # User model (patients)
│   ├── doctor.py                 # Doctor model (medical professionals with hospital association)
│   ├── hospital.py               # Hospital model (hospitals in India with location data)
│   ├── report.py                 # Report model (medical reports with health markers, AI/doctor approval)
│   ├── report_sharing.py         # ReportSharing model (tracking patient-doctor report sharing)
│   └── forecast.py               # Forecast model (LLM-generated health predictions)
│
├── schemas/                      # Pydantic models (API request/response validation)
│   ├── __init__.py
│   ├── auth.py                   # Token, TokenData schemas
│   ├── user.py                   # UserCreate, UserResponse, DoctorCreate, DoctorResponse
│   ├── hospital.py               # HospitalBase, HospitalCreate, HospitalResponse
│   ├── report.py                 # ReportCreate, ReportResponse, ReportReview (with AI/doctor approval)
│   ├── report_sharing.py         # ReportSharingBase, ReportSharingCreate, ReportSharingResponse
│   └── forecast.py               # ForecastBase, ForecastCreate, ForecastResponse
│
├── services/                     # Business logic services
│   ├── __init__.py
│   ├── ocr_service.py            # Text extraction from PDFs and images
│   ├── parser_service.py         # Health marker extraction using regex patterns
│   ├── ai_engine.py              # Health marker analysis with specialized Ollama models
│   ├── ollama_service.py         # Ollama API client for LLM and embedding calls
│   ├── forecasting_service.py    # LLM-based health forecasting and prediction
│   ├── notification_service.py   # Notification system for doctors and patients
│   └── storage_service.py        # File storage management (save uploaded reports)
│
├── dependencies.py               # FastAPI dependencies (get_db, password hashing, JWT, get_current_user/doctor)
├── config.py                     # Application configuration (JWT, database, uploads, Ollama, ChromaDB)
├── seed_hospitals.py             # Script to populate database with Indian hospitals and doctors
│
├── uploads/                      # Directory for storing uploaded medical reports (user-specific subdirectories)
├── vectorstore/                  # ChromaDB persistent storage directory (auto-created)
├── aivara.db                     # SQLite database file (auto-created)
│
├── frontend/                     # Next.js React frontend application
│   ├── app/                      # Next.js App Router pages and layouts
│   │   ├── (auth)/               # Authentication routes (login, register)
│   │   ├── (dashboard)/          # Patient dashboard routes
│   │   ├── doctor/               # Doctor portal routes (login, register, dashboard)
│   │   ├── layout.tsx            # Root layout with providers
│   │   └── globals.css           # Global styles and Tailwind CSS
│   ├── components/               # React components
│   │   ├── layout/               # Header, Sidebar, navigation components
│   │   ├── dashboard/            # Report cards, charts, AI analysis display
│   │   ├── patient/              # Patient-specific components (report sharing)
│   │   └── ui/                   # shadcn/ui components
│   ├── lib/                      # Utility libraries
│   │   ├── api.ts                # Axios-based API client with interceptors
│   │   ├── auth.ts               # Authentication utilities
│   │   └── animations.ts         # GSAP animation utilities
│   ├── hooks/                    # React custom hooks
│   │   └── useAuth.ts            # Authentication hook
│   ├── package.json              # Frontend dependencies
│   └── next.config.js            # Next.js configuration
│
├── streamlit_app.py              # Legacy Streamlit frontend (still available for testing)
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
- **`main.py`**: Initializes the FastAPI application, sets up startup events (database table creation), includes the API router, and configures CORS middleware
- **`services/`**: Application-level services that support the core functionality
  - **`embeddings_service.py`**: Generates text embeddings using Ollama `embeddinggemma:latest` (with fallback to local SentenceTransformer model)
  - **`vector_store.py`**: Manages ChromaDB operations for storing and retrieving embedded document chunks (RAG foundation)

#### `/api` - API Routing Layer
- **`router.py`**: Central router that combines all route modules with appropriate prefixes and tags
- **`routes/`**: Individual route handlers organized by domain
  - **`auth.py`**: Patient registration and authentication endpoints
  - **`reports.py`**: Medical report upload, retrieval, management, and sharing with doctors
  - **`analysis.py`**: Re-analysis of existing reports with updated AI analysis
  - **`doctor.py`**: Doctor-specific endpoints (registration, authentication, pending reports, review submission)
  - **`hospital.py`**: Hospital listing and doctor retrieval by hospital
  - **`forecasting.py`**: Health forecasting endpoints using LLM predictions
  - **`abha.py`**: Mock endpoint for future ABHA integration

#### `/db` - Database Layer
- **`database.py`**: SQLAlchemy configuration including engine creation, session factory, declarative base, and automatic table creation

#### `/models` - Data Models
- **`user.py`**: User (patient) model with email, hashed password, full name, timestamps, and relationship to reports
- **`doctor.py`**: Doctor model with email, password, full name, specialization, hospital_id, phone, registration_number, is_active, and relationship to hospital and reports
- **`hospital.py`**: Hospital model with name, address, city, state, pincode, phone, email, is_active, and relationship to doctors
- **`report.py`**: Report model with file path, extracted health markers (Hemoglobin, WBC, Platelets, RBC), analysis results (JSON), ai_approval_status, doctor_approval_timestamp, and relationships to users/doctors
- **`report_sharing.py`**: ReportSharing model tracking patient-doctor report sharing workflow with status (sent, under_review, reviewed), patient_message, and timestamps
- **`forecast.py`**: Forecast model storing LLM-generated health predictions with forecast_type, forecast_data, confidence_score, and timestamps

#### `/schemas` - API Schemas
- **`auth.py`**: Token schemas for authentication responses
- **`user.py`**: Request/response schemas for user and doctor operations
- **`report.py`**: Schemas for report creation, responses, and doctor reviews

#### `/services` - Business Logic
- **`ocr_service.py`**: Handles text extraction from PDFs (`pdfplumber`) and images (`pytesseract`), with graceful handling of missing dependencies
- **`parser_service.py`**: Extracts health markers using regex patterns (supports various label formats)
- **`ai_engine.py`**: Analyzes health markers against reference ranges, generates rule-based observations, and uses specialized Ollama models:
  - `make_explanation()`: Uses `llama3.2` for general health explanations
  - `read_report_with_qwen3vl()`: Uses `qwen3-vl:2b` for report reading and understanding
  - `get_medicine_suggestions()`: Uses `medbot` for medicine and treatment recommendations
  - `get_women_health_suggestions()`: Uses `edi` for women's healthcare recommendations
- **`ollama_service.py`**: Ollama API client providing functions for LLM calls (`call_ollama_llm`, `call_ollama_chat`) and embedding generation (`get_embedding_via_ollama`)
- **`forecasting_service.py`**: LLM-based health forecasting service using `llama3.2` to predict future health outcomes based on historical data
- **`notification_service.py`**: Notification system for doctors (new report notifications) and patients (review update notifications)
- **`storage_service.py`**: Saves uploaded files to user-specific directories with unique filenames

#### Root Files
- **`dependencies.py`**: FastAPI dependency injection functions (database sessions, password hashing with bcrypt, JWT token creation/verification, current user/doctor retrieval)
- **`config.py`**: Centralized configuration for JWT, database URL, uploads directory, Ollama base URL and model assignments, and ChromaDB settings
- **`seed_hospitals.py`**: Script to populate database with major Indian hospitals and sample doctors (default password: `Doctor@123`)
- **`streamlit_app.py`**: Legacy Streamlit frontend for testing all API endpoints (deprecated in favor of Next.js frontend)

#### `/frontend` - Next.js React Frontend
- **`app/`**: Next.js App Router structure with route groups and layouts
  - **`(auth)/`**: Patient authentication pages (login, register)
  - **`(dashboard)/`**: Patient dashboard with reports, upload, and detailed views
  - **`doctor/`**: Doctor portal (login, register, dashboard, report review)
  - **`layout.tsx`**: Root layout with Toaster provider and metadata
  - **`globals.css`**: Tailwind CSS v4 styles with custom properties
- **`components/`**: Reusable React components
  - **`layout/`**: Header, Sidebar with navigation
  - **`dashboard/`**: ReportCards, ReportDetails, HealthMarkerChart, TrendChart, AIAnalysisDisplay
  - **`patient/`**: ShareReport component for selecting hospitals and doctors
  - **`ui/`**: shadcn/ui components (Button, Card, Input, etc.) and Markdown renderer
- **`lib/`**: Utility libraries and API client
  - **`api.ts`**: Axios-based API client with request/response interceptors, JWT token management, role-based error handling
  - **`auth.ts`**: LocalStorage-based authentication utilities
  - **`animations.ts`**: GSAP animation utilities for page transitions and staggered effects
- **`hooks/`**: React custom hooks
  - **`useAuth.ts`**: Authentication hook for user state management

## Key Features

### Current Implementation

1. **User & Doctor Authentication**
   - Secure registration with email validation and password hashing (bcrypt)
   - JWT-based authentication with configurable token expiration
   - Separate authentication flows for patients and doctors with role-based access control
   - Doctor registration with hospital association, license number, and specialization

2. **Medical Report Processing Pipeline**
   - **Upload**: Secure file storage with user-specific directories
   - **OCR**: Automatic text extraction from PDF and image formats
   - **Parsing**: Intelligent extraction of health markers using pattern matching
   - **Analysis**: Multi-model AI analysis combining rule-based detection and specialized LLM explanations
   - **Storage**: Data stored in both SQL database and vector store (ChromaDB) for RAG queries

3. **AI-Powered Health Analysis with Specialized Models**
   - Rule-based comparison against clinical reference ranges
   - **General Explanations**: `llama3.2` for patient-friendly health explanations
   - **Report Reading**: `qwen3-vl:2b` for specialized medical report understanding
   - **Medicine Suggestions**: `medbot` for treatment and medication recommendations
   - **Women's Health**: `edi` for women's healthcare-specific advice
   - All models run locally via Ollama for privacy, cost-effectiveness, and offline capability

4. **Hospital & Doctor Management**
   - Hospital registration with complete location data (name, address, city, state, pincode)
   - Doctor registration with hospital association, specialization, and license number
   - Hospital and doctor listing APIs with filtering capabilities
   - Pre-seeded database with major Indian hospitals (Mumbai, Delhi, Bangalore, Chennai, Hyderabad, Kolkata, Coimbatore including KMCH)

5. **Report Sharing & Doctor Review Workflow**
   - Patients can browse hospitals by city/state and view available doctors
   - Report sharing with optional patient messages
   - Doctor dashboard with pending reports, review history, and statistics
   - Doctors can review AI analysis, approve/reject findings, add professional notes
   - AI approval status tracking (approved/rejected/needs_review)
   - Doctor approval timestamp and review status updates
   - Notification system for doctors (new reports) and patients (review updates)

6. **Health Forecasting**
   - LLM-powered predictive analytics using `llama3.2`
   - Forecast generation based on historical health data
   - Trend analysis and future outcome predictions
   - Confidence scoring for predictions

7. **Vector Store Integration (RAG Foundation)**
   - ChromaDB integration for storing embedded report text using `embeddinggemma:latest`
   - Patient-specific search capabilities
   - Ready for semantic search and context retrieval

8. **Modern Web Frontend (Next.js/React)**
   - Responsive design with Tailwind CSS v4 and shadcn/ui components
   - Patient dashboard with report management, charts, and AI analysis display
   - Doctor portal with review interface and pending reports management
   - Markdown support for AI-generated content with syntax highlighting
   - GSAP animations for smooth UI transitions
   - Recharts for health data visualization (bar charts, trend lines)
   - Role-based routing and authentication

9. **ABHA Integration (Mock)**
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
| `/doctor/register_doctor` | `POST` | Register a new doctor account with hospital association | No |
| `/doctor/token_doctor` | `POST` | Obtain JWT access token for doctor login | No |
| `/doctor/reports/pending` | `GET` | Get all pending reports sent to the current doctor with patient info | Yes (Doctor) |
| `/doctor/reports/{report_id}` | `GET` | Get detailed report information for doctor review | Yes (Doctor) |
| `/doctor/reports/{report_id}/review` | `POST` | Submit or update a doctor's review with AI approval status and notes | Yes (Doctor) |
| `/doctor/reports/reviewed` | `GET` | Get all reviewed reports by the current doctor | Yes (Doctor) |
| `/doctor/profile` | `GET` | Get current doctor's profile information | Yes (Doctor) |

### Hospitals (`/hospitals`)

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/hospitals/` | `GET` | List all hospitals with optional city/state filtering | No |
| `/hospitals/{hospital_id}` | `GET` | Get hospital details | No |
| `/hospitals/{hospital_id}/doctors` | `GET` | Get all doctors associated with a hospital | No |

### Reports - Sharing (`/reports`)

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/reports/{report_id}/share` | `POST` | Share a report with a specific doctor | Yes (User) |
| `/reports/shared` | `GET` | Get all reports shared by the current user | Yes (User) |
| `/reports/{report_id}/cancel-sharing/{sharing_id}` | `PUT` | Cancel report sharing | Yes (User) |

### Forecasting (`/forecasting`)

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/forecasting/generate` | `POST` | Generate health forecast for a specific report | Yes (User) |
| `/forecasting/{report_id}` | `GET` | Get forecast for a specific report | Yes (User) |
| `/forecasting/trends` | `GET` | Get forecasting trends for the current user | Yes (User) |

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

4. **Install Ollama (Required for AI Features)**:
   
   Download and install Ollama from [https://ollama.ai](https://ollama.ai)
   
   Pull the required models:
   ```bash
   ollama pull llama3.2
   ollama pull qwen3-vl:2b
   ollama pull medbot
   ollama pull edi
   ollama pull embeddinggemma:latest
   ```
   
   Ensure Ollama is running on `http://localhost:11434` (default)

5. **Seed Database with Hospitals and Doctors**:
   
   ```bash
   python seed_hospitals.py
   ```
   
   This creates major Indian hospitals and sample doctors. Default doctor password: `Doctor@123`

6. **Configure Environment Variables (Optional)**:
   
   Create a `.env` file or set environment variables:
   ```bash
   SECRET_KEY="your-secret-key-here"
   OLLAMA_BASE_URL="http://localhost:11434"  # Default Ollama URL
   DATABASE_URL="sqlite:///./aivara.db"
   UPLOADS_DIR="./uploads"
   VECTOR_DIR="./vectorstore"
   ```
   
   **Windows PowerShell:**
   ```powershell
   $env:SECRET_KEY="your-secret-key-here"
   $env:OLLAMA_BASE_URL="http://localhost:11434"
   ```

7. **Run the Backend Server**:

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

### Starting the Next.js Frontend

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

   The frontend will start on `http://localhost:3000`.

4. **Access the application**:
   - **Patient Portal**: `http://localhost:3000/login`
   - **Doctor Portal**: `http://localhost:3000/doctor/login`
   - **API Docs**: `http://localhost:8000/docs`

### Starting the Streamlit Frontend (Legacy, Optional)

To test the API with the legacy Streamlit interface:

```bash
streamlit run streamlit_app.py --server.port 8501
```

Then open `http://localhost:8501` in your browser.

**Note**: The Streamlit frontend is deprecated in favor of the Next.js frontend.

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

4. **AI Analysis with Specialized Models**
   - **Rule-Based Analysis**: Compares extracted values against clinical reference ranges
     - Hemoglobin: 12.0-17.5 g/dL
     - WBC: 4.0-11.0 x10³/µL
     - Platelets: 150-450 x10³/µL
     - RBC: 4.5-5.9 x10⁶/µL
   - **Specialized LLM Processing**:
     - **General Explanations** (`llama3.2`): Patient-friendly health explanations
     - **Report Reading** (`qwen3-vl:2b`): Specialized medical report understanding during upload
     - **Medicine Suggestions** (`medbot`): On-demand medicine and treatment recommendations
     - **Women's Health** (`edi`): On-demand women's healthcare-specific advice
   - Results include summary, observations, AI-generated explanation, and optional specialized suggestions

5. **Vector Storage (RAG Foundation)**
   - Extracted text is embedded using Ollama `embeddinggemma:latest` (with fallback to local SentenceTransformer model)
   - Embeddings stored in ChromaDB with patient-specific metadata
   - Enables semantic search and context retrieval for RAG-enhanced analysis

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

### Doctor-Patient Workflow

1. **Hospital & Doctor Setup**:
   - Hospitals register with location details
   - Doctors register with hospital association, specialization, and license number
   - Database seeded with major Indian hospitals (Mumbai, Delhi, Bangalore, Chennai, Hyderabad, Kolkata, Coimbatore)

2. **Report Sharing Flow**:
   - Patient uploads and analyzes report with AI
   - Patient browses hospitals by city/state
   - Patient selects a doctor from the hospital
   - Patient shares report with optional message
   - Doctor receives notification of new report

3. **Doctor Review Flow**:
   - Doctor logs into portal
   - Doctor views pending reports with patient information
   - Doctor reviews AI analysis and report details
   - Doctor can:
     - Approve or reject AI findings
     - Add professional notes (markdown supported)
     - Update review status
   - Patient receives notification of doctor review

4. **Health Forecasting**:
   - Patient can generate forecasts based on historical data
   - LLM analyzes trends and predicts future outcomes
   - Forecasts include confidence scores and recommendations

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

## Hackathon Evaluation Criteria

This section addresses the hackathon evaluation framework, demonstrating how Aivara meets each criterion with current implementations and planned enhancements.

---

## 1. AI Integration & Innovation

### Current AI Implementations

#### Retrieval-Augmented Generation (RAG) Architecture

```mermaid
graph TB
    A[Medical Report Upload] --> B[OCR Text Extraction]
    B --> C[Text Chunking Service]
    C --> D[Embedding Generation]
    D --> E[Vector Store ChromaDB]
    E --> F[Patient History Context]
    F --> G[LLM Analysis with Context]
    G --> H[Personalized Health Explanations]
    
    I[User Query] --> J[Semantic Search]
    J --> E
    J --> K[Retrieve Relevant Chunks]
    K --> G
    
    style E fill:#4A90E2
    style G fill:#50C878
    style H fill:#FF6B6B
```

**Technologies Used:**

- **Ollama Integration** (`services/ollama_service.py`, `services/ai_engine.py`)
  - **Local LLM Server**: All AI models run locally via Ollama for privacy and cost-effectiveness
  - **Specialized Models**:
    - `llama3.2`: General health explanations and analysis
    - `qwen3-vl:2b`: Specialized medical report reading and understanding
    - `medbot`: Medicine and treatment suggestions
    - `edi`: Women's healthcare-specific recommendations
    - `embeddinggemma:latest`: Text embedding generation for vector storage
  - **Model Selection**: Automatic model selection based on function (general, report reading, medicine, women's health)
  - **Patient-friendly Explanations**: Context-aware explanations using patient history
  
- **RAG Pipeline** (`app/services/vector_store.py`)
  - **ChromaDB**: Persistent vector database for semantic search
  - **Embeddings Service**: Primary Ollama `embeddinggemma:latest` with SentenceTransformer fallback
  - **Context Retrieval**: Patient-specific historical report analysis
  - **Top-K Retrieval**: Configurable context window (default: 5 chunks)

- **Intelligent Text Processing**
  - **Text Chunking** (`services/text_chunking_service.py`): Overlapping chunks (500 chars, 50 char overlap) with sentence boundary detection
  - **Health Marker Extraction** (`services/parser_service.py`): Regex-based parsing supporting multiple label formats
  - **Multi-format Support**: Handles various medical report formats and terminology

#### AI Analysis Pipeline

```mermaid
sequenceDiagram
    participant U as User
    participant API as FastAPI
    participant OCR as OCR Service
    participant Parser as Parser Service
    participant VS as Vector Store
    participant AI as AI Engine
    participant Ollama as Ollama LLM

    U->>API: Upload Report
    API->>OCR: Extract Text
    OCR-->>API: Raw Text
    API->>Parser: Parse Health Markers
    Parser-->>API: Structured Data
    API->>VS: Chunk & Store
    VS->>VS: Generate Embeddings
    VS-->>API: Stored
    API->>AI: Analyze with Context
    AI->>VS: Retrieve Historical Context
    VS-->>AI: Relevant Chunks
    AI->>Ollama: Generate Explanation (llama3.2) with Context
    Ollama-->>AI: Patient-Friendly Explanation
    AI->>Ollama: Read Report (qwen3-vl:2b)
    Ollama-->>AI: Report Insights
    AI-->>API: Complete Analysis
    API-->>U: Analysis Results
```

**AI Features:**

1. **Rule-Based Analysis**: Clinical reference range comparison (Hemoglobin, WBC, Platelets, RBC)
2. **Specialized LLM Models**: Different models for different tasks:
   - General explanations (`llama3.2`)
   - Report reading (`qwen3-vl:2b`)
   - Medicine suggestions (`medbot`)
   - Women's health (`edi`)
3. **Context-Aware Explanations**: Uses patient history via RAG for personalized insights
4. **Local Processing**: All models run locally via Ollama - no API costs, complete privacy
5. **Historical Context Integration**: RAG retrieves relevant past reports for trend analysis
6. **Health Forecasting**: LLM-powered predictions based on historical data

#### Planned AI Enhancements

- **Advanced Pattern Recognition**: Machine learning models for anomaly detection
- **Predictive Analytics**: Trend prediction using historical data
- **Multi-Modal Analysis**: Image-based health marker detection (beyond OCR)
- **Personalized Health Insights**: User-specific recommendations based on patterns
- **Automated Report Summarization**: Generate executive summaries from complex reports

---

## 2. Problem Statement & Value Proposition

### Problem Statement

**Challenge:** Patients struggle to understand medical reports due to:
- Medical jargon and technical terminology
- Lack of context from previous health records
- Difficulty tracking health trends over time
- No personalized explanations or recommendations

### Value Proposition

**Aivara** provides an intelligent healthcare analytics platform that:

1. **Democratizes Medical Understanding**: Transforms complex medical reports into patient-friendly explanations
2. **Contextual Intelligence**: Uses RAG to provide personalized insights based on complete medical history
3. **Accessibility**: Free AI models ensure zero-cost operation for users
4. **Doctor-Patient Bridge**: Facilitates better communication through structured doctor reviews

### Target Impact

```mermaid
pie title Value Creation Distribution
    "Patient Understanding" : 35
    "Healthcare Accessibility" : 25
    "Medical Cost Reduction" : 20
    "Preventive Care Enablement" : 20
```

### Key Differentiators

- **Free AI Models**: Uses Llama/Mistral free tiers - no subscription costs
- **RAG Architecture**: Historical context-aware analysis (unique in healthcare)
- **Multi-format Support**: Handles PDF and image reports
- **Doctor Integration**: Two-tier authentication (patients + doctors)
- **ABHA Ready**: Prepared for India's national health records integration

---

## 3. UI Usability

### Current UI Implementation

#### Next.js React Frontend (`frontend/`)

**Features:**

- **Modern, Responsive Design**
  - Tailwind CSS v4 with custom design system
  - shadcn/ui component library for consistent UI
  - Mobile-first responsive layouts
  - Dark mode support (via Tailwind)

- **Patient Portal**
  - Dashboard with report overview and statistics
  - Upload interface with drag-and-drop
  - Report list with health marker charts
  - Detailed report view with AI analysis
  - Report sharing interface (select hospital → doctor → share)
  - Markdown-rendered AI responses with syntax highlighting
  - Health trend charts (Recharts)
  - Forecasting visualization

- **Doctor Portal**
  - Separate authentication and routing
  - Dashboard with pending/reviewed reports statistics
  - Pending reports list with patient information
  - Report review interface with AI analysis display
  - Approval/rejection with markdown notes editor
  - Review history tracking

- **Enhanced UX Features**
  - GSAP animations for smooth page transitions
  - Staggered animations for list items
  - Loading states with spinners
  - Toast notifications for user feedback
  - Role-based navigation (patient vs. doctor)
  - Protected routes with authentication guards

- **Error Handling**
  - Graceful error messages with user-friendly descriptions
  - Network error handling with retry options
  - 401 error handling with role-based redirects
  - Form validation feedback

```mermaid
graph TB
    A[Root Page] --> B{User Role?}
    B -->|Patient| C[Patient Login]
    B -->|Doctor| D[Doctor Login]
    C --> E[Patient Dashboard]
    D --> F[Doctor Dashboard]
    E --> G[Upload Report]
    E --> H[My Reports]
    E --> I[Report Details]
    E --> J[Share Report]
    I --> K[AI Analysis]
    I --> L[Health Charts]
    I --> M[Forecasting]
    F --> N[Pending Reports]
    F --> O[Review Report]
    F --> P[Reviewed Reports]
    O --> Q[Approve/Reject]
    O --> R[Add Notes]
    
    style E fill:#4A90E2
    style F fill:#50C878
    style K fill:#FF6B6B
    style L fill:#FFA500
```

### UI Enhancements Completed

- ✅ **Dashboard Analytics**: Recharts-based visual charts for health marker trends
- ✅ **Responsive Design**: Mobile-optimized layouts with Tailwind CSS
- ✅ **Dark Mode**: Theme support via Tailwind CSS variables
- ✅ **Interactive Charts**: Bar charts and trend lines for health markers
- ✅ **Markdown Support**: Rich rendering of AI-generated content
- ✅ **Animations**: GSAP-powered smooth transitions
- ✅ **Doctor Portal**: Complete doctor workflow with review interface

### Planned UI Enhancements

- **Report Comparison View**: Side-by-side report analysis
- **Accessibility Features**: Enhanced screen reader support, keyboard navigation
- **Interactive Health Timeline**: Visual representation of health journey
- **Real-time Notifications**: Push notifications for doctor reviews
- **Advanced Filtering**: Enhanced search and filter options for reports

---

## 4. Responsiveness

### Current Performance Features

#### Backend Optimization

- **Async Framework**: FastAPI with ASGI (Uvicorn) for high concurrency
- **Database Optimization**: SQLAlchemy ORM with connection pooling
- **Efficient File Handling**: Streaming file uploads, unique filename generation
- **Error Handling**: Non-blocking vector store operations (failures don't block uploads)

#### Response Time Architecture

```mermaid
graph TB
    A[API Request] --> B{Request Type}
    B -->|Auth| C[< 100ms<br/>JWT Generation]
    B -->|Upload| D[OCR Processing<br/>2-10s]
    D --> E[Chunking<br/>< 1s]
    E --> F[Vector Store<br/>3-5s]
    F --> G[AI Analysis<br/>2-5s]
    G --> H[Response<br/>Total: 7-20s]
    B -->|List Reports| I[< 200ms<br/>DB Query]
    B -->|Get Report| J[< 100ms<br/>Single Query]
    
    style C fill:#50C878
    style I fill:#50C878
    style J fill:#50C878
    style H fill:#FFA500
```

**Performance Metrics:**

- **Authentication**: < 100ms (JWT-based)
- **Report List**: < 200ms (optimized queries)
- **Report Upload**: 7-20s (includes OCR + AI analysis)
- **Vector Store Operations**: 3-5s (async, non-blocking)

### Planned Responsiveness Improvements

- **Caching Layer**: Redis for frequently accessed reports
- **Background Jobs**: Celery for async OCR/AI processing
- **CDN Integration**: Fast file serving via cloud CDN
- **Database Indexing**: Enhanced indexes for faster queries
- **API Rate Limiting**: Prevent abuse while maintaining performance
- **Connection Pooling**: Optimized database connections

---

## 5. Data Persistence

### Current Data Storage Architecture

```mermaid
erDiagram
    USERS ||--o{ REPORTS : owns
    DOCTORS ||--o{ REPORTS : reviews
    REPORTS ||--o{ VECTOR_CHUNKS : "embedded in"
    
    USERS {
        int id PK
        string email UK
        string hashed_password
        string full_name
        datetime created_at
        datetime updated_at
        boolean is_active
    }
    
    HOSPITALS ||--o{ DOCTORS : has
    DOCTORS {
        int id PK
        string email UK
        string hashed_password
        string full_name
        string specialization
        int hospital_id FK
        string phone
        string registration_number
        boolean is_active
        datetime created_at
    }
    
    HOSPITALS {
        int id PK
        string name
        string address
        string city
        string state
        string pincode
        string phone
        string email
        boolean is_active
        datetime created_at
    }
    
    USERS ||--o{ REPORT_SHARING : shares
    DOCTORS ||--o{ REPORT_SHARING : receives
    REPORTS ||--o{ REPORT_SHARING : shared_via
    REPORTS {
        int id PK
        int user_id FK
        string report_name
        string file_path
        datetime upload_timestamp
        text analysis_result_json
        text doctor_notes
        string review_status
        string ai_approval_status
        datetime doctor_approval_timestamp
        float hemoglobin
        float wbc
        float platelets
        float rbc
    }
    
    REPORT_SHARING {
        int id PK
        int report_id FK
        int patient_id FK
        int doctor_id FK
        string patient_message
        string status
        datetime sent_at
        datetime reviewed_at
    }
    
    REPORTS ||--o{ FORECASTS : has
    FORECASTS {
        int id PK
        int report_id FK
        int patient_id FK
        string forecast_type
        json forecast_data
        float confidence_score
        datetime generated_at
    }
    
    VECTOR_CHUNKS {
        string id PK
        string patient_id
        string text
        vector embedding
        json metadata
    }
```

### Implemented Persistence Solutions

#### Relational Database (SQLite/PostgreSQL Ready)

**Technologies:**
- **SQLAlchemy ORM**: Database abstraction layer
- **SQLite**: Development database (production-ready for PostgreSQL/MySQL)
- **Schema Design**: Normalized relational structure
- **Relationships**: Foreign keys for referential integrity

**Data Stored:**
- User accounts and authentication data
- Hospital profiles with location data
- Doctor profiles with hospital associations, specializations, and license numbers
- Medical reports metadata and analysis results
- Health markers (structured data)
- AI approval status and doctor approval timestamps
- Report sharing records and status
- Doctor reviews and notes
- Health forecasts and predictions
- Upload timestamps and status

#### Vector Database (ChromaDB)

**Technologies:**
- **ChromaDB**: Persistent vector store
- **Embeddings**: Generated via Ollama `embeddinggemma:latest` (with SentenceTransformer fallback)
- **Metadata Filtering**: Patient-specific search with metadata filters

**Data Stored:**
- Text chunks from medical reports
- Embedding vectors for semantic search
- Report metadata (report_id, chunk_index, timestamps)
- Patient-specific filtering via metadata

#### File Storage

**Technologies:**
- **Local Filesystem**: User-specific directories
- **UUID-based Naming**: Prevents filename conflicts
- **Organized Structure**: `uploads/{user_id}/{uuid}.{ext}`

**Data Stored:**
- Original PDF/image files
- Secure user isolation via directory structure

### Data Flow Diagram

```mermaid
flowchart TD
    A[Report Upload] --> B[File Storage<br/>uploads/user_id/]
    A --> C[SQL Database<br/>Report Metadata]
    A --> D[OCR Text Extraction]
    D --> E[Text Chunking]
    E --> F[Embedding Generation]
    F --> G[Vector Store<br/>ChromaDB]
    
    H[Query Request] --> I{Query Type}
    I -->|Structured| C
    I -->|Semantic| G
    G --> J[Similarity Search]
    J --> K[Relevant Chunks]
    K --> L[Context for AI]
    
    style B fill:#FFD700
    style C fill:#4A90E2
    style G fill:#50C878
```

### Planned Persistence Enhancements

- **Database Migrations**: Alembic for schema versioning
- **Backup & Recovery**: Automated backup strategies
- **Cloud Storage**: Migration to AWS S3/Azure Blob for files
- **Data Encryption**: At-rest encryption for sensitive data
- **Audit Logging**: Track all data access and modifications
- **Data Retention Policies**: Automated archival for old reports

---

## 6. User Auth & Security

### Security Architecture

```mermaid
graph TB
    A[User Registration] --> B[Password Hashing<br/>bcrypt]
    B --> C[Database Storage]
    D[User Login] --> E[Password Verification]
    E --> F[JWT Token Generation]
    F --> G[Token Storage Client-side]
    G --> H[Protected Endpoints]
    H --> I[Token Validation]
    I --> J[User Context]
    
    K[Doctor Auth] --> L[Role-Based Tokens]
    L --> M[Doctor Endpoints]
    
    style B fill:#FF6B6B
    style F fill:#4A90E2
    style I fill:#50C878
```

### Implemented Security Features

#### Authentication & Authorization

**Technologies:**

1. **JWT (JSON Web Tokens)** (`dependencies.py`, `services/ai_engine.py`)
   - **Library**: `python-jose` with HS256 algorithm
   - **Token Expiration**: 30 minutes (configurable)
   - **Secure Key**: 256-bit secret key
   - **Token Payload**: Email (subject) + expiration time

2. **Password Security** (`dependencies.py`)
   - **Hashing**: bcrypt (direct implementation, no passlib)
   - **Salt**: Automatic salt generation per password
   - **Strength**: 72-byte password limit handled
   - **Verification**: Constant-time comparison

3. **OAuth2 Flow** (`api/routes/auth.py`)
   - **Standard**: OAuth2PasswordBearer
   - **Token URL**: `/auth/token`
   - **Bearer Token**: Header-based authentication

4. **Role-Based Access** (`api/routes/doctor.py`, `dependencies.py`)
   - **Separate Endpoints**: Patient vs. Doctor authentication
   - **Role Claims**: JWT includes role information (`"role": "doctor"` or patient)
   - **Endpoint Protection**: `get_current_user` for patient endpoints, `get_current_doctor` for doctor endpoints
   - **Frontend Role-Based Routing**: Next.js redirects based on user role from localStorage

#### Security Implementation Details

```mermaid
sequenceDiagram
    participant C as Client
    participant API as FastAPI
    participant Auth as Auth Service
    participant DB as Database
    participant JWT as JWT Service

    C->>API: POST /auth/register
    API->>Auth: Hash Password (bcrypt)
    Auth-->>API: Hashed Password
    API->>DB: Store User
    DB-->>API: User Created
    API-->>C: 201 Created
    
    C->>API: POST /auth/token
    API->>DB: Verify User
    DB-->>API: User Found
    API->>Auth: Verify Password
    Auth-->>API: Valid
    API->>JWT: Generate Token
    JWT-->>API: JWT Token
    API-->>C: Access Token
    
    C->>API: GET /reports (with Bearer Token)
    API->>JWT: Verify Token
    JWT-->>API: Valid + User Email
    API->>DB: Get User
    DB-->>API: User Context
    API-->>C: User Reports
```

**Security Layers:**

1. **Password Security**
   - Minimum 8 characters enforced
   - Bcrypt hashing (10 rounds by default)
   - No password storage in plain text
   - Unique salts per password

2. **Token Security**
   - HS256 algorithm (HMAC SHA-256)
   - Short expiration (30 minutes)
   - Stateless authentication
   - No token storage on server

3. **API Security**
   - Protected endpoints require valid JWT
   - User context validation on every request
   - Role-based access control (doctor vs. patient)
   - HTTPException for unauthorized access

4. **Data Security**
   - User-specific file isolation (`uploads/{user_id}/`)
   - SQL injection prevention (SQLAlchemy ORM)
   - Input validation (Pydantic schemas)
   - Email format validation

### Planned Security Enhancements

- **HTTPS/TLS**: SSL certificate implementation
- **Rate Limiting**: Prevent brute force attacks
- **CORS Configuration**: Restrict cross-origin requests
- **API Key Rotation**: Regular secret key updates
- **Two-Factor Authentication**: Additional security layer
- **Session Management**: Refresh tokens for extended sessions
- **Audit Trail**: Log all authentication attempts
- **Data Encryption**: Encrypt sensitive fields at rest
- **Input Sanitization**: Enhanced XSS prevention

---

## Feature Implementation Matrix

| Category | Feature | Status | Technology |
|----------|---------|--------|------------|
| **AI Integration** | RAG Architecture | ✅ Implemented | ChromaDB, Ollama Embeddings |
| **AI Integration** | Specialized LLM Models | ✅ Implemented | Ollama (llama3.2, qwen3-vl:2b, medbot, edi) |
| **AI Integration** | Health Marker Parsing | ✅ Implemented | Regex Patterns |
| **AI Integration** | Historical Context Analysis | ✅ Implemented | Vector Similarity Search |
| **AI Integration** | Health Forecasting | ✅ Implemented | Ollama LLM (llama3.2) |
| **AI Integration** | Medicine Suggestions | ✅ Implemented | Ollama (medbot) |
| **AI Integration** | Women's Health Advice | ✅ Implemented | Ollama (edi) |
| **UI Usability** | Next.js Frontend | ✅ Implemented | Next.js 16, React 18, TypeScript |
| **UI Usability** | Patient Dashboard | ✅ Implemented | shadcn/ui, Recharts |
| **UI Usability** | Doctor Portal | ✅ Implemented | Next.js, Role-based routing |
| **UI Usability** | Dashboard Analytics | ✅ Implemented | Recharts (Bar/Line charts) |
| **UI Usability** | Markdown Rendering | ✅ Implemented | react-markdown, syntax highlighting |
| **UI Usability** | Animations | ✅ Implemented | GSAP |
| **Workflow** | Report Sharing | ✅ Implemented | ReportSharing model, APIs |
| **Workflow** | Hospital Management | ✅ Implemented | Hospital model, seeding script |
| **Workflow** | Doctor Review System | ✅ Implemented | Review APIs, approval workflow |
| **Workflow** | Notifications | ✅ Implemented | Notification service (future: email/SMS) |
| **Responsiveness** | FastAPI Async | ✅ Implemented | FastAPI, Uvicorn |
| **Responsiveness** | Background Processing | 🔄 Planned | Celery |
| **Data Persistence** | SQL Database | ✅ Implemented | SQLAlchemy, SQLite |
| **Data Persistence** | Vector Database | ✅ Implemented | ChromaDB |
| **Data Persistence** | File Storage | ✅ Implemented | Local Filesystem |
| **Data Persistence** | Cloud Storage | 🔄 Planned | AWS S3/Azure Blob |
| **Security** | JWT Authentication | ✅ Implemented | python-jose |
| **Security** | Password Hashing | ✅ Implemented | bcrypt |
| **Security** | Role-Based Access | ✅ Implemented | OAuth2, JWT Claims |
| **Security** | CORS Configuration | ✅ Implemented | CORSMiddleware |
| **Security** | HTTPS/TLS | 🔄 Planned | SSL Certificates |

---

## Recent Updates & Improvements

### Major Changes

1. **✅ Ollama Integration**: Replaced OpenRouter with local Ollama models for privacy, cost-effectiveness, and offline capability
2. **✅ Specialized AI Models**: Implemented task-specific models (report reading, medicine suggestions, women's health)
3. **✅ Next.js Frontend**: Replaced Streamlit with modern Next.js/React frontend with shadcn/ui
4. **✅ Doctor Portal**: Complete doctor workflow with authentication, dashboard, and review interface
5. **✅ Hospital Management**: Hospital registration and doctor association system
6. **✅ Report Sharing**: Patient-doctor report sharing workflow with notifications
7. **✅ Health Forecasting**: LLM-powered predictive analytics
8. **✅ Enhanced UI**: Charts, animations, markdown support, responsive design
9. **✅ Role-Based Routing**: Separate patient and doctor portals with proper authentication

## Future Enhancements

### Planned Features

1. **Semantic Search**: Query patient history using natural language queries (RAG foundation ready)
2. **Advanced Trend Analysis**: Enhanced visualizations and pattern detection
3. **Multi-Report Comparison**: Compare reports side-by-side
4. **Export Functionality**: Generate PDF summaries and reports
5. **Real-time Notifications**: Push notifications via WebSockets or email/SMS
6. **ABHA Integration**: Full integration with India's health records system
7. **Advanced OCR**: Support for complex formats and handwritten notes
8. **API Analytics**: Usage tracking and performance metrics
9. **Mobile App**: React Native mobile application
10. **Telemedicine Integration**: Video consultations and chat features

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

**Last Updated**: January 2025  
**Version**: 2.0.0

## Changelog

### v2.0.0 (January 2025)
- ✅ Migrated from OpenRouter to Ollama for local LLM processing
- ✅ Implemented specialized AI models (llama3.2, qwen3-vl:2b, medbot, edi, embeddinggemma)
- ✅ Built Next.js/React frontend replacing Streamlit
- ✅ Added complete doctor portal with review workflow
- ✅ Implemented hospital management and doctor association
- ✅ Added report sharing between patients and doctors
- ✅ Integrated health forecasting service
- ✅ Added notification system
- ✅ Enhanced UI with charts, animations, and markdown support
- ✅ Improved authentication with role-based routing

### v1.0.0 (Initial Release)
- Initial FastAPI backend with OpenRouter integration
- Streamlit frontend
- Basic OCR and health marker extraction
- RAG foundation with ChromaDB
