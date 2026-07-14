import pytest
from unittest.mock import patch, MagicMock
from backend.services.session_service import session_manager
from backend.schemas.gemini import JobAnalysisSchema
from backend.services.gemini_service import GeminiError

# Testing Gemini Key Validation Flow
@patch('backend.services.gemini_service.GeminiService.validate_key')
def test_validate_key_success(mock_validate):
    mock_validate.return_value = True
    from backend.api.session import validate_gemini_key
    
    response = validate_gemini_key("test_key", "gemini-3.5-flash")
    assert response["message"] == "Key is valid."
    mock_validate.assert_called_once_with("test_key", "gemini-3.5-flash")

@patch('backend.services.gemini_service.GeminiService.validate_key')
def test_validate_key_failure(mock_validate):
    mock_validate.return_value = False
    from backend.api.session import validate_gemini_key
    from fastapi import HTTPException
    
    with pytest.raises(HTTPException) as exc:
        validate_gemini_key("bad_key")
    assert exc.value.status_code == 401
    assert "Key is invalid" in exc.value.detail["message"]

# Testing Job Analysis Flow
@patch('backend.services.jd_analyzer.JDAnalyzer.analyze')
def test_analyze_job_success(mock_analyze):
    mock_analyze.return_value = JobAnalysisSchema(
        job_title="Mock Engineer",
        required_skills=["Python"],
        preferred_skills=[],
        technologies=[],
        programming_languages=["Python"],
        frameworks=[],
        responsibilities=[],
        experience_requirements=[],
        education_requirements=[],
        keywords=[]
    )
    from backend.api.jobs import analyze_job, JobAnalyzeRequest
    
    session_id = session_manager.create_session()
    request = JobAnalyzeRequest(session_id=session_id, job_description="Need a Python dev")
    
    response = analyze_job(request, "mock_key")
    assert "jd_analysis" in response
    assert response["jd_analysis"]["job_title"] == "Mock Engineer"
    assert "match_analysis" in response
    
    session = session_manager.get_session(session_id)
    assert session.jd_analysis is not None
    assert session.match_analysis is not None

# Testing Validation Pipeline Strictness
def test_validation_pipeline_rejects_unsupported():
    from backend.services.validation_pipeline import ChangeValidationPipeline
    from backend.schemas.gemini import ResumeChangeSchema
    
    # Mock JD requiring Rust
    jd = JobAnalysisSchema(
        job_title="Dev", required_skills=["Rust"]
    )
    
    # Mock Resume not containing Rust
    parsed_resume = {
        "sections": [
            {
                "id": "exp", "raw_content": "I know Python",
                "entries": [
                    {"id": "entry1", "bullets": [{"id": "b1", "description": "I know Python"}]}
                ]
            }
        ]
    }
    
    pipeline = ChangeValidationPipeline(parsed_resume, jd)
    
    changes = [
        ResumeChangeSchema(
            change_id="1", change_type="REWRITE", target_id="b1",
            section="exp", original_content="I know Python",
            proposed_content="I know Python and Rust", # Fabricating Rust!
            reason="added rust", jd_requirements=["Rust"], keywords=["Rust"], confidence=100
        )
    ]
    
    valid, warnings = pipeline.validate_changes(changes)
    assert len(valid) == 0
    assert len(warnings) == 1
    assert "unsupported skill/requirement: rust" in warnings[0].lower()

def test_validation_pipeline_rejects_dangerous_latex():
    from backend.services.validation_pipeline import ChangeValidationPipeline
    from backend.schemas.gemini import ResumeChangeSchema
    
    jd = JobAnalysisSchema(job_title="Dev")
    parsed_resume = {
        "sections": [
            {
                "id": "exp", "raw_content": "I know Python",
                "entries": [
                    {"id": "entry1", "bullets": [{"id": "b1", "description": "I know Python"}]}
                ]
            }
        ]
    }
    pipeline = ChangeValidationPipeline(parsed_resume, jd)
    
    changes = [
        ResumeChangeSchema(
            change_id="1", change_type="REWRITE", target_id="b1",
            section="exp", original_content="I know Python",
            proposed_content=r"I know Python \input{/etc/passwd}", # Dangerous!
            reason="injection", jd_requirements=[], keywords=[], confidence=100
        )
    ]
    
    valid, warnings = pipeline.validate_changes(changes)
    assert len(valid) == 0
    assert "dangerous" in warnings[0].lower()
