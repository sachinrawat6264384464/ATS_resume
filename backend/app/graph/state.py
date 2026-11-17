from typing import TypedDict, Dict, Any, List, Optional


class ATSGraphState(TypedDict):
    analysis_id: str
    resume_id: str
    job_id: str
    resume_file: Optional[str]
    resume_text: str
    parsed_resume: Dict[str, Any]
    job_description: str
    parsed_job: Dict[str, Any]
    normalized_skills: List[Dict[str, Any]]
    keyword_matches: Dict[str, Any]
    semantic_matches: Dict[str, Any]
    bm25_matches: Dict[str, Any]
    experience_analysis: Dict[str, Any]
    scoring_result: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    validation_result: Dict[str, Any]
    final_report: Dict[str, Any]
    errors: List[str]
    processing_status: str
    stage: str
    progress_percentage: int

