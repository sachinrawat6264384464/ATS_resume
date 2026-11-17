import pytest
from app.nlp.skill_taxonomy import SkillTaxonomy
from app.matching.keyword_matcher import KeywordMatcher
from app.matching.experience_matcher import ExperienceMatcher
from app.matching.evidence_classifier import EvidenceClassifier
from app.matching.bm25_matcher import BM25Matcher
from app.matching.semantic_matcher import SemanticMatcher


def test_skill_taxonomy_normalization():
    # Test aliases and casing
    canon1, cat1 = SkillTaxonomy.normalize_skill("Postgres")
    assert canon1 == "postgresql"
    assert cat1 == "Databases"

    canon2, cat2 = SkillTaxonomy.normalize_skill("k8s")
    assert canon2 == "kubernetes"
    assert cat2 == "Cloud & DevOps"

    canon3, cat3 = SkillTaxonomy.normalize_skill("ReactJS")
    assert canon3 == "react"
    assert cat3 == "Frontend"

    # Test related skills
    related = SkillTaxonomy.get_related_skills("fastapi")
    assert "django" in related or "flask" in related


def test_keyword_matcher():
    resume_skills = ["Python", "FastAPI", "Postgres", "Docker"]
    resume_text = "Experienced with Python, FastAPI microservices, and PostgreSQL database migrations."
    jd_required = ["Python", "PostgreSQL", "Kubernetes"]
    jd_preferred = ["Docker", "Kafka"]

    result = KeywordMatcher.match(
        resume_skills=resume_skills,
        resume_raw_text=resume_text,
        jd_required_skills=jd_required,
        jd_preferred_skills=jd_preferred
    )

    assert result["score"] > 50.0
    matched_canonicals = [m["canonical"] for m in result["matched_skills"]]
    assert "python" in matched_canonicals
    assert "postgresql" in matched_canonicals
    assert "docker" in matched_canonicals

    # Kubernetes must be in missing mandatory
    missing_mandatory = [m["canonical"] for m in result["missing_mandatory"]]
    assert "kubernetes" in missing_mandatory


def test_experience_deduplication():
    # Concurrent jobs: Jan 2020 to Dec 2021 (24 months) and Jun 2020 to Jun 2021 (12 months, fully overlapping)
    work_experience = [
        {
            "title": "Backend Engineer",
            "company": "Company A",
            "start_date": "Jan 2020",
            "end_date": "Dec 2021"
        },
        {
            "title": "Consultant",
            "company": "Company B",
            "start_date": "Jun 2020",
            "end_date": "Jun 2021"
        }
    ]

    tenure = ExperienceMatcher.calculate_tenure(work_experience)
    assert tenure["has_overlaps"] is True
    # Deduplicated tenure should be ~24 months (2.0 years), NOT 36 months (3.0 years)!
    assert tenure["total_months"] <= 24
    assert tenure["total_years"] == 2.0
    assert tenure["overlap_months_deducted"] >= 11

    # Match against 3 years required
    match_result = ExperienceMatcher.match(work_experience, experience_years_required=3.0)
    assert match_result["candidate_years"] == 2.0
    assert match_result["score"] < 100.0


def test_evidence_classifier():
    work_exp = [{
        "title": "Software Engineer",
        "company": "Stripe",
        "description": ["Implemented microservices using FastAPI and optimized database queries with pgvector."]
    }]
    projects = [{
        "title": "AI Agent Dashboard",
        "description": ["Built frontend with React and TypeScript."]
    }]
    certs = ["AWS Certified Solutions Architect"]
    skills_list = ["Docker", "Kubernetes", "Redis"]

    # 1. FastAPI is in work experience
    ev1 = EvidenceClassifier.classify_skill("FastAPI", work_exp, projects, certs, skills_list)
    assert ev1["evidence_level"] == "demonstrated_in_experience"
    assert ev1["weight"] == 1.0

    # 2. React is in projects
    ev2 = EvidenceClassifier.classify_skill("React", work_exp, projects, certs, skills_list)
    assert ev2["evidence_level"] == "demonstrated_in_projects"
    assert ev2["weight"] == 0.85

    # 3. AWS is in certifications
    ev3 = EvidenceClassifier.classify_skill("AWS", work_exp, projects, certs, skills_list)
    assert ev3["evidence_level"] == "mentioned_in_certifications"

    # 4. Kubernetes is only in skills list
    ev4 = EvidenceClassifier.classify_skill("Kubernetes", work_exp, projects, certs, skills_list)
    assert ev4["evidence_level"] == "mentioned_in_skills"
    assert ev4["weight"] == 0.60

    # 5. Missing
    ev5 = EvidenceClassifier.classify_skill("Rust", work_exp, projects, certs, skills_list)
    assert ev5["evidence_level"] == "missing"
    assert ev5["weight"] == 0.0


def test_bm25_and_semantic_matching():
    resume_sections = {
        "summary": "Full Stack developer specializing in Python and PostgreSQL.",
        "work_experience": "Architected high volume payments with FastAPI and Redis caching.",
        "skills": "Python, FastAPI, PostgreSQL, Redis, Docker"
    }
    requirements = [
        "Strong experience with Python and FastAPI microservices.",
        "Expertise in relational database schema design with PostgreSQL."
    ]
    responsibilities = ["Design fault-tolerant APIs."]

    # Test BM25
    bm25_res = BM25Matcher.match(resume_sections, requirements, responsibilities)
    assert bm25_res["score"] > 0.0
    assert len(bm25_res["top_passages"]) > 0

    # Test Semantic
    chunks = [
        "Full Stack developer specializing in Python and PostgreSQL.",
        "Architected high volume payments with FastAPI and Redis caching."
    ]
    sem_res = SemanticMatcher.match(chunks, requirements)
    assert sem_res["score"] > 0.0
    assert len(sem_res["matches"]) == len(requirements)
