from typing import Dict, Any, List, Optional


class ScoringEngine:
    """Configurable, explainable ATS Scoring Engine with empirical component breakdowns."""

    DEFAULT_WEIGHTS = {
        "keyword": 0.40,
        "semantic": 0.25,
        "experience": 0.20,
        "project": 0.10,
        "education": 0.05
    }

    VERSION = "v1.0.0"

    @classmethod
    def evaluate(
        cls,
        keyword_score: float,
        semantic_score: float,
        experience_score: float,
        project_score: float,
        education_score: float,
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        w = weights or cls.DEFAULT_WEIGHTS

        # Ensure weights sum to 1.0
        total_w = sum(w.values())
        norm_w = {k: v / total_w for k, v in w.items()}

        overall = (
            keyword_score * norm_w["keyword"] +
            semantic_score * norm_w["semantic"] +
            experience_score * norm_w["experience"] +
            project_score * norm_w["project"] +
            education_score * norm_w["education"]
        )

        overall = round(min(100.0, max(0.0, overall)), 1)

        # Grade classification
        if overall >= 85.0:
            rating = "Exceptional Match"
            badge = "high"
        elif overall >= 70.0:
            rating = "Strong Match"
            badge = "good"
        elif overall >= 55.0:
            rating = "Moderate Match"
            badge = "medium"
        else:
            rating = "Low Alignment"
            badge = "low"

        return {
            "overall": overall,
            "keyword": round(keyword_score, 1),
            "semantic": round(semantic_score, 1),
            "experience": round(experience_score, 1),
            "project": round(project_score, 1),
            "education": round(education_score, 1),
            "weights": norm_w,
            "rating": rating,
            "badge": badge,
            "version": cls.VERSION
        }

    @classmethod
    def compute_education_score(
        cls,
        candidate_education: List[Dict[str, Any]],
        jd_required_education: List[str]
    ) -> float:
        if not jd_required_education:
            return 100.0

        if not candidate_education:
            return 30.0  # Partial credit if self-taught or non-traditional background

        candidate_degrees = [
            (e.get("degree") or "").lower() for e in candidate_education
        ]

        # Degree rank hierarchy
        degree_ranks = {
            "phd": 4, "doctorate": 4,
            "master": 3, "m.s": 3, "m.tech": 3, "mba": 3,
            "bachelor": 2, "b.s": 2, "b.tech": 2, "undergraduate": 2,
            "associate": 1, "diploma": 1
        }

        def get_max_rank(degree_strings: List[str]) -> int:
            max_r = 0
            for s in degree_strings:
                for k, r in degree_ranks.items():
                    if k in s.lower():
                        max_r = max(max_r, r)
            return max_r

        candidate_rank = get_max_rank(candidate_degrees)
        required_rank = get_max_rank(jd_required_education)

        if required_rank == 0:
            return 100.0

        if candidate_rank >= required_rank:
            return 100.0
        elif candidate_rank == required_rank - 1:
            return 75.0
        else:
            return 50.0

    @classmethod
    def compute_project_score(
        cls,
        candidate_projects: List[Dict[str, Any]],
        jd_technical_tools: List[str],
        bm25_score: float
    ) -> float:
        if not candidate_projects:
            # If no explicit projects section, rely on BM25 experience score
            return round(min(100.0, max(30.0, bm25_score * 0.8)), 1)

        project_texts = []
        for p in candidate_projects:
            project_texts.append(" ".join(p.get("description", [])) + " " + (p.get("title") or ""))

        combined = " ".join(project_texts).lower()

        # Count how many JD tools are applied in projects
        matched = 0
        total = len(jd_technical_tools) if jd_technical_tools else 1

        for tool in jd_technical_tools:
            if tool.lower() in combined:
                matched += 1

        tool_ratio = min(1.0, matched / total)
        # Blend tool presence (60%) with BM25 relevance (40%)
        project_score = (tool_ratio * 60.0) + (min(100.0, bm25_score) * 0.40)
        return round(min(100.0, max(0.0, project_score)), 1)

