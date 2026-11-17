import re
import uuid
from typing import Dict, Any, List
from app.graph.state import ATSGraphState


class ResumeImprovementAgent:
    """Agent 6: Formulates factual, non-hallucinatory bullet improvements and keyword alignment suggestions."""

    ACTION_VERB_REPLACEMENTS = {
        "worked on": ["engineered", "developed", "architected", "delivered"],
        "responsible for": ["spearheaded", "directed", "managed", "orchestrated"],
        "helped": ["collaborated to build", "facilitated", "contributed to"],
        "handled": ["resolved", "managed", "executed", "oversaw"],
        "did": ["implemented", "executed", "deployed"],
        "made": ["designed", "constructed", "formulated"]
    }

    @classmethod
    def execute(cls, state: ATSGraphState) -> Dict[str, Any]:
        parsed_resume = state.get("parsed_resume", {})
        keyword_matches = state.get("keyword_matches", {})
        missing_mandatory = keyword_matches.get("missing_mandatory", [])
        work_experience = parsed_resume.get("work_experience", [])

        recommendations: List[Dict[str, Any]] = []

        # 1. Missing Critical Keywords Suggestions
        if missing_mandatory:
            top_missing = [m["canonical"] for m in missing_mandatory[:4]]
            recommendations.append({
                "id": str(uuid.uuid4()),
                "category": "keyword",
                "priority": "high",
                "original_text": None,
                "suggested_text": f"Incorporate verifiable experience with: {', '.join(top_missing)}.",
                "reasoning": "These are explicitly listed as required minimum qualifications in the target job posting."
            })

        # 2. Bullet Point Action-Verb Enhancements
        for job in work_experience:
            for bullet in job.get("description", []):
                bullet_lower = bullet.lower()
                for weak_phrase, strong_verbs in cls.ACTION_VERB_REPLACEMENTS.items():
                    if bullet_lower.startswith(weak_phrase) or f" {weak_phrase} " in bullet_lower:
                        # Replace while keeping the exact factual contents
                        pattern = re.compile(re.escape(weak_phrase), re.IGNORECASE)
                        suggested = pattern.sub(strong_verbs[0].capitalize(), bullet, count=1)
                        recommendations.append({
                            "id": str(uuid.uuid4()),
                            "category": "bullet_point",
                            "priority": "medium",
                            "original_text": bullet,
                            "suggested_text": suggested,
                            "reasoning": f"Replace passive phrasing '{weak_phrase}' with high-impact executive action verb '{strong_verbs[0]}'."
                        })
                        break

        # 3. Measurable Impact Suggestion if bullets lack numbers
        has_metrics = False
        for job in work_experience:
            for bullet in job.get("description", []):
                if re.search(r"\b(\d+[%kKmM]?|\$\d+)\b", bullet):
                    has_metrics = True
                    break

        if not has_metrics and work_experience:
            recommendations.append({
                "id": str(uuid.uuid4()),
                "category": "formatting",
                "priority": "medium",
                "original_text": None,
                "suggested_text": "Quantify outcomes in your experience bullets (e.g. latency reduced by X%, team size led, requests handled).",
                "reasoning": "ATS scoring algorithms and hiring managers favor evidence with measurable scale and quantifiable impact."
            })

        # 4. Professional Summary Recommendation if missing
        if not parsed_resume.get("summary"):
            recommendations.append({
                "id": str(uuid.uuid4()),
                "category": "structure",
                "priority": "low",
                "original_text": None,
                "suggested_text": "Add a 2-3 line Professional Summary highlighting your years of experience, core stack, and target specialization.",
                "reasoning": "A concise summary provides immediate contextual grounding for semantic ATS parsing."
            })

        return {
            "recommendations": recommendations,
            "stage": "Actionable Improvements Formulated",
            "progress_percentage": 90
        }
