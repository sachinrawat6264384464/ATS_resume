# ResumeIQ — REST API Reference (v1)

Base URL: `http://localhost:8000/api/v1` (or your deployed server domain).

Interactive Swagger documentation is available at `/docs` and ReDoc at `/redoc`.

---

## 1. System Health

### `GET /api/v1/health`
Checks backend service availability, database connectivity, and environment mode.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "app_name": "ResumeIQ - ATS Intelligence Engine",
  "version": "1.0.0",
  "environment": "development",
  "database": "connected"
}
```

---

## 2. Resumes

### `POST /api/v1/resumes/upload`
Uploads and parses a PDF or DOCX resume document. Validates magic bytes, file extension, and size limits (max 10MB).

**Request:** `multipart/form-data`
- `file`: Binary file (`.pdf` or `.docx`).

**Response (200 OK):**
```json
{
  "id": "e2f170e5-7d4e-4b6f-a859-9f79590ff2e2",
  "filename": "John_Doe_Resume.pdf",
  "file_type": "pdf",
  "file_size": 145020,
  "raw_text": "John Doe\nSoftware Engineer...",
  "parsed_data": {
    "contact_info": {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1-555-0199",
      "github": "https://github.com/johndoe",
      "linkedin": "https://linkedin.com/in/johndoe",
      "portfolio": null
    },
    "summary": "Experienced backend engineer...",
    "skills": ["Python", "PostgreSQL", "FastAPI", "Docker"],
    "work_experience": [
      {
        "company": "Acme Tech",
        "role": "Senior Engineer",
        "start_date": "2021-01",
        "end_date": "2024-03",
        "bullets": ["Architected distributed microservices in Python."]
      }
    ],
    "education": [
      {
        "institution": "University of Technology",
        "degree": "Bachelor of Science",
        "field_of_study": "Computer Science",
        "graduation_year": "2020"
      }
    ],
    "projects": []
  },
  "created_at": "2026-11-18T00:00:00Z"
}
```

**Errors:**
- `400 Bad Request`: Invalid magic byte signature or corrupted file.
- `413 Payload Too Large`: File exceeds 10MB limit.

---

### `GET /api/v1/resumes/{resume_id}`
Retrieves stored resume parsing data.

**Response (200 OK):** Same schema as `/upload`.

---

### `DELETE /api/v1/resumes/{resume_id}`
Permanently deletes stored resume record and isolated disk upload.

**Response (200 OK):**
```json
{
  "detail": "Resume e2f170e5-7d4e-4b6f-a859-9f79590ff2e2 deleted successfully."
}
```

---

## 3. Job Descriptions

### `POST /api/v1/jobs`
Decomposes pasted or uploaded JD text into structured requirements.

**Request:** `application/json`
```json
{
  "title": "Senior Backend Engineer",
  "company": "Stripe",
  "raw_text": "We are seeking a Senior Backend Engineer with 5+ years of Python and PostgreSQL experience. Experience with Docker and Kubernetes is required."
}
```

**Response (200 OK):**
```json
{
  "id": "c71a3964-16e7-40b9-b883-d02f5db04207",
  "title": "Senior Backend Engineer",
  "company": "Stripe",
  "raw_text": "...",
  "extracted_data": {
    "title": "Senior Backend Engineer",
    "company": "Stripe",
    "required_skills": ["Python", "PostgreSQL", "Docker", "Kubernetes"],
    "preferred_skills": ["Redis", "Terraform"],
    "experience_years_required": 5.0,
    "education_required": ["Bachelor of Science in Computer Science"],
    "responsibilities": ["Design and scale backend APIs"],
    "qualifications": ["5+ years building distributed systems"]
  },
  "created_at": "2026-11-18T00:00:00Z"
}
```

---

### `PUT /api/v1/jobs/{job_id}`
Allows candidate to manually adjust or fine-tune extracted requirements prior to running ATS analysis.

---

## 4. ATS Multi-Agent Analysis

### `POST /api/v1/analysis`
Dispatches the LangGraph 8-agent analysis workflow in the background (via Celery or FastAPI BackgroundTasks).

**Request:** `application/json`
```json
{
  "resume_id": "e2f170e5-7d4e-4b6f-a859-9f79590ff2e2",
  "job_id": "c71a3964-16e7-40b9-b883-d02f5db04207"
}
```

**Response (200 OK):**
```json
{
  "analysis_id": "f583e74b-65ad-494b-97e3-0c466e31dd4c",
  "status": "processing",
  "progress_percentage": 10,
  "stage": "Starting Pipeline",
  "message": "LangGraph agent workflow dispatched."
}
```

---

### `GET /api/v1/analysis/{analysis_id}/status`
Polls live progress during analysis.

**Response (200 OK):**
```json
{
  "analysis_id": "f583e74b-65ad-494b-97e3-0c466e31dd4c",
  "status": "processing",
  "progress_percentage": 65,
  "stage": "Matching Engine Agent",
  "message": "Computing local BGE-small dense embeddings..."
}
```

---

### `GET /api/v1/analysis/{analysis_id}/report`
Retrieves the comprehensive ATS audit report once completed.

**Response (200 OK):** Contains complete `scoring` breakdown, `matched_skills`, `missing_skills`, `related_skills`, `mandatory_missing_skills`, `experience_evaluation`, `education_evaluation`, and fact-grounded `recommendations`.

---

## 5. PDF Audit Export

### `GET /api/v1/reports/{analysis_id}/pdf`
Downloads an audit-ready, high-resolution PDF report generated deterministically with ReportLab.

**Response (200 OK):**
- `Content-Type: application/pdf`
- `Content-Disposition: attachment; filename="ResumeIQ_Report_{analysis_id}.pdf"`

