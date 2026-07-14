from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Any
from backend.services.file_service import file_service, MasterResumeError
from backend.services.resume_parser import ResumeParser
from backend.services.scoring_service import scoring_service
from backend.services.session_service import session_manager
from backend.services.tailoring_service import tailoring_service
from backend.services.gemini_service import GeminiError
from backend.schemas.gemini import JobAnalysisSchema

router = APIRouter()

class ResumeMatchRequest(BaseModel):
    session_id: str
    jd_analysis: Dict[str, Any]

class GenerateChangesRequest(BaseModel):
    session_id: str

@router.post("/generate-changes")
def generate_changes(request: GenerateChangesRequest, x_gemini_key: str = Header(...)):
    session = session_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "message": "Session not found.", "retryable": False})
        
    if not session.jd_analysis or not session.match_analysis:
        raise HTTPException(status_code=400, detail={"code": "MISSING_ANALYSIS", "message": "Job Description analysis must be completed before generating changes.", "retryable": False})

    try:
        raw_resume = file_service.read_master_resume()
        parsed_resume = ResumeParser.parse(raw_resume)
        jd_schema = JobAnalysisSchema.model_validate(session.jd_analysis)
        
        result = tailoring_service.generate_changes(x_gemini_key, parsed_resume, jd_schema, session.match_analysis)
        
        session.validated_changes = result["validated_changes"]
        session.rejection_warnings = result["rejection_warnings"]
        
        return result
        
    except GeminiError as e:
        raise HTTPException(status_code=500, detail={"code": "GEMINI_ERROR", "message": str(e), "retryable": e.retryable})
    except MasterResumeError as e:
        raise HTTPException(status_code=500, detail={"code": "MASTER_RESUME_ERROR", "message": str(e), "retryable": False})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "INTERNAL_ERROR", "message": str(e), "retryable": False})

@router.post("/match")
def match_resume(request: ResumeMatchRequest):
    try:
        raw_resume = file_service.read_master_resume()
        parsed_resume = ResumeParser.parse(raw_resume)
        score = scoring_service.calculate_score(request.jd_analysis, parsed_resume)
        
        return {
            "score": score,
            "parsed_resume_sections": len(parsed_resume.get("sections", []))
        }
    except MasterResumeError as e:
        raise HTTPException(status_code=500, detail={"code": "MASTER_RESUME_ERROR", "message": str(e), "retryable": False})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "INTERNAL_ERROR", "message": str(e), "retryable": False})

@router.get("/master")
def get_master_resume_info():
    try:
        raw_resume = file_service.read_master_resume()
        resume_hash = file_service.compute_master_resume_hash()
        parsed = ResumeParser.parse(raw_resume)
        return {
            "hash": resume_hash,
            "sections_count": len(parsed["sections"])
        }
    except MasterResumeError as e:
        raise HTTPException(status_code=500, detail={"code": "MASTER_RESUME_ERROR", "message": str(e), "retryable": False})
