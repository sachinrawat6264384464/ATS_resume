import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import init_db
from app.api.v1.health import router as health_router
from app.api.v1.resumes import router as resumes_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.reports import router as reports_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Agentic AI-Powered ATS Resume Analyzer with explainable deterministic matching.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
origins = [
    settings.FRONTEND_URL,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "path": request.url.path
        }
    )

# Include Routers
app.include_router(health_router, prefix=settings.API_V1_STR, tags=["System Health"])
app.include_router(resumes_router, prefix=f"{settings.API_V1_STR}/resumes", tags=["Resumes"])
app.include_router(jobs_router, prefix=f"{settings.API_V1_STR}/jobs", tags=["Job Descriptions"])
app.include_router(analysis_router, prefix=f"{settings.API_V1_STR}/analysis", tags=["ATS Analysis"])
app.include_router(reports_router, prefix=f"{settings.API_V1_STR}/reports", tags=["Reports"])


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "status": "online",
        "docs_url": "/docs",
        "health_check": f"{settings.API_V1_STR}/health"
    }
