from typing import Dict, Any
from app.graph.state import ATSGraphState
from app.matching.scoring_engine import ScoringEngine


class ScoringAgent:
    """Agent 5: Calculates explainable weighted ATS score, category scores, and detects mandatory gaps."""

    @classmethod
    def execute(cls, state: ATSGraphState) -> Dict[str, Any]:
        keyword_data = state.get("keyword_matches", {})
        semantic_data = state.get("semantic_matches", {})
        experience_data = state.get("experience_analysis", {})
        bm25_data = state.get("bm25_matches", {})
        parsed_resume = state.get("parsed_resume", {})
        parsed_job = state.get("parsed_job", {})

        keyword_score = keyword_data.get("score", 0.0)
        semantic_score = semantic_data.get("score", 0.0)
        experience_score = experience_data.get("score", 0.0)
        bm25_score = bm25_data.get("score", 0.0)

        # Compute Project Score
        project_score = ScoringEngine.compute_project_score(
            candidate_projects=parsed_resume.get("projects", []),
            jd_technical_tools=parsed_job.get("technical_tools", []),
            bm25_score=bm25_score
        )

        # Compute Education Score
        education_score = ScoringEngine.compute_education_score(
            candidate_education=parsed_resume.get("education", []),
            jd_required_education=parsed_job.get("education_required", [])
        )

        scoring_result = ScoringEngine.evaluate(
            keyword_score=keyword_score,
            semantic_score=semantic_score,
            experience_score=experience_score,
            project_score=project_score,
            education_score=education_score
        )

        # Flag mandatory gaps impact
        missing_mandatory = keyword_data.get("missing_mandatory", [])
        if missing_mandatory and scoring_result["overall"] > 80.0:
            scoring_result["warning"] = (
                f"Candidate lacks {len(missing_mandatory)} mandatory prerequisite(s). "
                "Recruiters may screen this resume out regardless of the overall match score."
            )

        return {
            "scoring_result": scoring_result,
            "stage": "ATS Score Calculated & Decomposed",
            "progress_percentage": 80
        }
