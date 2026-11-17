from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None


class WorkExperienceItem(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: bool = False
    duration_months: int = 0
    description: List[str] = []
    technologies: List[str] = []


class EducationItem(BaseModel):
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[str] = None
    gpa: Optional[str] = None


class ProjectItem(BaseModel):
    title: Optional[str] = None
    description: List[str] = []
    technologies: List[str] = []
    link: Optional[str] = None


class ParsedResumeResponse(BaseModel):
    id: str
    resume_id: str
    contact_info: ContactInfo
    summary: Optional[str] = None
    skills: List[str] = []
    work_experience: List[WorkExperienceItem] = []
    education: List[EducationItem] = []
    projects: List[ProjectItem] = []
    certifications: List[str] = []
    achievements: List[str] = []
    languages: List[str] = []
    technical_tools: List[str] = []
    extraction_confidence: float = 1.0
    warnings: List[str] = []


class ResumeUploadResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: int
    created_at: datetime
    message: str
    parsed_data: Optional[ParsedResumeResponse] = None

