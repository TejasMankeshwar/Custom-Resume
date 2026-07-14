import pytest
from backend.services.session_service import session_manager
from backend.services.file_service import file_service, FileSecurityError
from backend.services.resume_parser import ResumeParser
from backend.services.scoring_service import scoring_service
from pathlib import Path

def test_session_lifecycle():
    session_id = session_manager.create_session()
    assert session_id is not None
    
    session = session_manager.get_session(session_id)
    assert session is not None
    assert session.session_id == session_id
    
    deleted = session_manager.delete_session(session_id)
    assert deleted is True
    
    assert session_manager.get_session(session_id) is None

def test_master_resume_loading_and_hashing():
    content = file_service.read_master_resume()
    assert "Tejas Mankeshwar" in content
    
    file_hash = file_service.compute_master_resume_hash()
    assert isinstance(file_hash, str)
    assert len(file_hash) == 64

def test_path_traversal_protection():
    # Attempt a traversal
    traversal_id = "../../../etc/passwd"
    with pytest.raises(FileSecurityError):
        file_service.get_safe_session_dir(traversal_id)

def test_filename_sanitization():
    unsafe = "Resume  @#$ %^ name.tex"
    safe = file_service.sanitize_filename(unsafe)
    assert "@" not in safe
    assert "$" not in safe
    assert " " not in safe

def test_resume_parser_stable_ids():
    content = file_service.read_master_resume()
    parsed = ResumeParser.parse(content)
    
    assert "sections" in parsed
    
    has_experience = False
    for sec in parsed["sections"]:
        if "experience" in sec["id"].lower():
            has_experience = True
            # Check entries
            assert len(sec["entries"]) > 0
            first_entry = sec["entries"][0]
            assert "entry_01" in first_entry["id"]
            
            # Check bullets
            if "bullets" in first_entry and len(first_entry["bullets"]) > 0:
                first_bullet = first_entry["bullets"][0]
                assert "bullet_01" in first_bullet["id"]
    
    assert has_experience

from backend.schemas.gemini import JobAnalysisSchema

def test_scoring_service():
    jd_mock = JobAnalysisSchema(
        job_title="Software Engineer",
        required_skills=["Python", "React", "FastAPI"],
        preferred_skills=["Docker", "AWS"],
        keywords=["Machine Learning", "FastAPI"],
        experience_requirements=["Data Science Intern"],
        education_requirements=["B.E in Computer Science"]
    )
    
    content = file_service.read_master_resume()
    parsed = ResumeParser.parse(content)
    
    score = scoring_service.calculate_score(jd_mock, parsed)
    assert score["total_score"] > 0
    assert score["total_score"] <= 100
    
    # Test weak match
    weak_jd_mock = JobAnalysisSchema(
        job_title="Architect",
        required_skills=["Cobol", "Fortran"],
        preferred_skills=["VBScript"],
        keywords=["Mainframe"],
        experience_requirements=["Senior Architect"],
        education_requirements=["Ph.D"]
    )
    weak_score = scoring_service.calculate_score(weak_jd_mock, parsed)
    assert weak_score["total_score"] < score["total_score"]
    
    # Empty JD
    empty_jd_mock = JobAnalysisSchema(job_title="None")
    empty_score = scoring_service.calculate_score(empty_jd_mock, parsed)
    # If no requirements, we set 1.0 (100% match for nothing required)
    assert empty_score["total_score"] == 100
