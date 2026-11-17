import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.parsers.pdf_parser import PDFParser
from app.parsers.docx_parser import DocxParser
from app.parsers.section_detector import SectionDetector


class ResumeParser:
    """Full-featured resume extraction and structured entity extraction."""

    # Common email regex
    EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    
    # Phone regex covering global & US/India formats
    PHONE_REGEX = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+?\d{10,14}"
    
    # Date formats (e.g. "Jan 2021 - Present", "05/2019 - 08/2022", "2018 - 2021")
    DATE_RANGE_REGEX = r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}|\d{1,2}/\d{4}|\d{4})\s*(?:–|-|to)\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}|\d{1,2}/\d{4}|\d{4}|Present|Current|Now)"

    # Common degrees
    DEGREES_PATTERN = r"\b(Bachelor(?:'s)?|Master(?:'s)?|B\.?S\.?|M\.?S\.?|B\.?A\.?|M\.?A\.?|B\.?Tech\.?|M\.?Tech\.?|Ph\.?D\.?|MBA|Associate(?:'s)?|Diploma)\b"

    @classmethod
    def parse_document(cls, file_path: str, file_type: str) -> Dict[str, Any]:
        """Extracts text and parses structured resume entities."""
        warnings: List[str] = []
        raw_text = ""

        if file_type.lower() == "pdf":
            pdf_data = PDFParser.extract(file_path)
            raw_text = pdf_data["raw_text"]
            warnings.extend(pdf_data.get("warnings", []))
            if pdf_data.get("is_two_column"):
                warnings.append("Multi-column layout detected; parsed using positional geometry.")
        elif file_type.lower() in ["docx", "doc"]:
            docx_data = DocxParser.extract(file_path)
            raw_text = docx_data["raw_text"]
            warnings.extend(docx_data.get("warnings", []))
        else:
            raise ValueError(f"Unsupported file format: {file_type}")

        if not raw_text.strip():
            warnings.append("Document text is empty or non-extractable.")
            return cls._empty_parsed_result(raw_text, warnings)

        # Partition sections
        sections = SectionDetector.partition_sections(raw_text)

        # Extract entities
        contact_info = cls._extract_contact_info(sections.get("header", ""), raw_text)
        summary = sections.get("summary", "").strip() or None
        skills = cls._extract_skills(sections.get("skills", ""), raw_text)
        work_experience = cls._extract_work_experience(sections.get("work_experience", ""))
        education = cls._extract_education(sections.get("education", ""))
        projects = cls._extract_projects(sections.get("projects", ""))
        certifications = cls._extract_simple_list(sections.get("certifications", ""))
        achievements = cls._extract_simple_list(sections.get("achievements", ""))
        languages = cls._extract_simple_list(sections.get("languages", ""))

        # Confidence calculation
        confidence = 1.0
        if not contact_info.get("email"):
            confidence -= 0.15
            warnings.append("Could not reliably identify candidate email.")
        if not contact_info.get("name"):
            confidence -= 0.1
            warnings.append("Could not determine candidate full name.")
        if not work_experience:
            confidence -= 0.2
            warnings.append("No explicit work experience section could be parsed.")
        if not skills:
            confidence -= 0.15
            warnings.append("No explicit skills section found; extracted from experience text.")

        confidence = max(0.2, round(confidence, 2))

        return {
            "raw_text": raw_text,
            "contact_info": contact_info,
            "summary": summary,
            "skills": skills,
            "work_experience": work_experience,
            "education": education,
            "projects": projects,
            "certifications": certifications,
            "achievements": achievements,
            "languages": languages,
            "technical_tools": skills,  # normalized subset
            "extraction_confidence": confidence,
            "warnings": warnings
        }

    @classmethod
    def _extract_contact_info(cls, header_text: str, full_text: str) -> Dict[str, Optional[str]]:
        text_to_search = header_text if len(header_text) > 30 else full_text[:1200]

        # Email
        email_match = re.search(cls.EMAIL_REGEX, text_to_search)
        email = email_match.group(0) if email_match else None

        # Phone
        phone_match = re.search(cls.PHONE_REGEX, text_to_search)
        phone = phone_match.group(0).strip() if phone_match else None

        # Links
        linkedin = None
        linkedin_match = re.search(r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_\-]+", text_to_search, re.I)
        if linkedin_match:
            linkedin = linkedin_match.group(0)

        github = None
        github_match = re.search(r"(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_\-]+", text_to_search, re.I)
        if github_match:
            github = github_match.group(0)

        portfolio = None
        portfolio_match = re.search(r"(?:https?:\/\/)?(?:www\.)?[a-zA-Z0-9\-]+\.(?:dev|me|io|tech|app)(?:\/[^\s]*)?", text_to_search, re.I)
        if portfolio_match:
            portfolio = portfolio_match.group(0)

        # Name heuristic: First non-empty line of header, <= 4 words, letters only
        name = None
        for line in header_text.splitlines():
            line = line.strip()
            if not line:
                continue
            # Skip if it contains email or phone or URLs
            if "@" in line or "http" in line or re.search(r"\d{3}", line):
                continue
            words = line.split()
            if 1 <= len(words) <= 4 and all(re.match(r"^[a-zA-Z\.\'-]+$", w) for w in words):
                name = line
                break

        # Fallback to first line of full text if no name in header
        if not name:
            for line in full_text.splitlines()[:5]:
                line = line.strip()
                if line and not ("@" in line or "http" in line or re.search(r"\d{3}", line)):
                    words = line.split()
                    if 1 <= len(words) <= 4 and all(re.match(r"^[a-zA-Z\.\'-]+$", w) for w in words):
                        name = line
                        break

        # Location heuristic (e.g. City, State / Country)
        location = None
        loc_match = re.search(r"([A-Z][a-zA-Z\s]+,\s*[A-Z]{2}\b|[A-Z][a-zA-Z\s]+,\s*(?:USA|India|Canada|UK|Germany|Singapore|Australia))", text_to_search)
        if loc_match:
            location = loc_match.group(1).strip()

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "linkedin": linkedin,
            "github": github,
            "portfolio": portfolio
        }

    @classmethod
    def _extract_skills(cls, skills_section: str, full_text: str) -> List[str]:
        source = skills_section if len(skills_section.strip()) > 10 else full_text
        extracted: List[str] = []

        # Common delimiters in skills sections: commas, bullets, pipes, slashes, newlines
        tokens = re.split(r"[,•|\n/]+", source)
        for t in tokens:
            cleaned = re.sub(r"^[^\w]+|[^\w]+$", "", t).strip()
            if cleaned and 2 <= len(cleaned) <= 35:
                # Avoid long sentence fragments
                if len(cleaned.split()) <= 4 and not cleaned.lower().startswith(("responsible", "experience", "worked")):
                    if cleaned not in extracted:
                        extracted.append(cleaned)

        return extracted[:50]

    @classmethod
    def _extract_work_experience(cls, experience_section: str) -> List[Dict[str, Any]]:
        if not experience_section.strip():
            return []

        jobs: List[Dict[str, Any]] = []
        lines = [l.strip() for l in experience_section.splitlines() if l.strip()]

        current_job: Dict[str, Any] = {
            "title": None,
            "company": None,
            "location": None,
            "start_date": None,
            "end_date": None,
            "is_current": False,
            "duration_months": 0,
            "description": [],
            "technologies": []
        }

        for line in lines:
            # Check for date range
            date_match = re.search(cls.DATE_RANGE_REGEX, line, re.I)
            if date_match:
                # If we already have a job with bullets, push it
                if current_job["title"] or current_job["description"]:
                    jobs.append(current_job)
                    current_job = {
                        "title": None,
                        "company": None,
                        "location": None,
                        "start_date": None,
                        "end_date": None,
                        "is_current": False,
                        "duration_months": 0,
                        "description": [],
                        "technologies": []
                    }

                current_job["start_date"] = date_match.group(1).strip()
                current_job["end_date"] = date_match.group(2).strip()
                current_job["is_current"] = any(w in current_job["end_date"].lower() for w in ["present", "current", "now"])

                # The remainder of the line might have title or company
                remainder = line[:date_match.start()] + " " + line[date_match.end():]
                remainder = re.sub(r"[|\-–,]+", " ", remainder).strip()
                if remainder and not current_job["title"]:
                    current_job["title"] = remainder

            elif line.startswith(("-", "*", "•", "–")) or len(line) > 60:
                clean_bullet = re.sub(r"^[-*•–\s]+", "", line).strip()
                current_job["description"].append(clean_bullet)
            else:
                if not current_job["title"]:
                    current_job["title"] = line
                elif not current_job["company"]:
                    current_job["company"] = line
                else:
                    current_job["description"].append(line)

        if current_job["title"] or current_job["description"]:
            jobs.append(current_job)

        return jobs

    @classmethod
    def _extract_education(cls, education_section: str) -> List[Dict[str, Any]]:
        if not education_section.strip():
            return []

        records: List[Dict[str, Any]] = []
        lines = [l.strip() for l in education_section.splitlines() if l.strip()]

        for line in lines:
            deg_match = re.search(cls.DEGREES_PATTERN, line, re.I)
            year_match = re.search(r"\b(19\d{2}|20\d{2})\b", line)
            gpa_match = re.search(r"\bGPA[:\s]*([0-4]\.\d{1,2}|[0-9]\.\d{1,2}\s*/\s*10)\b", line, re.I)

            if deg_match or year_match or any(w in line.lower() for w in ["university", "college", "institute", "school"]):
                records.append({
                    "degree": deg_match.group(0) if deg_match else "Degree/Coursework",
                    "field_of_study": None,
                    "institution": line,
                    "graduation_year": year_match.group(0) if year_match else None,
                    "gpa": gpa_match.group(1) if gpa_match else None
                })

        return records

    @classmethod
    def _extract_projects(cls, projects_section: str) -> List[Dict[str, Any]]:
        if not projects_section.strip():
            return []

        projects: List[Dict[str, Any]] = []
        lines = [l.strip() for l in projects_section.splitlines() if l.strip()]

        current_proj: Dict[str, Any] = {
            "title": None,
            "description": [],
            "technologies": [],
            "link": None
        }

        for line in lines:
            url_match = re.search(r"https?://[^\s]+", line)
            if url_match:
                current_proj["link"] = url_match.group(0)

            if line.startswith(("-", "*", "•", "–")) or len(line) > 60:
                clean_bullet = re.sub(r"^[-*•–\s]+", "", line).strip()
                current_proj["description"].append(clean_bullet)
            else:
                if current_proj["title"] and current_proj["description"]:
                    projects.append(current_proj)
                    current_proj = {"title": line, "description": [], "technologies": [], "link": None}
                elif not current_proj["title"]:
                    current_proj["title"] = line

        if current_proj["title"] or current_proj["description"]:
            projects.append(current_proj)

        return projects

    @classmethod
    def _extract_simple_list(cls, section_text: str) -> List[str]:
        if not section_text.strip():
            return []
        items = []
        for line in section_text.splitlines():
            line = re.sub(r"^[-*•–\s]+", "", line).strip()
            if line and len(line) < 120:
                items.append(line)
        return items

    @classmethod
    def _empty_parsed_result(cls, raw_text: str, warnings: List[str]) -> Dict[str, Any]:
        return {
            "raw_text": raw_text,
            "contact_info": {},
            "summary": None,
            "skills": [],
            "work_experience": [],
            "education": [],
            "projects": [],
            "certifications": [],
            "achievements": [],
            "languages": [],
            "technical_tools": [],
            "extraction_confidence": 0.0,
            "warnings": warnings
        }
