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
        status_code = 429 if e.retryable else 500
        raise HTTPException(status_code=status_code, detail={"code": "GEMINI_ERROR", "message": str(e), "retryable": e.retryable})
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

class GenerateResumeRequest(BaseModel):
    session_id: str
    decisions: Dict[str, str]

@router.post("/generate")
def generate_resume(request: GenerateResumeRequest):
    session = session_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND", "message": "Session not found."})
        
    if not session.validated_changes:
        raise HTTPException(status_code=400, detail={"code": "NO_CHANGES", "message": "No changes generated to apply."})

    from backend.services.change_service import change_service, ChangeServiceError
    try:
        result = change_service.apply_changes(request.session_id, request.decisions, session.validated_changes)
        
        # Calculate new score
        raw_resume = file_service.read_generated_resume(request.session_id)
        parsed_resume = ResumeParser.parse(raw_resume)
        new_score = scoring_service.calculate_score(session.jd_analysis, parsed_resume)
        
        result["new_score"] = new_score
        session.final_match_analysis = {
            "score": new_score
        }
        
        return result
    except ChangeServiceError as e:
        raise HTTPException(status_code=400, detail={"code": "CHANGE_SERVICE_ERROR", "message": str(e)})
    except MasterResumeError as e:
        raise HTTPException(status_code=500, detail={"code": "MASTER_RESUME_ERROR", "message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "INTERNAL_ERROR", "message": str(e)})

class CompileResumeRequest(BaseModel):
    session_id: str

@router.post("/compile")
def compile_resume(request: CompileResumeRequest):
    from backend.services.latex_service import LaTeXService, LaTeXCompilationError
    try:
        pdf_path = LaTeXService.compile_resume(request.session_id)
        return {"status": "SUCCESS", "pdf_path": pdf_path}
    except LaTeXCompilationError as e:
        raise HTTPException(status_code=500, detail={"code": e.code, "message": str(e)})

from fastapi.responses import FileResponse
import os
from backend.services.file_service import GENERATED_DIR

@router.get("/preview/{session_id}")
def preview_resume(session_id: str):
    session_dir = os.path.join(GENERATED_DIR, session_id)
    pdf_path = os.path.join(session_dir, "resume.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found. Please compile first.")
    return FileResponse(pdf_path, media_type="application/pdf", filename="Tejas_Resume_Tailored.pdf")

@router.get("/export/{session_id}/tex")
def export_tex(session_id: str):
    session_dir = os.path.join(GENERATED_DIR, session_id)
    tex_path = os.path.join(session_dir, "resume.tex")
    if not os.path.exists(tex_path):
        raise HTTPException(status_code=404, detail="TEX file not found. Please generate first.")
    return FileResponse(tex_path, media_type="application/x-tex", filename="Tejas_Resume_Tailored.tex")

@router.get("/export/{session_id}/pdf")
def export_pdf(session_id: str):
    session_dir = os.path.join(GENERATED_DIR, session_id)
    pdf_path = os.path.join(session_dir, "resume.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found. Please compile first.")
    return FileResponse(pdf_path, media_type="application/pdf", filename="Tejas_Resume_Tailored.pdf")
