from typing import Dict, Any, List
from app.graph.state import ATSGraphState
from app.matching.keyword_matcher import KeywordMatcher
from app.matching.bm25_matcher import BM25Matcher
from app.matching.semantic_matcher import SemanticMatcher
from app.matching.experience_matcher import ExperienceMatcher
from app.matching.evidence_classifier import EvidenceClassifier


class MatchingAgent:
    """Agent 4: Runs multi-modal ATS matching algorithms (Keyword, BM25, Semantic BGE, and Experience)."""

    @classmethod
    def execute(cls, state: ATSGraphState) -> Dict[str, Any]:
        parsed_resume = state.get("parsed_resume", {})
        parsed_job = state.get("parsed_job", {})
        resume_text = state.get("resume_text", "")

        resume_skills = parsed_resume.get("skills", [])
        jd_required = parsed_job.get("required_skills", [])
        jd_preferred = parsed_job.get("preferred_skills", [])
        work_experience = parsed_resume.get("work_experience", [])
        projects = parsed_resume.get("projects", [])
        certifications = parsed_resume.get("certifications", [])

        # 1. Exact & Alias Keyword Matching
        keyword_result = KeywordMatcher.match(
            resume_skills=resume_skills,
            resume_raw_text=resume_text,
            jd_required_skills=jd_required,
            jd_preferred_skills=jd_preferred
        )

        # 2. Enrich matched skills with evidence spans
        for m in keyword_result["matched_skills"]:
            evidence_info = EvidenceClassifier.classify_skill(
                skill_name=m["canonical"],
                work_experience=work_experience,
                projects=projects,
                certifications=certifications,
                skills_list=resume_skills
            )
            m["evidence_level"] = evidence_info["evidence_level"]
            m["evidence_weight"] = evidence_info["weight"]
            m["provenance"] = evidence_info["provenance"]
            m["snippet"] = evidence_info["snippet"]

        # 3. BM25 Section Relevance
        resume_sections = {
            "summary": parsed_resume.get("summary") or "",
            "work_experience": "\n".join([" ".join(j.get("description", [])) for j in work_experience]),
            "projects": "\n".join([" ".join(p.get("description", [])) for p in projects]),
            "skills": ", ".join(resume_skills)
        }
        bm25_result = BM25Matcher.match(
            resume_sections=resume_sections,
            jd_requirements=jd_required + jd_preferred,
            jd_responsibilities=parsed_job.get("responsibilities", [])
        )

        # 4. Dense Semantic Embedding Matching (BGE-small)
        resume_chunks = [
            chunk.strip()
            for chunk in resume_text.splitlines()
            if len(chunk.strip()) > 30
        ][:25]
        if not resume_chunks:
            resume_chunks = [resume_text[:400]]

        semantic_result = SemanticMatcher.match(
            resume_chunks=resume_chunks,
            jd_requirements=(jd_required + parsed_job.get("responsibilities", []))[:15]
        )

        # 5. Experience Matching
        exp_required = parsed_job.get("experience_years_required", 0.0)
        experience_result = ExperienceMatcher.match(work_experience, exp_required)

        return {
            "keyword_matches": keyword_result,
            "bm25_matches": bm25_result,
            "semantic_matches": semantic_result,
            "experience_analysis": experience_result,
            "stage": "Multi-Modal ATS Matching Executed",
            "progress_percentage": 65
        }
