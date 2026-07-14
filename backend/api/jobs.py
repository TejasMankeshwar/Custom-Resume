from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from backend.services.session_service import session_manager
from backend.services.jd_analyzer import jd_analyzer
from backend.services.scoring_service import scoring_service
from backend.services.resume_parser import ResumeParser
from backend.services.file_service import file_service, MasterResumeError
from backend.services.gemini_service import GeminiError

router = APIRouter()

class JobAnalyzeRequest(BaseModel):
    session_id: str
    job_description: str
    job_title: Optional[str] = ""

@router.post("/analyze")
def analyze_job(
    request: JobAnalyzeRequest, 
    x_gemini_key: str = Header(...),
    x_gemini_model: str = Header("gemini-1.5-flash")
):
    print(f"\n>>> [Jobs API] Starting job analysis for Session ID: {request.session_id} using model: {x_gemini_model}")
    session = session_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "message": "Session not found or expired.", "retryable": False})

    try:
        # 1. Analyze JD
        jd_analysis = jd_analyzer.analyze(
            x_gemini_key, 
            request.job_description, 
            request.job_title,
            model_name=x_gemini_model
        )
        
        # 2. Parse master resume
        raw_resume = file_service.read_master_resume()
        parsed_resume = ResumeParser.parse(raw_resume)
        
        # 3. Score
        match_analysis = scoring_service.calculate_score(jd_analysis, parsed_resume)
        
        # 4. Save to session
        session.jd_analysis = jd_analysis.model_dump()
        session.match_analysis = match_analysis
        
        return {
            "jd_analysis": session.jd_analysis,
            "match_analysis": match_analysis
        }
        
    except GeminiError as e:
        status_code = 429 if e.retryable else 500
        raise HTTPException(status_code=status_code, detail={"code": "GEMINI_ERROR", "message": str(e), "retryable": e.retryable})
    except MasterResumeError as e:
        raise HTTPException(status_code=500, detail={"code": "MASTER_RESUME_ERROR", "message": str(e), "retryable": False})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "INTERNAL_ERROR", "message": str(e), "retryable": False})
