from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Analysis
from app.services.pdf_report_generator import PDFReportGenerator

router = APIRouter()


@router.get("/{analysis_id}/pdf")
def download_pdf_report(analysis_id: str, db: Session = Depends(get_db)):
    """Generates and downloads a clean, publication-ready PDF audit report."""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found.")

    if analysis.status != "completed":
        raise HTTPException(status_code=400, detail="Cannot generate PDF for an incomplete analysis.")

    match_detail = analysis.match_detail
    recommendations = analysis.recommendations

    analysis_data = {
        "analysis_id": analysis.id,
        "candidate_name": analysis.resume.parsed_resume.contact_info.get("name") if analysis.resume and analysis.resume.parsed_resume else "Candidate",
        "job_title": analysis.job_description.title if analysis.job_description else "Target Role",
        "scoring_version": analysis.scoring_version,
        "scores": {
            "overall": analysis.overall_score or 0.0,
            "keyword": analysis.keyword_score or 0.0,
            "semantic": analysis.semantic_score or 0.0,
            "experience": analysis.experience_score or 0.0,
            "project": analysis.project_score or 0.0,
            "education": analysis.education_score or 0.0
        },
        "matched_skills": match_detail.matched_skills if match_detail else [],
        "missing_mandatory": match_detail.missing_mandatory if match_detail else [],
        "recommendations": [
            {
                "priority": r.priority,
                "category": r.category,
                "suggested_text": r.suggested_text,
                "reasoning": r.reasoning
            }
            for r in recommendations
        ]
    }

    pdf_bytes = PDFReportGenerator.generate(analysis_data)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="ResumeIQ_Report_{analysis.id[:8]}.pdf"'
        }
    )

