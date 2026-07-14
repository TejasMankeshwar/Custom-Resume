from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import health, session, resume, jobs

app = FastAPI(
    title="Resume Tailoring API",
    description="Backend API for the AI Resume Tailoring App",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(session.router, prefix="/api/session", tags=["Session"])
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
