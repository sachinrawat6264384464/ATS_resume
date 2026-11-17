from datetime import datetime, timezone
from typing import Dict, Any
from app.graph.state import ATSGraphState


class ReportGenerationAgent:
    """Agent 8: Assembles the comprehensive, structured ATS report."""

    @classmethod
    def execute(cls, state: ATSGraphState) -> Dict[str, Any]:
        scoring_result = state.get("scoring_result", {})
        keyword_matches = state.get("keyword_matches", {})
        semantic_matches = state.get("semantic_matches", {})
        experience_analysis = state.get("experience_analysis", {})
        recommendations = state.get("recommendations", [])
        validation_result = state.get("validation_result", {})
        parsed_resume = state.get("parsed_resume", {})
        parsed_job = state.get("parsed_job", {})

        report = {
            "analysis_id": state["analysis_id"],
            "resume_id": state["resume_id"],
            "job_id": state["job_id"],
            "status": "completed",
            "scores": {
                "overall": scoring_result.get("overall", 0.0),
                "keyword": scoring_result.get("keyword", 0.0),
                "semantic": scoring_result.get("semantic", 0.0),
                "experience": scoring_result.get("experience", 0.0),
                "project": scoring_result.get("project", 0.0),
                "education": scoring_result.get("education", 0.0),
                "weights": scoring_result.get("weights", {}),
                "rating": scoring_result.get("rating", "Evaluated")
            },
            "matched_skills": keyword_matches.get("matched_skills", []),
            "missing_skills": keyword_matches.get("missing_preferred", []) + keyword_matches.get("missing_mandatory", []),
            "missing_mandatory": [m["canonical"] for m in keyword_matches.get("missing_mandatory", [])],
            "related_skills": keyword_matches.get("related_skills", []),
            "experience_analysis": experience_analysis,
            "semantic_details": semantic_matches.get("matches", [])[:10],
            "recommendations": recommendations,
            "candidate_name": parsed_resume.get("contact_info", {}).get("name") or "Candidate",
            "job_title": parsed_job.get("title") or "Target Role",
            "scoring_version": scoring_result.get("version", "v1.0.0"),
            "validation": validation_result,
            "completed_at": datetime.now(timezone.utc).isoformat()
        }

        return {
            "final_report": report,
            "processing_status": "completed",
            "stage": "Report Ready",
            "progress_percentage": 100
        }
