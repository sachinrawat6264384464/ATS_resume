from typing import Dict, Any
from app.graph.state import ATSGraphState
from app.parsers.resume_parser import ResumeParser


class ResumeParserAgent:
    """Agent 1: Ingests, parses, and validates resume sections and entities."""

    @classmethod
    def execute(cls, state: ATSGraphState) -> Dict[str, Any]:
        resume_file = state.get("resume_file")
        parsed_resume = state.get("parsed_resume") or {}

        # If already parsed from upload, ensure all fields exist
        if parsed_resume and parsed_resume.get("skills"):
            return {
                "parsed_resume": parsed_resume,
                "resume_text": parsed_resume.get("raw_text") or state.get("resume_text", ""),
                "stage": "Resume Parsed",
                "progress_percentage": 15
            }

        # Otherwise parse from file if provided
        if resume_file:
            ext = resume_file.split(".")[-1].lower()
            try:
                result = ResumeParser.parse_document(resume_file, ext)
                return {
                    "parsed_resume": result,
                    "resume_text": result["raw_text"],
                    "stage": "Resume Parsed",
                    "progress_percentage": 15
                }
            except Exception as e:
                return {
                    "errors": state.get("errors", []) + [f"ResumeParserAgent error: {str(e)}"],
                    "processing_status": "failed"
                }

        return {
            "parsed_resume": parsed_resume,
            "stage": "Resume Verified",
            "progress_percentage": 15
        }
