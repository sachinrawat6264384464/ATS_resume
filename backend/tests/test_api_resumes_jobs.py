import io
import pytest
import httpx
from app.main import app
import fitz  # PyMuPDF


def create_sample_pdf_bytes() -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    text = """
Alex Mercer
alex.mercer@gmail.com | +1 (555) 789-0123 | New York, NY
https://linkedin.com/in/alexmercer | https://github.com/alexmercer

PROFESSIONAL SUMMARY
Senior Backend Engineer with 5+ years of experience designing robust microservices and distributed database architectures.

TECHNICAL SKILLS
Python, FastAPI, Django, PostgreSQL, Redis, Docker, Kubernetes, AWS, Git, CI/CD

WORK EXPERIENCE
Lead Backend Engineer - Fintech Innovations
Jan 2021 - Present
- Architected high-throughput payment transaction pipelines handling over 15M queries daily.
- Implemented real-time anomaly detection with Redis caching, reducing API latency by 45%.

Software Engineer - Cloud Systems
Jun 2018 - Dec 2020
- Built and maintained scalable RESTful microservices using Python and PostgreSQL.
- Deployed containerized applications onto AWS ECS using Docker.

EDUCATION
B.S. in Computer Science
Columbia University, 2018
GPA: 3.8 / 4.0
"""
    page.insert_text((50, 72), text, fontsize=11)
    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes


@pytest.mark.asyncio
async def test_upload_resume_api():
    pdf_bytes = create_sample_pdf_bytes()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        files = {
            "file": ("alex_mercer_resume.pdf", pdf_bytes, "application/pdf")
        }
        response = await client.post("/api/v1/resumes/upload", files=files)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["filename"] == "alex_mercer_resume.pdf"
        assert data["parsed_data"]["contact_info"]["name"] == "Alex Mercer"
        assert data["parsed_data"]["contact_info"]["email"] == "alex.mercer@gmail.com"
        assert len(data["parsed_data"]["work_experience"]) >= 1
        assert len(data["parsed_data"]["skills"]) > 0

        # Test retrieve
        resume_id = data["id"]
        get_res = await client.get(f"/api/v1/resumes/{resume_id}")
        assert get_res.status_code == 200
        assert get_res.json()["id"] == resume_id


@pytest.mark.asyncio
async def test_create_and_update_job_api():
    sample_jd_text = """
Staff Backend Platform Engineer
Airbnb

Responsibilities:
- Build fault-tolerant distributed services using Python and Go.
- Lead the architecture of our cloud-native event processing pipeline.

Minimum Qualifications:
- 5+ years of software engineering experience.
- Deep expertise in PostgreSQL, Redis, and message queues.
- Bachelor's or Master's in Computer Science or related field.

Preferred Qualifications:
- Experience with Kubernetes and Terraform.
- Microservices scalability at scale.
"""
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Create JD
        res = await client.post("/api/v1/jobs", json={
            "raw_text": sample_jd_text,
            "title": "Staff Backend Platform Engineer",
            "company": "Airbnb"
        })
        assert res.status_code == 200, res.text
        jd = res.json()
        job_id = jd["id"]
        assert jd["title"] == "Staff Backend Platform Engineer"
        assert jd["extracted_data"]["experience_years_required"] == 5.0
        assert len(jd["extracted_data"]["required_skills"]) > 0

        # Update JD (manual adjustment)
        updated_extracted = jd["extracted_data"]
        updated_extracted["required_skills"].append("Apache Kafka")
        put_res = await client.put(f"/api/v1/jobs/{job_id}", json=updated_extracted)
        assert put_res.status_code == 200
        assert "Apache Kafka" in put_res.json()["extracted_data"]["required_skills"]
