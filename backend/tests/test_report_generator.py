import pytest
from app.services.pdf_report_generator import PDFReportGenerator


def test_generate_pdf_report_structure():
    report_data = {
        "analysis_id": "test-pdf-123",
        "resume_name": "John_Doe_Resume.pdf",
        "job_title": "Senior Python Backend Engineer",
        "job_company": "Acme Tech Labs",
        "created_at": "2026-11-18T00:00:00Z",
        "scoring": {
            "overall_score": 84.5,
            "keyword_match_score": 88.0,
            "semantic_match_score": 82.0,
            "experience_match_score": 85.0,
            "project_match_score": 80.0,
            "education_match_score": 90.0,
            "scoring_version": "v1.0.0-heuristic",
            "weights_used": {
                "keyword": 0.40,
                "semantic": 0.25,
                "experience": 0.20,
                "project": 0.10,
                "education": 0.05,
            },
        },
        "mandatory_missing": ["Docker", "Kubernetes"],
        "skill_matches": [
            {
                "skill": "Python",
                "status": "matched",
                "evidence_type": "demonstrated_in_experience",
                "is_mandatory": True,
                "confidence": 0.95,
                "context_snippet": "5 years building Python services",
            },
            {
                "skill": "FastAPI",
                "status": "matched",
                "evidence_type": "demonstrated_in_projects",
                "is_mandatory": True,
                "confidence": 0.90,
                "context_snippet": "Architected FastAPI microservices",
            },
            {
                "skill": "Docker",
                "status": "missing",
                "evidence_type": "missing",
                "is_mandatory": True,
                "confidence": 0.0,
                "context_snippet": None,
            },
        ],
        "experience": {
            "candidate_years": 4.5,
            "required_years": 5.0,
            "gap_years": 0.5,
            "meets_experience": True,
        },
        "education": {
            "matches_required": True,
            "candidate_degrees": ["Bachelor of Science in Computer Science"],
            "required_degrees": ["Bachelor in Computer Science or related"],
        },
        "recommendations": [
            {
                "id": "rec-1",
                "category": "weak_bullet",
                "original_text": "Worked on backend bugs",
                "suggested_text": "Resolved 40+ high-priority backend latency issues in production Python services",
                "reasoning": "Strengthen with action verbs and specific technical scope",
                "priority": "high",
            },
            {
                "id": "rec-2",
                "category": "missing_keyword",
                "suggested_text": "Add Docker containerization evidence to your cloud deployment section",
                "reasoning": "Docker is a mandatory skill mentioned in the job requirements",
                "priority": "high",
            },
        ],
    }

    pdf_bytes = PDFReportGenerator.generate(report_data)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    # PDF magic bytes
    assert pdf_bytes.startswith(b"%PDF-")
