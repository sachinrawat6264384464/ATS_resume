import re
from typing import Dict, Any, List, Set, Tuple
from app.nlp.skill_taxonomy import SkillTaxonomy


class KeywordMatcher:
    """Exact keyword and canonical skill matching engine with substring guardrails."""

    @classmethod
    def match(
        cls,
        resume_skills: List[str],
        resume_raw_text: str,
        jd_required_skills: List[str],
        jd_preferred_skills: List[str]
    ) -> Dict[str, Any]:
        resume_text_lower = resume_raw_text.lower()

        # Build candidate canonical skills inventory
        candidate_canonical_map: Dict[str, str] = {}  # canonical -> original text
        for s in resume_skills:
            canonical, category = SkillTaxonomy.normalize_skill(s)
            candidate_canonical_map[canonical] = s

        # Also scan resume text for known taxonomy terms that might not be in explicit skill list
        for term, category in SkillTaxonomy.TAXONOMY.items():
            if term not in candidate_canonical_map:
                # Safe regex boundary match
                escaped = re.escape(term)
                pattern = rf"(?:\b|_){escaped}(?:\b|_)"
                if re.search(pattern, resume_text_lower):
                    candidate_canonical_map[term] = term

        matched_skills: List[Dict[str, Any]] = []
        missing_mandatory: List[Dict[str, Any]] = []
        missing_preferred: List[Dict[str, Any]] = []
        related_skills: List[Dict[str, Any]] = []

        # Process Required (Mandatory) Skills
        for req_raw in jd_required_skills:
            req_canonical, category = SkillTaxonomy.normalize_skill(req_raw)

            if req_canonical in candidate_canonical_map:
                matched_skills.append({
                    "canonical": req_canonical,
                    "category": category,
                    "found_in_resume": candidate_canonical_map[req_canonical],
                    "is_mandatory": True,
                    "confidence": 1.0,
                    "evidence": f"Found '{candidate_canonical_map[req_canonical]}' matching required skill '{req_raw}'."
                })
            else:
                # Check if candidate has a related skill
                related_candidates = SkillTaxonomy.get_related_skills(req_canonical)
                found_related = None
                for rel in related_candidates:
                    if rel in candidate_canonical_map:
                        found_related = rel
                        break

                if found_related:
                    related_skills.append({
                        "required": req_canonical,
                        "candidate_possesses": found_related,
                        "category": category,
                        "relevance_note": f"Candidate demonstrates '{found_related}', which is technically related to '{req_canonical}'."
                    })

                missing_mandatory.append({
                    "canonical": req_canonical,
                    "category": category,
                    "is_mandatory": True,
                    "context": f"Required prerequisite '{req_raw}' was not explicitly demonstrated."
                })

        # Process Preferred Skills
        for pref_raw in jd_preferred_skills:
            pref_canonical, category = SkillTaxonomy.normalize_skill(pref_raw)
            if pref_canonical in candidate_canonical_map:
                # If not already added
                if not any(m["canonical"] == pref_canonical for m in matched_skills):
                    matched_skills.append({
                        "canonical": pref_canonical,
                        "category": category,
                        "found_in_resume": candidate_canonical_map[pref_canonical],
                        "is_mandatory": False,
                        "confidence": 0.9,
                        "evidence": f"Found '{candidate_canonical_map[pref_canonical]}' matching preferred skill '{pref_raw}'."
                    })
            else:
                if not any(m["canonical"] == pref_canonical for m in missing_mandatory):
                    missing_preferred.append({
                        "canonical": pref_canonical,
                        "category": category,
                        "is_mandatory": False,
                        "context": f"Preferred skill '{pref_raw}' is absent."
                    })

        # Score computation:
        # Required skills carry 80% weight of keyword score, preferred carry 20%
        # Related skills grant a 40% partial credit towards a missing required skill
        total_req = len(jd_required_skills) if jd_required_skills else 1
        matched_req = len([m for m in matched_skills if m.get("is_mandatory")])
        related_credit = len(related_skills) * 0.4

        req_ratio = min(1.0, (matched_req + related_credit) / total_req)

        total_pref = len(jd_preferred_skills) if jd_preferred_skills else 1
        matched_pref = len([m for m in matched_skills if not m.get("is_mandatory")])
        pref_ratio = min(1.0, matched_pref / total_pref) if jd_preferred_skills else 1.0

        if jd_preferred_skills:
            keyword_score = (req_ratio * 0.8 + pref_ratio * 0.2) * 100.0
        else:
            keyword_score = req_ratio * 100.0

        return {
            "score": round(keyword_score, 1),
            "matched_skills": matched_skills,
            "missing_mandatory": missing_mandatory,
            "missing_preferred": missing_preferred,
            "related_skills": related_skills,
            "total_required": len(jd_required_skills),
            "total_matched": len(matched_skills)
        }

