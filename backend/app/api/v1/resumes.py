import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import Resume, ParsedResume
from app.schemas.resume import ResumeUploadResponse, ParsedResumeResponse, ContactInfo, WorkExperienceItem, EducationItem, ProjectItem
from app.parsers.resume_parser import ResumeParser
from app.core.security import validate_file_content, sanitize_text

router = APIRouter()


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Securely uploads, validates, extracts, and parses a candidate resume."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected for upload.")

    content = await file.read()
    ext = validate_file_content(file.filename, content)
    resume_id = str(uuid.uuid4())
    stored_filename = f"{resume_id}.{ext}"
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    stored_filepath = os.path.join(settings.UPLOAD_DIR, stored_filename)

    with open(stored_filepath, "wb") as f:
        f.write(content)

    # Parse resume document
    try:
        parsed_result = ResumeParser.parse_document(stored_filepath, ext)
    except Exception as e:
        if os.path.exists(stored_filepath):
            os.remove(stored_filepath)
        raise HTTPException(status_code=422, detail=f"Failed to parse resume document: {str(e)}")

    # Persist in DB
    resume_record = Resume(
        id=resume_id,
        filename=file.filename,
        file_type=ext,
        file_size=len(content),
        file_path=stored_filepath,
        raw_text=sanitize_text(parsed_result["raw_text"]),
        is_processed=True
    )
    db.add(resume_record)

    parsed_record = ParsedResume(
        resume_id=resume_id,
        contact_info=parsed_result["contact_info"],
        summary=parsed_result["summary"],
        skills=parsed_result["skills"],
        work_experience=parsed_result["work_experience"],
        education=parsed_result["education"],
        projects=parsed_result["projects"],
        certifications=parsed_result["certifications"],
        achievements=parsed_result["achievements"],
        languages=parsed_result["languages"],
        technical_tools=parsed_result["technical_tools"],
        extraction_confidence=parsed_result["extraction_confidence"],
        warnings=parsed_result["warnings"]
    )
    db.add(parsed_record)
    db.commit()
    db.refresh(resume_record)
    db.refresh(parsed_record)

    parsed_response = ParsedResumeResponse(
        id=parsed_record.id,
        resume_id=parsed_record.resume_id,
        contact_info=ContactInfo(**parsed_record.contact_info),
        summary=parsed_record.summary,
        skills=parsed_record.skills,
        work_experience=[WorkExperienceItem(**item) for item in parsed_record.work_experience],
        education=[EducationItem(**item) for item in parsed_record.education],
        projects=[ProjectItem(**item) for item in parsed_record.projects],
        certifications=parsed_record.certifications,
        achievements=parsed_record.achievements,
        languages=parsed_record.languages,
        technical_tools=parsed_record.technical_tools,
        extraction_confidence=parsed_record.extraction_confidence,
        warnings=parsed_record.warnings
    )

    return ResumeUploadResponse(
        id=resume_record.id,
        filename=resume_record.filename,
        file_type=resume_record.file_type,
        file_size=resume_record.file_size,
        created_at=resume_record.created_at,
        message="Resume successfully uploaded and parsed.",
        parsed_data=parsed_response
    )


@router.get("/{resume_id}", response_model=ResumeUploadResponse)
def get_resume(resume_id: str, db: Session = Depends(get_db)):
    """Retrieves resume record and structured parsed entities."""
    resume_record = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume_record:
        raise HTTPException(status_code=404, detail="Resume not found.")

    parsed_record = resume_record.parsed_resume
    parsed_response = None
    if parsed_record:
        parsed_response = ParsedResumeResponse(
            id=parsed_record.id,
            resume_id=parsed_record.resume_id,
            contact_info=ContactInfo(**parsed_record.contact_info),
            summary=parsed_record.summary,
            skills=parsed_record.skills,
            work_experience=[WorkExperienceItem(**item) for item in parsed_record.work_experience],
            education=[EducationItem(**item) for item in parsed_record.education],
            projects=[ProjectItem(**item) for item in parsed_record.projects],
            certifications=parsed_record.certifications,
            achievements=parsed_record.achievements,
            languages=parsed_record.languages,
            technical_tools=parsed_record.technical_tools,
            extraction_confidence=parsed_record.extraction_confidence,
            warnings=parsed_record.warnings
        )

    return ResumeUploadResponse(
        id=resume_record.id,
        filename=resume_record.filename,
        file_type=resume_record.file_type,
        file_size=resume_record.file_size,
        created_at=resume_record.created_at,
        message="Resume found.",
        parsed_data=parsed_response
    )


@router.delete("/{resume_id}")
def delete_resume(resume_id: str, db: Session = Depends(get_db)):
    """Deletes uploaded resume and purges stored file for privacy."""
    resume_record = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume_record:
        raise HTTPException(status_code=404, detail="Resume not found.")

    if resume_record.file_path and os.path.exists(resume_record.file_path):
        try:
            os.remove(resume_record.file_path)
        except OSError:
            pass

    db.delete(resume_record)
    db.commit()
    return {"message": "Resume and related parsed data purged successfully."}
