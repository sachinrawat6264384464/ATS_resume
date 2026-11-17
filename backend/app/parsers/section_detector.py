import re
from typing import Dict, List, Tuple, Optional


class SectionDetector:
    """Detects and partitions standard resume sections using heuristic keyword patterns."""

    SECTION_PATTERNS = {
        "summary": [
            r"^professional\s+summary",
            r"^executive\s+summary",
            r"^summary",
            r"^profile",
            r"^about\s+me",
            r"^career\s+objective",
            r"^objective"
        ],
        "skills": [
            r"^technical\s+skills",
            r"^core\s+competencies",
            r"^skills\s+(&|and)\s+(tools|technologies)",
            r"^skills",
            r"^technologies",
            r"^technical\s+proficiencies",
            r"^tools\s+(&|and)\s+technologies",
            r"^areas\s+of\s+expertise"
        ],
        "work_experience": [
            r"^work\s+experience",
            r"^professional\s+experience",
            r"^employment\s+history",
            r"^work\s+history",
            r"^experience",
            r"^relevant\s+experience",
            r"^career\s+history"
        ],
        "education": [
            r"^education(\s+(&|and)\s+qualifications)?",
            r"^academic\s+background",
            r"^academic\s+history",
            r"^degrees",
            r"^qualifications"
        ],
        "projects": [
            r"^personal\s+projects",
            r"^academic\s+projects",
            r"^key\s+projects",
            r"^technical\s+projects",
            r"^featured\s+projects",
            r"^projects"
        ],
        "certifications": [
            r"^certifications?",
            r"^licenses?\s+(&|and)\s+certifications?",
            r"^professional\s+certifications?",
            r"^accreditations?"
        ],
        "achievements": [
            r"^achievements?",
            r"^honors?\s+(&|and)\s+awards?",
            r"^awards?\s+(&|and)\s+honors?",
            r"^key\s+achievements?",
            r"^publications?"
        ],
        "languages": [
            r"^languages?",
            r"^language\s+proficiency"
        ]
    }

    @classmethod
    def match_heading(cls, line: str) -> Optional[str]:
        cleaned = line.strip().lower()
        # Strip trailing colons or dashes
        cleaned = re.sub(r"[:\-_|]+$", "", cleaned).strip()

        # If line is too long, it's not a heading
        if len(cleaned) > 45 or len(cleaned) < 3:
            return None

        for section_name, patterns in cls.SECTION_PATTERNS.items():
            for pat in patterns:
                if re.match(pat, cleaned):
                    return section_name
        return None

    @classmethod
    def partition_sections(cls, raw_text: str) -> Dict[str, str]:
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        sections: Dict[str, List[str]] = {
            "header": [],
            "summary": [],
            "skills": [],
            "work_experience": [],
            "education": [],
            "projects": [],
            "certifications": [],
            "achievements": [],
            "languages": [],
            "other": []
        }

        current_section = "header"

        for line in lines:
            detected = cls.match_heading(line)
            if detected:
                current_section = detected
            else:
                sections[current_section].append(line)

        return {k: "\n".join(v).strip() for k, v in sections.items() if v}
