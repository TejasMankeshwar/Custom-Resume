from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from backend.services.session_service import session_manager
from backend.services.gemini_service import GeminiService, GeminiError

router = APIRouter()

class SessionCreateResponse(BaseModel):
    session_id: str
    message: str

class ErrorResponse(BaseModel):
    code: str
    message: str
    retryable: bool

@router.post("/", response_model=SessionCreateResponse)
def create_session():
    session_id = session_manager.create_session()
    return {"session_id": session_id, "message": "Session created successfully."}

@router.post("/validate-key")
def validate_gemini_key(x_gemini_key: str = Header(...)):
    try:
        is_valid = GeminiService.validate_key(x_gemini_key)
        if is_valid:
            return {"message": "Key is valid."}
        else:
            raise HTTPException(status_code=401, detail={"code": "INVALID_KEY", "message": "Key is invalid or lacking quota.", "retryable": False})
    except HTTPException:
        raise
    except GeminiError as e:
        raise HTTPException(status_code=401, detail={"code": "INVALID_KEY", "message": str(e), "retryable": False})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "INTERNAL_ERROR", "message": "Validation failed.", "retryable": False})


@router.delete("/{session_id}")
def delete_session(session_id: str):
    success = session_manager.delete_session(session_id)
    if not success:
        return {"code": "SESSION_NOT_FOUND", "message": "Session not found.", "retryable": False}
    return {"message": "Session deleted successfully."}
