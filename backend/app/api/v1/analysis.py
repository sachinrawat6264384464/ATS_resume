import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db, SessionLocal
from app.models.models import Resume, JobDescription, Analysis, MatchDetail, Recommendation, ProcessingJob
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisStatusResponse,
    AnalysisReportResponse,
    ScoreBreakdown,
    MatchedSkillItem,
    MissingSkillItem,
    RelatedSkillItem,
    RecommendationItem
)
from app.graph.orchestrator import ats_pipeline

router = APIRouter()


def run_pipeline_sync(analysis_id: str, resume_id: str, job_id: str):
    """Executes the LangGraph analysis pipeline and persists the results idempotently."""
    db: Session = SessionLocal()
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        job_tracker = db.query(ProcessingJob).filter(ProcessingJob.analysis_id == analysis_id).first()

        if not resume or not job or not analysis:
            return

        # Prepare initial state for LangGraph
        initial_state = {
            "analysis_id": analysis_id,
            "resume_id": resume_id,
            "job_id": job_id,
            "resume_file": resume.file_path,
            "resume_text": resume.raw_text or "",
            "parsed_resume": {
                "skills": resume.parsed_resume.skills if resume.parsed_resume else [],
                "work_experience": resume.parsed_resume.work_experience if resume.parsed_resume else [],
                "education": resume.parsed_resume.education if resume.parsed_resume else [],
                "projects": resume.parsed_resume.projects if resume.parsed_resume else [],
                "certifications": resume.parsed_resume.certifications if resume.parsed_resume else [],
                "summary": resume.parsed_resume.summary if resume.parsed_resume else None,
                "contact_info": resume.parsed_resume.contact_info if resume.parsed_resume else {},
                "raw_text": resume.raw_text or ""
            },
            "job_description": job.raw_text,
            "parsed_job": job.extracted_data or {},
            "normalized_skills": [],
            "keyword_matches": {},
            "semantic_matches": {},
            "bm25_matches": {},
            "experience_analysis": {},
            "scoring_result": {},
            "recommendations": [],
            "validation_result": {},
            "final_report": {},
            "errors": [],
            "processing_status": "in_progress",
            "stage": "Pipeline Initialized",
            "progress_percentage": 10
        }

        # Run LangGraph pipeline
        result_state = ats_pipeline.invoke(initial_state)

        if result_state.get("processing_status") == "failed":
            analysis.status = "failed"
            analysis.error_message = "; ".join(result_state.get("errors", ["Processing failed"]))
            if job_tracker:
                job_tracker.status = "failed"
                job_tracker.error = analysis.error_message
                job_tracker.progress_percentage = 100
            db.commit()
            return

        final_rep = result_state.get("final_report", {})
        scores = final_rep.get("scores", {})

        # Update Analysis record
        analysis.status = "completed"
        analysis.overall_score = scores.get("overall", 0.0)
        analysis.keyword_score = scores.get("keyword", 0.0)
        analysis.semantic_score = scores.get("semantic", 0.0)
        analysis.experience_score = scores.get("experience", 0.0)
        analysis.project_score = scores.get("project", 0.0)
        analysis.education_score = scores.get("education", 0.0)
        analysis.completed_at = datetime.now(timezone.utc)

        # Idempotent MatchDetail handling
        existing_match = db.query(MatchDetail).filter(MatchDetail.analysis_id == analysis_id).first()
        if existing_match:
            existing_match.matched_skills = final_rep.get("matched_skills", [])
            existing_match.missing_skills = final_rep.get("missing_skills", [])
            existing_match.missing_mandatory = final_rep.get("missing_mandatory", [])
            existing_match.related_skills = final_rep.get("related_skills", [])
            existing_match.bm25_scores = result_state.get("bm25_matches", {})
            existing_match.semantic_matches = final_rep.get("semantic_details", [])
            existing_match.experience_analysis = final_rep.get("experience_analysis", {})
        else:
            match_detail = MatchDetail(
                analysis_id=analysis_id,
                matched_skills=final_rep.get("matched_skills", []),
                missing_skills=final_rep.get("missing_skills", []),
                missing_mandatory=final_rep.get("missing_mandatory", []),
                related_skills=final_rep.get("related_skills", []),
                bm25_scores=result_state.get("bm25_matches", {}),
                semantic_matches=final_rep.get("semantic_details", []),
                experience_analysis=final_rep.get("experience_analysis", {}),
                evidence_spans=[]
            )
            db.add(match_detail)

        # Idempotent Recommendations handling
        db.query(Recommendation).filter(Recommendation.analysis_id == analysis_id).delete()
        for rec in final_rep.get("recommendations", []):
            rec_record = Recommendation(
                id=rec.get("id") or str(uuid.uuid4()),
                analysis_id=analysis_id,
                category=rec.get("category", "general"),
                priority=rec.get("priority", "medium"),
                original_text=rec.get("original_text"),
                suggested_text=rec.get("suggested_text"),
                reasoning=rec.get("reasoning", "")
            )
            db.add(rec_record)

        if job_tracker:
            job_tracker.status = "completed"
            job_tracker.stage = "Report Ready"
            job_tracker.progress_percentage = 100

        db.commit()

    except Exception as e:
        db.rollback()
        try:
            analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis:
                analysis.status = "failed"
                analysis.error_message = str(e)
            job_tracker = db.query(ProcessingJob).filter(ProcessingJob.analysis_id == analysis_id).first()
            if job_tracker:
                job_tracker.status = "failed"
                job_tracker.error = str(e)
            db.commit()
        except Exception:
            pass
    finally:
        db.close()


@router.post("", response_model=AnalysisStatusResponse)
def create_analysis(
    payload: AnalysisCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Initiates an asynchronous multi-agent ATS analysis for a resume and job description."""
    resume = db.query(Resume).filter(Resume.id == payload.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")

    job = db.query(JobDescription).filter(JobDescription.id == payload.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found.")

    analysis_id = str(uuid.uuid4())
    analysis = Analysis(
        id=analysis_id,
        resume_id=payload.resume_id,
        job_id=payload.job_id,
        status="processing"
    )
    db.add(analysis)

    job_tracker = ProcessingJob(
        analysis_id=analysis_id,
        status="in_progress",
        stage="Starting Pipeline",
        progress_percentage=10
    )
    db.add(job_tracker)
    db.commit()

    # Trigger pipeline execution in background (Celery worker or FastAPI BackgroundTasks)
    dispatched_to_celery = False
    try:
        from app.core.celery_app import celery_app, run_ats_analysis_task
        from app.core.redis_client import cache
        if celery_app and cache.is_redis_available:
            run_ats_analysis_task.delay(analysis_id, payload.resume_id, payload.job_id)
            dispatched_to_celery = True
    except Exception:
        dispatched_to_celery = False

    if not dispatched_to_celery:
        background_tasks.add_task(run_pipeline_sync, analysis_id, payload.resume_id, payload.job_id)

    return AnalysisStatusResponse(
        analysis_id=analysis_id,
        status="processing",
        progress_percentage=10,
        stage="Starting Pipeline",
        message="LangGraph agent workflow dispatched via " + ("Celery queue" if dispatched_to_celery else "Background tasks") + "."
    )


@router.get("/{analysis_id}/status", response_model=AnalysisStatusResponse)
def get_analysis_status(analysis_id: str, db: Session = Depends(get_db)):
    """Polls real-time progress of an in-flight or completed ATS analysis."""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found.")

    job_tracker = db.query(ProcessingJob).filter(ProcessingJob.analysis_id == analysis_id).first()
    progress = 100 if analysis.status in ["completed", "failed"] else (job_tracker.progress_percentage if job_tracker else 50)
    stage = "Complete" if analysis.status == "completed" else ("Failed" if analysis.status == "failed" else (job_tracker.stage if job_tracker else "Processing"))

    return AnalysisStatusResponse(
        analysis_id=analysis.id,
        status=analysis.status,
        progress_percentage=progress,
        stage=stage,
        error=analysis.error_message
    )


@router.get("/{analysis_id}/report")
def get_analysis_report(analysis_id: str, db: Session = Depends(get_db)):
    """Retrieves the full explainable ATS matching report."""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found.")

    if analysis.status != "completed":
        return {
            "analysis_id": analysis.id,
            "status": analysis.status,
            "message": "Analysis is still processing. Please check status endpoint.",
            "error": analysis.error_message
        }

    match_detail = analysis.match_detail
    recommendations = analysis.recommendations

    return {
        "analysis_id": analysis.id,
        "resume_id": analysis.resume_id,
        "job_id": analysis.job_id,
        "status": analysis.status,
        "candidate_name": analysis.resume.parsed_resume.contact_info.get("name") if analysis.resume and analysis.resume.parsed_resume else "Candidate",
        "job_title": analysis.job_description.title if analysis.job_description else "Target Role",
        "scores": {
            "overall": analysis.overall_score or 0.0,
            "keyword": analysis.keyword_score or 0.0,
            "semantic": analysis.semantic_score or 0.0,
            "experience": analysis.experience_score or 0.0,
            "project": analysis.project_score or 0.0,
            "education": analysis.education_score or 0.0,
            "weights": {
                "keyword": 0.40,
                "semantic": 0.25,
                "experience": 0.20,
                "project": 0.10,
                "education": 0.05
            }
        },
        "matched_skills": match_detail.matched_skills if match_detail else [],
        "missing_skills": match_detail.missing_skills if match_detail else [],
        "missing_mandatory": match_detail.missing_mandatory if match_detail else [],
        "related_skills": match_detail.related_skills if match_detail else [],
        "experience_analysis": match_detail.experience_analysis if match_detail else {},
        "recommendations": [
            {
                "id": r.id,
                "category": r.category,
                "priority": r.priority,
                "original_text": r.original_text,
                "suggested_text": r.suggested_text,
                "reasoning": r.reasoning
            }
            for r in recommendations
        ],
        "scoring_version": analysis.scoring_version,
        "created_at": analysis.created_at,
        "completed_at": analysis.completed_at
    }


@router.delete("/{analysis_id}")
def delete_analysis(analysis_id: str, db: Session = Depends(get_db)):
    """Purges analysis record and match details."""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found.")

    db.delete(analysis)
    db.commit()
    return {"message": "Analysis purged successfully."}
