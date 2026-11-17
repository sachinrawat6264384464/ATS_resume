from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class AnalysisCreate(BaseModel):
    resume_id: str
    job_id: str


class ScoreBreakdown(BaseModel):
    overall: float
    keyword: float
    semantic: float
    experience: float
    project: float
    education: float
    weights: Dict[str, float]


class MatchedSkillItem(BaseModel):
    canonical: str
    category: str
    found_in_resume: str
    confidence: float
    evidence: str


class MissingSkillItem(BaseModel):
    canonical: str
    category: str
    is_mandatory: bool
    context: str


class RelatedSkillItem(BaseModel):
    required: str
    candidate_possesses: str
    category: str
    relevance_note: str


class RecommendationItem(BaseModel):
    id: str
    category: str
    priority: str
    original_text: Optional[str] = None
    suggested_text: Optional[str] = None
    reasoning: str


class AnalysisStatusResponse(BaseModel):
    analysis_id: str
    status: str  # pending, processing, completed, failed
    progress_percentage: int
    stage: str
    message: Optional[str] = None
    error: Optional[str] = None


class AnalysisReportResponse(BaseModel):
    analysis_id: str
    resume_id: str
    job_id: str
    status: str
    scores: ScoreBreakdown
    matched_skills: List[MatchedSkillItem]
    missing_skills: List[MissingSkillItem]
    missing_mandatory: List[str]
    related_skills: List[RelatedSkillItem]
    experience_analysis: Dict[str, Any]
    recommendations: List[RecommendationItem]
    scoring_version: str
    created_at: datetime
    completed_at: Optional[datetime] = None

