import uuid
import pytest
import httpx
from app.graph.orchestrator import ats_pipeline
from app.main import app
from app.api.v1.analysis import run_pipeline_sync
from app.core.database import SessionLocal
from app.models.models import Resume, ParsedResume, JobDescription, Analysis


def test_langgraph_pipeline_execution():
    initial_state = {
        "analysis_id": f"test-analysis-{uuid.uuid4()}",
        "resume_id": f"test-res-{uuid.uuid4()}",
        "job_id": f"test-job-{uuid.uuid4()}",
        "resume_file": None,
        "resume_text": "Experienced Python developer with 4 years building APIs in FastAPI, PostgreSQL, and Docker.",
        "parsed_resume": {
            "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Git"],
            "work_experience": [
                {
                    "title": "Backend Engineer",
                    "company": "Tech Labs",
                    "start_date": "Jan 2021",
                    "end_date": "Present",
                    "description": ["Engineered scalable REST services using FastAPI and PostgreSQL."]
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Science",
                    "institution": "State University",
                    "graduation_year": "2020"
                }
            ],
            "projects": [
                {
                    "title": "Data Pipeline",
                    "description": ["Streamed data with Redis and Docker."]
                }
            ],
            "certifications": [],
            "summary": "Senior Python Backend Engineer.",
            "contact_info": {"name": "Jordan Lee", "email": "jordan@example.com"},
            "raw_text": "Experienced Python developer with 4 years building APIs in FastAPI, PostgreSQL, and Docker."
        },
        "job_description": "We need a Senior Python Engineer with 3+ years experience, FastAPI, and PostgreSQL. Docker is preferred.",
        "parsed_job": {
            "title": "Senior Python Engineer",
            "required_skills": ["Python", "FastAPI", "PostgreSQL"],
            "preferred_skills": ["Docker", "Kubernetes"],
            "experience_years_required": 3.0,
            "education_required": ["Bachelor's degree"],
            "responsibilities": ["Build scalable APIs."],
            "technical_tools": ["Python", "FastAPI", "PostgreSQL", "Docker"]
        },
        "normalized_skills": [],
        "keyword_matches": {},
        "semantic_matches": {},
        "bm25_matches": {},
        "experience_analysis": {},
        "scoring_result": {},
        "recommendations": [],
        "validation_result": {},
        "final_report": {},
        "errors": [],
        "processing_status": "in_progress",
        "stage": "Starting",
        "progress_percentage": 10
    }

    result = ats_pipeline.invoke(initial_state)

    assert result["processing_status"] == "completed"
    assert result["validation_result"]["is_valid"] is True
    assert "final_report" in result

    report = result["final_report"]
    assert report["scores"]["overall"] >= 70.0
    assert report["scores"]["keyword"] >= 80.0
    assert len(report["matched_skills"]) >= 3
    assert len(report["recommendations"]) >= 1


@pytest.mark.asyncio
async def test_analysis_api_workflow():
    db = SessionLocal()
    res_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())

    # Create test resume and job
    res = Resume(
        id=res_id,
        filename="jordan.pdf",
        file_type="pdf",
        file_size=2048,
        raw_text="Python and FastAPI developer."
    )
    db.add(res)
    parsed_res = ParsedResume(
        resume_id=res_id,
        contact_info={"name": "Jordan", "email": "jordan@test.com"},
        skills=["Python", "FastAPI", "PostgreSQL"],
        work_experience=[{"title": "Dev", "start_date": "2020", "end_date": "2023", "description": ["FastAPI code"]}],
        education=[],
        projects=[],
        certifications=[],
        achievements=[],
        languages=[],
        technical_tools=["Python", "FastAPI"]
    )
    db.add(parsed_res)

    job = JobDescription(
        id=job_id,
        title="Python Engineer",
        raw_text="Need Python and PostgreSQL developer with 2 years experience.",
        extracted_data={
            "title": "Python Engineer",
            "required_skills": ["Python", "PostgreSQL"],
            "preferred_skills": [],
            "experience_years_required": 2.0,
            "education_required": [],
            "responsibilities": [],
            "technical_tools": ["Python", "PostgreSQL"]
        }
    )
    db.add(job)
    db.commit()
    db.close()

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Start analysis
        create_res = await client.post("/api/v1/analysis", json={
            "resume_id": res_id,
            "job_id": job_id
        })
        assert create_res.status_code == 200, create_res.text
        analysis_id = create_res.json()["analysis_id"]

        # Run pipeline directly
        run_pipeline_sync(analysis_id, res_id, job_id)

        # Check status
        status_res = await client.get(f"/api/v1/analysis/{analysis_id}/status")
        assert status_res.status_code == 200
        assert status_res.json()["status"] == "completed"

        # Check report
        rep_res = await client.get(f"/api/v1/analysis/{analysis_id}/report")
        assert rep_res.status_code == 200
        report = rep_res.json()
        assert report["status"] == "completed"
        assert report["scores"]["overall"] > 0
        assert len(report["matched_skills"]) > 0
