import re
from typing import Dict, Any, List, Optional


class JobDescriptionParser:
    """Parses and decomposes job descriptions into structured requirements and expectations."""

    REQUIRED_PATTERNS = [
        r"(?:minimum|required|basic)\s+qualifications?",
        r"^requirements?",
        r"what\s+you('ll|\s+will)\s+need",
        r"must\s+haves?",
        r"who\s+you\s+are",
        r"required\s+skills?"
    ]

    PREFERRED_PATTERNS = [
        r"preferred\s+qualifications?",
        r"nice\s+to\s+haves?",
        r"bonus\s+(skills?|points?)",
        r"preferred\s+skills?",
        r"what\s+gives\s+you\s+an\s+edge",
        r"desired\s+skills?"
    ]

    RESPONSIBILITIES_PATTERNS = [
        r"responsibilities?",
        r"what\s+you('ll|\s+will)\s+do",
        r"the\s+role",
        r"key\s+duties",
        r"about\s+the\s+job"
    ]

    # Supports: "5+ years of experience", "5+ years of software engineering experience", "3-5 years relevant experience", "10 years experience"
    EXPERIENCE_REGEX = r"(\d{1,2}(?:\.\d+)?)\s*(?:\+|-|\s+to\s+\d{1,2})?\s*years?(?:\s+of)?(?:\s+[a-zA-Z\s]{1,30})?\s+experience"

    EDUCATION_PATTERNS = [
        r"\b(?:Bachelor(?:'s)?|B\.?S\.?|B\.?A\.?|B\.?Tech|undergraduate)\b",
        r"\b(?:Master(?:'s)?|M\.?S\.?|M\.?A\.?|M\.?Tech|graduate)\b",
        r"\b(?:Ph\.?D\.?|Doctorate)\b",
        r"\b(?:Associate(?:'s)?|Diploma)\b"
    ]

    KNOWN_TECH_TOKENS = {
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang", "rust",
        "react", "react.js", "next.js", "vue", "angular", "node", "node.js",
        "fastapi", "django", "flask", "spring", "express", "graphql", "rest", "api", "apis",
        "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch", "sql", "nosql",
        "docker", "kubernetes", "k8s", "aws", "gcp", "azure", "ci/cd", "git", "linux", "terraform",
        "kafka", "rabbitmq", "celery", "spark", "hadoop", "airflow",
        "pytorch", "tensorflow", "scikit-learn", "nlp", "llm", "rag", "embeddings", "vector"
    }

    @classmethod
    def parse(cls, raw_text: str, title: Optional[str] = None, company: Optional[str] = None) -> Dict[str, Any]:
        if not raw_text.strip():
            return {
                "title": title,
                "company": company,
                "required_skills": [],
                "preferred_skills": [],
                "experience_years_required": 0.0,
                "education_required": [],
                "responsibilities": [],
                "qualifications": [],
                "technical_tools": []
            }

        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

        detected_title = title
        if not detected_title and lines:
            first_line = lines[0]
            if len(first_line.split()) <= 6 and not any(w in first_line.lower() for w in ["requirement", "description", "about"]):
                detected_title = first_line

        sections: Dict[str, List[str]] = {
            "required": [],
            "preferred": [],
            "responsibilities": [],
            "other": []
        }

        current_section = "other"

        for line in lines:
            line_clean = re.sub(r"[:\-_|]+$", "", line).strip().lower()
            if any(re.search(pat, line_clean) for pat in cls.PREFERRED_PATTERNS) and len(line) < 50:
                current_section = "preferred"
                continue
            elif any(re.search(pat, line_clean) for pat in cls.REQUIRED_PATTERNS) and len(line) < 50:
                current_section = "required"
                continue
            elif any(re.search(pat, line_clean) for pat in cls.RESPONSIBILITIES_PATTERNS) and len(line) < 50:
                current_section = "responsibilities"
                continue

            sections[current_section].append(line)

        # Experience years required
        exp_match = re.search(cls.EXPERIENCE_REGEX, raw_text, re.I)
        experience_years = float(exp_match.group(1)) if exp_match else 0.0

        # Education requirements
        education_found: List[str] = []
        for pat in cls.EDUCATION_PATTERNS:
            match = re.search(pat, raw_text, re.I)
            if match and match.group(0) not in education_found:
                education_found.append(match.group(0))

        # Skill extraction
        required_text = "\n".join(sections["required"]) if sections["required"] else raw_text
        preferred_text = "\n".join(sections["preferred"])

        required_skills = cls._extract_candidate_skills(required_text)
        preferred_skills = cls._extract_candidate_skills(preferred_text)

        responsibilities = [
            re.sub(r"^[-*•–\s]+", "", l).strip()
            for l in sections["responsibilities"]
            if len(l) > 15
        ][:15]

        qualifications = [
            re.sub(r"^[-*•–\s]+", "", l).strip()
            for l in sections["required"]
            if len(l) > 15
        ][:15]

        return {
            "title": detected_title,
            "company": company,
            "required_skills": required_skills[:35],
            "preferred_skills": preferred_skills[:20],
            "experience_years_required": experience_years,
            "education_required": education_found,
            "responsibilities": responsibilities,
            "qualifications": qualifications,
            "technical_tools": required_skills[:20]
        }

    @classmethod
    def _extract_candidate_skills(cls, text: str) -> List[str]:
        if not text.strip():
            return []

        extracted: List[str] = []

        tokens = re.split(r"[,•|\n/;()]+", text)
        for t in tokens:
            cleaned = re.sub(r"^[^\w]+|[^\w]+$", "", t).strip()
            if 2 <= len(cleaned) <= 30 and len(cleaned.split()) <= 3:
                lower = cleaned.lower()
                if not lower.startswith(("we ", "you ", "the ", "must ", "have ", "with ", "ability ", "strong ", "years ", "including ")):
                    if cleaned not in extracted:
                        extracted.append(cleaned)

        words = re.findall(r"[a-zA-Z0-9+#.-]+", text)
        for w in words:
            w_clean = re.sub(r"^[^\w]+|[^\w]+$", "", w).strip()
            if w_clean.lower() in cls.KNOWN_TECH_TOKENS:
                proper_term = w_clean.capitalize() if w_clean.islower() else w_clean
                if proper_term not in extracted and not any(proper_term.lower() == e.lower() for e in extracted):
                    extracted.append(proper_term)

        return extracted
