import re
from typing import Dict, Any, List, Optional
from app.nlp.skill_taxonomy import SkillTaxonomy


class EvidenceClassifier:
    """Classifies candidate skills by empirical proof level (Experience, Projects, Certs, or Skill List)."""

    EVIDENCE_WEIGHTS = {
        "demonstrated_in_experience": 1.0,
        "demonstrated_in_projects": 0.85,
        "mentioned_in_certifications": 0.80,
        "mentioned_in_skills": 0.60,
        "related_skill": 0.40,
        "missing": 0.0
    }

    @classmethod
    def classify_skill(
        cls,
        skill_name: str,
        work_experience: List[Dict[str, Any]],
        projects: List[Dict[str, Any]],
        certifications: List[str],
        skills_list: List[str]
    ) -> Dict[str, Any]:
        canonical, category = SkillTaxonomy.normalize_skill(skill_name)
        escaped = re.escape(canonical)
        regex = rf"(?:\b|_){escaped}(?:\b|_)"

        # 1. Search in Work Experience
        for job in work_experience:
            combined_desc = " ".join(job.get("description", [])) + " " + (job.get("title") or "")
            if re.search(regex, combined_desc, re.I):
                return {
                    "skill": skill_name,
                    "canonical": canonical,
                    "category": category,
                    "evidence_level": "demonstrated_in_experience",
                    "weight": cls.EVIDENCE_WEIGHTS["demonstrated_in_experience"],
                    "provenance": f"Demonstrated in work experience at {job.get('company') or 'company'} ({job.get('title') or 'role'}).",
                    "snippet": combined_desc[:250]
                }

        # 2. Search in Projects
        for proj in projects:
            combined_proj = " ".join(proj.get("description", [])) + " " + (proj.get("title") or "")
            if re.search(regex, combined_proj, re.I):
                return {
                    "skill": skill_name,
                    "canonical": canonical,
                    "category": category,
                    "evidence_level": "demonstrated_in_projects",
                    "weight": cls.EVIDENCE_WEIGHTS["demonstrated_in_projects"],
                    "provenance": f"Demonstrated in project '{proj.get('title') or 'portfolio project'}'.",
                    "snippet": combined_proj[:250]
                }

        # 3. Search in Certifications
        for cert in certifications:
            if re.search(regex, cert, re.I):
                return {
                    "skill": skill_name,
                    "canonical": canonical,
                    "category": category,
                    "evidence_level": "mentioned_in_certifications",
                    "weight": cls.EVIDENCE_WEIGHTS["mentioned_in_certifications"],
                    "provenance": f"Validated by certification: {cert}.",
                    "snippet": cert
                }

        # 4. Search in Skills List
        for s in skills_list:
            if canonical == SkillTaxonomy.normalize_skill(s)[0]:
                return {
                    "skill": skill_name,
                    "canonical": canonical,
                    "category": category,
                    "evidence_level": "mentioned_in_skills",
                    "weight": cls.EVIDENCE_WEIGHTS["mentioned_in_skills"],
                    "provenance": "Listed in skills section without explicit project or work experience bullet.",
                    "snippet": s
                }

        # 5. Missing
        return {
            "skill": skill_name,
            "canonical": canonical,
            "category": category,
            "evidence_level": "missing",
            "weight": cls.EVIDENCE_WEIGHTS["missing"],
            "provenance": "No explicit evidence found in resume.",
            "snippet": None
        }

