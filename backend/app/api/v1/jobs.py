from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import JobDescription
from app.schemas.job import JobDescriptionCreate, JobDescriptionResponse, JobExtractedData
from app.parsers.jd_parser import JobDescriptionParser
from app.core.security import sanitize_text

router = APIRouter()


@router.post("", response_model=JobDescriptionResponse)
def create_job_description(payload: JobDescriptionCreate, db: Session = Depends(get_db)):
    """Decomposes and stores a target job description."""
    sanitized_text = sanitize_text(payload.raw_text)
    if len(sanitized_text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Job description text is too short to analyze.")

    extracted = JobDescriptionParser.parse(
        raw_text=sanitized_text,
        title=payload.title,
        company=payload.company
    )

    jd_record = JobDescription(
        title=extracted["title"] or payload.title,
        company=extracted["company"] or payload.company,
        raw_text=sanitized_text,
        extracted_data=extracted
    )
    db.add(jd_record)
    db.commit()
    db.refresh(jd_record)

    return JobDescriptionResponse(
        id=jd_record.id,
        title=jd_record.title,
        company=jd_record.company,
        raw_text=jd_record.raw_text,
        extracted_data=JobExtractedData(**jd_record.extracted_data),
        created_at=jd_record.created_at
    )


@router.get("/{job_id}", response_model=JobDescriptionResponse)
def get_job_description(job_id: str, db: Session = Depends(get_db)):
    """Retrieves parsed job description details."""
    jd_record = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not jd_record:
        raise HTTPException(status_code=404, detail="Job description not found.")

    return JobDescriptionResponse(
        id=jd_record.id,
        title=jd_record.title,
        company=jd_record.company,
        raw_text=jd_record.raw_text,
        extracted_data=JobExtractedData(**jd_record.extracted_data),
        created_at=jd_record.created_at
    )


@router.put("/{job_id}", response_model=JobDescriptionResponse)
def update_job_description(job_id: str, updated_data: JobExtractedData, db: Session = Depends(get_db)):
    """Allows candidates to manually review, edit, and fine-tune extracted requirements before analysis."""
    jd_record = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not jd_record:
        raise HTTPException(status_code=404, detail="Job description not found.")

    merged_data = jd_record.extracted_data.copy()
    merged_data.update(updated_data.model_dump())

    jd_record.title = updated_data.title or jd_record.title
    jd_record.company = updated_data.company or jd_record.company
    jd_record.extracted_data = merged_data

    db.commit()
    db.refresh(jd_record)

    return JobDescriptionResponse(
        id=jd_record.id,
        title=jd_record.title,
        company=jd_record.company,
        raw_text=jd_record.raw_text,
        extracted_data=JobExtractedData(**jd_record.extracted_data),
        created_at=jd_record.created_at
    )


@router.delete("/{job_id}")
def delete_job_description(job_id: str, db: Session = Depends(get_db)):
    """Deletes job description record."""
    jd_record = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not jd_record:
        raise HTTPException(status_code=404, detail="Job description not found.")

    db.delete(jd_record)
    db.commit()
    return {"message": "Job description deleted successfully."}
