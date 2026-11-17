from typing import Dict, Any, List
from app.graph.state import ATSGraphState
from app.nlp.skill_taxonomy import SkillTaxonomy


class SkillIntelligenceAgent:
    """Agent 3: Normalizes skills, resolves aliases, categorizes, and identifies related technologies."""

    @classmethod
    def execute(cls, state: ATSGraphState) -> Dict[str, Any]:
        parsed_resume = state.get("parsed_resume", {})
        raw_skills = parsed_resume.get("skills", [])

        normalized_list: List[Dict[str, Any]] = []
        for s in raw_skills:
            canonical, category = SkillTaxonomy.normalize_skill(s)
            related = SkillTaxonomy.get_related_skills(canonical)
            normalized_list.append({
                "original": s,
                "canonical": canonical,
                "category": category,
                "related": related
            })

        return {
            "normalized_skills": normalized_list,
            "stage": "Skills Normalized & Categorized",
            "progress_percentage": 45
        }

