from typing import Dict, Any
from app.graph.state import ATSGraphState
from app.parsers.jd_parser import JobDescriptionParser


class JDAnalyzerAgent:
    """Agent 2: Parses JD, identifies required vs preferred skills, experience, and responsibilities."""

    @classmethod
    def execute(cls, state: ATSGraphState) -> Dict[str, Any]:
        parsed_job = state.get("parsed_job") or {}
        job_desc = state.get("job_description", "")

        if parsed_job and parsed_job.get("required_skills"):
            return {
                "parsed_job": parsed_job,
                "stage": "Job Description Analyzed",
                "progress_percentage": 30
            }

        if job_desc:
            try:
                result = JobDescriptionParser.parse(job_desc)
                return {
                    "parsed_job": result,
                    "stage": "Job Description Analyzed",
                    "progress_percentage": 30
                }
            except Exception as e:
                return {
                    "errors": state.get("errors", []) + [f"JDAnalyzerAgent error: {str(e)}"],
                    "processing_status": "failed"
                }

        return {
            "parsed_job": parsed_job,
            "stage": "Job Description Verified",
            "progress_percentage": 30
        }

