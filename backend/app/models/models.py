import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Index
)
from sqlalchemy.orm import relationship
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


def get_utc_now():
    return datetime.now(timezone.utc)


class Resume(Base):
    """Uploaded resumes table."""
    __tablename__ = "resumes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  # pdf, docx
    file_size = Column(Integer, nullable=False)
    file_path = Column(String(512), nullable=True)
    raw_text = Column(Text, nullable=True)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    parsed_resume = relationship("ParsedResume", back_populates="resume", uselist=False, cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="resume", cascade="all, delete-orphan")


class ParsedResume(Base):
    """Structured extraction results from resume."""
    __tablename__ = "parsed_resumes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, unique=True)
    contact_info = Column(JSON, nullable=False, default=dict)  # name, email, phone, location, links
    summary = Column(Text, nullable=True)
    skills = Column(JSON, nullable=False, default=list)  # list of extracted skills
    work_experience = Column(JSON, nullable=False, default=list)  # list of jobs with dates, bullets, company
    education = Column(JSON, nullable=False, default=list)  # list of degrees, institutions, graduation dates
    projects = Column(JSON, nullable=False, default=list)  # list of project titles, tech, details
    certifications = Column(JSON, nullable=False, default=list)
    achievements = Column(JSON, nullable=False, default=list)
    languages = Column(JSON, nullable=False, default=list)
    technical_tools = Column(JSON, nullable=False, default=list)
    extraction_confidence = Column(Float, default=1.0)
    warnings = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    resume = relationship("Resume", back_populates="parsed_resume")


class JobDescription(Base):
    """Job descriptions submitted for matching."""
    __tablename__ = "job_descriptions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    raw_text = Column(Text, nullable=False)
    extracted_data = Column(JSON, nullable=False, default=dict)  # required_skills, preferred_skills, experience, etc.
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    analyses = relationship("Analysis", back_populates="job_description", cascade="all, delete-orphan")


class Analysis(Base):
    """Complete ATS Analysis record."""
    __tablename__ = "analyses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(String(36), ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    overall_score = Column(Float, nullable=True)
    keyword_score = Column(Float, nullable=True)
    semantic_score = Column(Float, nullable=True)
    experience_score = Column(Float, nullable=True)
    project_score = Column(Float, nullable=True)
    education_score = Column(Float, nullable=True)
    scoring_version = Column(String(50), default="v1.0.0")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    resume = relationship("Resume", back_populates="analyses")
    job_description = relationship("JobDescription", back_populates="analyses")
    match_detail = relationship("MatchDetail", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="analysis", cascade="all, delete-orphan")


class MatchDetail(Base):
    """Granular match results and evidence spans."""
    __tablename__ = "match_details"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    analysis_id = Column(String(36), ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False, unique=True)
    matched_skills = Column(JSON, nullable=False, default=list)
    missing_skills = Column(JSON, nullable=False, default=list)
    missing_mandatory = Column(JSON, nullable=False, default=list)
    related_skills = Column(JSON, nullable=False, default=list)
    bm25_scores = Column(JSON, nullable=False, default=dict)
    semantic_matches = Column(JSON, nullable=False, default=list)
    experience_analysis = Column(JSON, nullable=False, default=dict)
    evidence_spans = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    analysis = relationship("Analysis", back_populates="match_detail")


class Recommendation(Base):
    """Actionable improvement suggestions for the candidate."""
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    analysis_id = Column(String(36), ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(100), nullable=False)  # keyword, bullet_point, formatting, structure
    original_text = Column(Text, nullable=True)
    suggested_text = Column(Text, nullable=True)
    reasoning = Column(Text, nullable=False)
    priority = Column(String(50), default="medium")  # high, medium, low
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    analysis = relationship("Analysis", back_populates="recommendations")


class EmbeddingRecord(Base):
    """Vector representations stored for sections."""
    __tablename__ = "embeddings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_type = Column(String(50), nullable=False)  # resume, job_description
    source_id = Column(String(36), nullable=False)
    section_name = Column(String(100), nullable=False)
    content_chunk = Column(Text, nullable=False)
    vector = Column(JSON, nullable=False)  # JSON-serialized embedding list
    created_at = Column(DateTime(timezone=True), default=get_utc_now)


class Feedback(Base):
    """Public user feedback on analysis quality."""
    __tablename__ = "feedback"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    analysis_id = Column(String(36), ForeignKey("analyses.id", ondelete="SET NULL"), nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)


class AuditLog(Base):
    """Audit logs for actions and privacy compliance."""
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(36), nullable=True)
    details = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)


class ScoringVersion(Base):
    """Versioned ATS scoring configurations."""
    __tablename__ = "scoring_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    version = Column(String(50), nullable=False, unique=True)
    keyword_weight = Column(Float, default=0.40)
    semantic_weight = Column(Float, default=0.25)
    experience_weight = Column(Float, default=0.20)
    project_weight = Column(Float, default=0.10)
    education_weight = Column(Float, default=0.05)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)


class SkillTaxonomy(Base):
    """Curated skill taxonomy database table."""
    __tablename__ = "skill_taxonomy"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    canonical_name = Column(String(150), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=False, index=True)  # Programming, Framework, Database, etc.
    aliases = Column(JSON, nullable=False, default=list)  # ["python3", "py"]
    related_skills = Column(JSON, nullable=False, default=list)  # ["django", "flask", "fastapi"]
    created_at = Column(DateTime(timezone=True), default=get_utc_now)


class ProcessingJob(Base):
    """Async task tracking and progress reporting."""
    __tablename__ = "processing_jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    analysis_id = Column(String(36), nullable=False, index=True)
    status = Column(String(50), default="queued")  # queued, in_progress, completed, failed
    stage = Column(String(100), default="Initializing")
    progress_percentage = Column(Integer, default=0)
    message = Column(String(255), nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

