# Technical Specification (SPEC.md)
**Project:** Ebook2LateX

## 1. System Overview

### 1.1 Architecture
*3-tier architecture utilizing Docker for containerization.*
* **Presentation Layer:** React + Vite
* **Application Layer:** FastAPI (Python)
* **Data Layer:** PostgreSQL

### 1.2 Technology Stack
* **Backend:** Python 3.10+, FastAPI, SQLAlchemy (ORM), Alembic (Migrations), PyMuPDF (PDF Processing), pix2tex (OCR).
* **Frontend:** React 18+, **Vite** (Build tool & Dev server), Tailwind CSS, MathLive (Math Editor), Axios.
* **Database:** PostgreSQL 15+.
* **Infrastructure:** Docker, Docker Compose.

### 1.3 System Requirements and Constraints
* System must extract math formulas accurately from PDF files.
* Real-time bidirectional synchronization between LaTeX input and MathLive visual editor.
* Responsive UI for document review and editing.

---

## 2. Database Design

### 2.1 Schema Definition
**Table: `documents`**
* `id`: UUID (Primary Key)
* `filename`: String (255)
* `created_at`: Timestamp (Default: CURRENT_TIMESTAMP)

**Table: `formula_entries`**
* `id`: UUID (Primary Key)
* `document_id`: UUID (Foreign Key -> documents.id)
* `raw_latex`: Text
* `status`: String (Enum: 'pending', 'reviewed', 'submitted')
* `updated_at`: Timestamp

### 2.2 Relationships & Constraints
* One-to-Many relationship: A `document` can have multiple `formula_entries`.
* Foreign key constraint on `formula_entries.document_id` with `ON DELETE CASCADE`.

### 2.3 Indexes for Query Optimization
* Index on `formula_entries.document_id` for fast lookups when fetching formulas for a specific document.

### 2.4 Migration & Seeding Strategy
* Use **Alembic** for managing database schema migrations.
* Include a seeding script (`seed.py`) to inject initial mock data (Sample Document & Formulas) for UI/UX testing before the OCR model is fully integrated.

---

## 3. Backend API Specification

**Base URL:** `/api/v1`

### 3.1 Endpoints
* `POST /upload`
    * **Action:** Upload PDF file.
    * **Response:** Document metadata (ID, filename).
* `POST /process/{document_id}`
    * **Action:** Extract formulas via OCR.
    * **Response:** List of extracted formulas.
* `GET /formulas/{document_id}`
    * **Action:** Retrieve formulas with pagination.
    * **Response:** Paginated JSON list of formula objects.
* `PUT /formulas/{formula_id}`
    * **Action:** Update a single formula's LaTeX content.
    * **Response:** Updated formula object.
* `POST /formulas/batch`
    * **Action:** Batch update formulas (used for the final Submit action).
    * **Payload:** Array of formula objects.
    * **Response:** Success status and updated records count.

### 3.2 Error Handling
* Standardized HTTP status codes (400 Bad Request, 404 Not Found, 500 Internal Server Error).
* Standardized JSON error schema: `{ "error_code": "...", "message": "..." }`.

---

## 4. Backend Data Models

* **SQLAlchemy Models:** Define interface definitions mapping to the PostgreSQL tables (`Document`, `FormulaEntry`).
* **Pydantic Schemas:** Used for API request/response validation (e.g., `DocumentCreate`, `FormulaUpdate`).
* **Service Layer Interfaces:** Separate business logic (PDF processing, OCR invocation) from API route handlers.

---

## 5. Frontend Architecture

### 5.1 Build System & Setup
* **Tooling:** **Vite** is used as the primary build tool to ensure ultra-fast Hot Module Replacement (HMR) during development and optimized, minified bundles for production.

### 5.2 Component Hierarchy and Responsibilities
* `App` (Main Container)
    * `PDFUploader` (File upload component with drag-drop support)
    * `DocumentPreview` (Displays uploaded PDF context)
    * `FormulaList` (Iterates and displays extracted formulas)
        * `FormulaEditorItem` (Wraps editor components for a single formula)
            * `MathLiveEditor` (Interactive visual formula editor)
            * `LaTeXInput` (Raw LaTeX text editor)

### 5.3 State Management Strategy
* Use React `useState` and `useEffect` for local state.
* Custom hook `useFormulaSync` to manage the bidirectional synchronization state between `MathLiveEditor` and `LaTeXInput`.

### 5.4 API Service Layer
* Centralized Axios instance configuring base URL and interceptors for backend communication.

---

## 6. Business Logic Flows

* **Flow 1: Document Processing:** Upload PDF → Save to `uploads/` → Trigger PyMuPDF extraction → Run pix2tex OCR → Return array of LaTeX strings → Display on Frontend.
* **Flow 2: Bidirectional Edit Sync:** Edit formula with LaTeX Input ↔ State Update ↔ MathLive component re-renders (and vice versa).
* **Flow 3: Final Submission:** User clicks "Submit" → Collect all modified formulas → Send payload to `POST /formulas/batch` → Update PostgreSQL DB via SQLAlchemy.

---

## 7. Error Handling & Edge Cases

* **PDF Errors:** Handling files with no formulas, corrupted files, or processing timeouts.
* **OCR Errors:** Handling low confidence scores, model failure, or unsupported mathematical symbols.
* **LaTeX Errors:** Invalid LaTeX syntax input by the user causing MathLive rendering failures.
* **Database Errors:** Connection loss, constraint violations, transaction rollbacks during batch saves.
* **Frontend Edge Cases:** Network timeout during API calls, concurrent edits, drag-and-drop invalid file types.

---

## 8. Configuration & Environment

* **Backend (`.env`):** `DATABASE_URL`, `CORS_ORIGINS`, `MAX_UPLOAD_SIZE`.
* **Frontend (`.env`):** `VITE_API_BASE_URL` (Prefixed with `VITE_` specifically for Vite compatibility).
* **Docker Compose:** Configuration with 3 unified services (`db` for PostgreSQL, `backend` for FastAPI, `frontend` for Vite/React).

---

## 9. Dependencies

* **Backend (`requirements.txt`):** fastapi, uvicorn, sqlalchemy, psycopg2-binary, alembic, pymupdf (fitz), pix2tex, pydantic, python-multipart.
* **Frontend (`package.json`):** react, react-dom, **vite**, mathlive, axios, tailwindcss, postcss, autoprefixer.
* **System Dependencies:** PostgreSQL 15, Python 3.10+, Node.js 18+ (for Vite).

---

## 10. Implementation Roadmap

### Phase 1: Project Initialization, Database & Backend Foundation
* **Tasks:** Initialize Git repository, configure `.gitignore`, set up Docker Compose. Configure PostgreSQL database, write SQLAlchemy models, Alembic migrations, and **Seed Data** script. Setup FastAPI basic structure.

### Phase 2: PDF Processing & OCR Integration
* **Tasks:** Implement `PDFUploader` endpoint. Integrate PyMuPDF for image extraction. Integrate `pix2tex` model for OCR processing.

### Phase 3: Frontend Foundation (Vite) & Components
* **Tasks:** Scaffold frontend application using **Vite**. Configure Tailwind CSS. Build foundational UI components (`PDFUploader`, `FormulaList`).

### Phase 4: MathLive Integration & Sync Logic
* **Tasks:** Integrate `<math-field>`. Implement the bidirectional sync hook (`useFormulaSync.js`). Connect components to handle real-time state updates.

### Phase 5: Integration Testing & Deployment
* **Tasks:** Connect Frontend "Submit" flow to Backend batch save API. Conduct end-to-end testing with complex mathematical PDFs. Finalize Docker orchestration for production.

---

## 11. Critical Files to Create/Modify

**Version Control:**
* `.gitignore` - Exclude `node_modules`, `__pycache__`, `uploads/`, `.env`.

**Backend:**
* `backend/app/models/document.py` & `formula.py` - SQLAlchemy models
* `backend/app/schemas/document.py` & `formula.py` - Pydantic schemas
* `backend/app/api/upload.py`, `process.py`, `formulas.py` - API Endpoints
* `backend/app/services/pdf_processor.py` & `ocr_service.py` - Core logic
* `backend/app/core/config.py` & `database.py` - Configuration
* `backend/requirements.txt`
* `backend/alembic.ini` & `backend/alembic/versions/001_initial.py` - Migrations
* `backend/scripts/seed.py` - **Mock data injection script**

**Frontend:**
* `frontend/vite.config.js` - **Vite configuration file**
* `frontend/src/components/PDFUploader.jsx`
* `frontend/src/components/FormulaList.jsx`
* `frontend/src/components/MathLiveEditor.jsx`
* `frontend/src/components/LaTeXInput.jsx`
* `frontend/src/hooks/useFormulaSync.js`
* `frontend/src/services/api.js`
* `frontend/package.json`
* `frontend/tailwind.config.js` & `postcss.config.js`

**Infrastructure:**
* `docker-compose.yml` - System orchestration
* `backend/Dockerfile`
* `frontend/Dockerfile` - **Configured for Vite multi-stage build or dev server**