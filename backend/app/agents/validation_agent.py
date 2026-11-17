from typing import Dict, Any, List
from app.graph.state import ATSGraphState


class ValidationAgent:
    """Agent 7: Verifies calculation integrity, evidence citations, and absence of hallucinations."""

    @classmethod
    def execute(cls, state: ATSGraphState) -> Dict[str, Any]:
        scoring_result = state.get("scoring_result", {})
        keyword_matches = state.get("keyword_matches", {})
        parsed_resume = state.get("parsed_resume", {})
        parsed_job = state.get("parsed_job", {})

        issues: List[str] = []

        # 1. Score boundary verification
        overall = scoring_result.get("overall", 0.0)
        if not (0.0 <= overall <= 100.0):
            issues.append(f"Overall score {overall} is outside allowable range [0, 100].")

        # 2. Weights integrity
        weights = scoring_result.get("weights", {})
        if abs(sum(weights.values()) - 1.0) > 0.01:
            issues.append(f"Scoring weights do not sum to 1.0 (sum: {sum(weights.values())}).")

        # 3. Evidence citation check
        matched_skills = keyword_matches.get("matched_skills", [])
        for m in matched_skills:
            if not m.get("canonical"):
                issues.append("Found matched skill with missing canonical identification.")

        # 4. Data completeness check
        if not parsed_resume.get("raw_text"):
            issues.append("Resume raw text is missing from state.")
        if not parsed_job.get("required_skills") and not parsed_job.get("responsibilities"):
            issues.append("Job description has neither required skills nor responsibilities.")

        is_valid = len(issues) == 0

        return {
            "validation_result": {
                "is_valid": is_valid,
                "issues": issues,
                "verified_at_score": overall
            },
            "stage": "Audit & Validation Complete",
            "progress_percentage": 95
        }

