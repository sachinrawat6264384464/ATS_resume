from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class JobDescriptionCreate(BaseModel):
    raw_text: str = Field(..., min_length=20, description="Full job description text")
    title: Optional[str] = None
    company: Optional[str] = None


class JobExtractedData(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    experience_years_required: float = 0.0
    education_required: List[str] = []
    responsibilities: List[str] = []
    qualifications: List[str] = []
    technical_tools: List[str] = []


class JobDescriptionResponse(BaseModel):
    id: str
    title: Optional[str] = None
    company: Optional[str] = None
    raw_text: str
    extracted_data: JobExtractedData
    created_at: datetime

