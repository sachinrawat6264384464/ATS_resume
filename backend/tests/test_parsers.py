import pytest
from app.parsers.section_detector import SectionDetector
from app.parsers.jd_parser import JobDescriptionParser
from app.parsers.resume_parser import ResumeParser


def test_section_detector():
    sample_text = """
John Doe
Software Engineer
john.doe@example.com

PROFESSIONAL SUMMARY
Experienced backend engineer specializing in high-performance APIs and distributed systems.

TECHNICAL SKILLS
Python, FastAPI, PostgreSQL, Docker, Redis, Kubernetes

WORK EXPERIENCE
Senior Software Engineer - Acme Corp
Jan 2021 - Present
- Designed and scaled microservices handling 10M requests daily.
- Implemented vector similarity search with pgvector.

EDUCATION
B.S. in Computer Science
University of California, 2020
"""
    sections = SectionDetector.partition_sections(sample_text)
    assert "summary" in sections
    assert "skills" in sections
    assert "work_experience" in sections
    assert "education" in sections
    assert "Acme Corp" in sections["work_experience"]


def test_jd_parser():
    sample_jd = """
Senior Python Backend Developer
Stripe Inc.

About the job
We are seeking an experienced Senior Python Backend Developer to lead our core billing platform.

Responsibilities:
- Build and maintain highly scalable RESTful microservices.
- Optimize database performance and implement caching strategies.
- Collaborate with frontend engineers to ship reliable features.

Minimum Qualifications:
- 4+ years of experience with Python and web frameworks (FastAPI, Django).
- Strong proficiency in PostgreSQL and database query optimization.
- Bachelor's degree in Computer Science or equivalent.
- Experience with Docker and container orchestration.

Preferred Qualifications:
- Familiarity with Kafka or distributed streaming.
- Kubernetes deployment experience.
"""
    parsed = JobDescriptionParser.parse(sample_jd)
    assert parsed["experience_years_required"] == 4.0
    assert len(parsed["education_required"]) > 0
    assert any("Bachelor" in edu for edu in parsed["education_required"])
    assert len(parsed["responsibilities"]) >= 2
    assert len(parsed["required_skills"]) > 0
    assert len(parsed["preferred_skills"]) > 0


def test_contact_info_extraction():
    header = """
Jane Smith
Senior Cloud Architect
jane.smith@techcorp.io | +1 (555) 234-5678 | San Francisco, CA
https://linkedin.com/in/janesmith | https://github.com/janesmith
"""
    contact = ResumeParser._extract_contact_info(header, header)
    assert contact["email"] == "jane.smith@techcorp.io"
    assert contact["name"] == "Jane Smith"
    assert "555" in contact["phone"]
    assert "linkedin.com/in/janesmith" in contact["linkedin"]
    assert "github.com/janesmith" in contact["github"]

