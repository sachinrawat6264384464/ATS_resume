# ResumeIQ — Production Deployment Guide

## 1. Quickstart: Docker Compose (All-in-One)

The simplest method to deploy ResumeIQ in production with complete service isolation (Next.js frontend, FastAPI backend, PostgreSQL with pgvector, Redis, Celery background worker, and Nginx reverse proxy) is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/sachinrawat6264384464/ATS_resume.git
cd ATS_resume

# Launch all 6 services in detached mode
docker compose up --build -d
```

### Deployed Services & Ports:
- **Nginx Gateway**: `http://localhost:80` (routes `/api` to backend and `/` to frontend)
- **Frontend Web UI**: `http://localhost:3000`
- **FastAPI Backend**: `http://localhost:8000` (docs at `/docs`)
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`
- **Celery Worker**: In-container background worker

---

## 2. Cloud Deployment: Render (Backend) + Vercel (Frontend)

### Backend Deployment (Render Web Service)
1. In the [Render Dashboard](https://dashboard.render.com), create a new **Web Service** pointing to your GitHub repository.
2. Configure settings:
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Add Environment Variables:
   - `ENVIRONMENT`: `production`
   - `DATABASE_URL`: Your PostgreSQL connection string (e.g. from Neon, Supabase, or Render PostgreSQL with `sslmode=require`).
   - `REDIS_URL`: Your Redis connection string (or leave empty to use in-memory resilient cache).
   - `FRONTEND_URL`: `https://<your-app>.vercel.app`
   - `BACKEND_URL`: `https://<your-render-service>.onrender.com`
   - `MAX_UPLOAD_SIZE_MB`: `10`

### Frontend Deployment (Vercel)
1. In the [Vercel Dashboard](https://vercel.com), import your GitHub repository.
2. Configure settings:
   - **Root Directory**: `frontend`
   - **Framework Preset**: `Next.js`
3. Add Environment Variables:
   - `NEXT_PUBLIC_API_URL`: `https://<your-render-service>.onrender.com/api/v1`
4. Deploy. Client-side routes (`/analyze`, `/results/[id]`, `/improve/[id]`) are fully prerendered with dynamic Suspense boundaries.

---

## 3. Environment Variables Reference

| Variable | Default Value | Description |
|---|---|---|
| `ENVIRONMENT` | `development` | Operating environment (`development`, `production`, `test`). |
| `DATABASE_URL` | `sqlite:///./resumeiq.db` | SQLAlchemy database connection URI (supports SQLite and PostgreSQL). |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection URL for Celery queue and caching. |
| `FRONTEND_URL` | `http://localhost:3000` | Allowed CORS origin for frontend requests. |
| `BACKEND_URL` | `http://localhost:8000` | Backend API server base URL. |
| `MAX_UPLOAD_SIZE_MB` | `10` | Maximum allowed file upload size. |
| `RATE_LIMIT_PER_MINUTE` | `60` | Sliding-window request limit per client IP. |
| `UPLOAD_DIR` | `./uploads` | Directory for isolated temporary resume storage. |
