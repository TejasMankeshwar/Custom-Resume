import pytest
from unittest.mock import patch, MagicMock
import unittest.mock
from backend.services.change_service import change_service, ChangeServiceError
from backend.services.latex_service import LaTeXService, LaTeXCompilationError
from backend.schemas.gemini import ResumeChangeSchema

# Sample fake resume
FAKE_MASTER_RESUME = r"""
\section{Experience}
\resumeSubheading{Software Engineer}{Company A}{San Francisco, CA}{2020 - Present}
\resumeItemNH{Built a scalable backend system using Python.}
\resumeItemNH{Improved performance by 50\%.}
"""

def test_change_service_missing_decision():
    change = ResumeChangeSchema(
        change_id="c1", change_type="REWRITE", target_id="fake", section="Exp",
        original_content="fake", proposed_content="new", reason="r", jd_requirements=[], keywords=[], confidence=90
    )
    with pytest.raises(ChangeServiceError, match="Missing decision for change_id c1"):
        change_service.apply_changes("sess1", {}, [change])

@patch('backend.services.file_service.FileService.read_master_resume')
@patch('backend.services.file_service.FileService.compute_master_resume_hash')
@patch('backend.services.file_service.FileService.write_generated_resume')
def test_change_service_apply_accepted(mock_write, mock_hash, mock_read):
    mock_read.return_value = FAKE_MASTER_RESUME
    mock_hash.return_value = "fakehash"
    mock_write.return_value = "generated.tex"

    change = ResumeChangeSchema(
        change_id="c1", change_type="REWRITE", target_id="section_experience_entry_01_bullet_01", section="Exp",
        original_content="Built a scalable backend system using Python.", proposed_content="Architected a highly scalable backend using Python and FastAPI.", reason="r", jd_requirements=[], keywords=[], confidence=90
    )

    result = change_service.apply_changes("sess1", {"c1": "ACCEPTED"}, [change])
    assert result["status"] == "SUCCESS"
    assert result["accepted_count"] == 1
    
    # Verify write was called with the modified content
    args, _ = mock_write.call_args
    assert args[0] == "sess1"
    assert "Architected a highly scalable backend using Python and FastAPI." in args[1]
    assert "Built a scalable backend system using Python." not in args[1]

@patch('subprocess.run')
@patch('os.path.exists')
def test_latex_service_success(mock_exists, mock_run):
    # Setup mocks
    # First call is to check latexmk, second is the actual run
    mock_run.return_value = MagicMock(returncode=0)
    mock_exists.side_effect = [True, True, True] # session_dir, resume.tex, resume.pdf (after compile)

    # We also need to mock open for the dangerous macro check
    with patch("builtins.open", unittest.mock.mock_open(read_data="clean latex content")):
        pdf_path = LaTeXService.compile_resume("sess1")
        assert "resume.pdf" in pdf_path

@patch('os.path.exists')
def test_latex_service_dangerous_macro(mock_exists):
    mock_exists.side_effect = [True, True]
    with patch("builtins.open", unittest.mock.mock_open(read_data=r"some malicious \write18{rm -rf /} command")):
        with pytest.raises(LaTeXCompilationError, match="Dangerous LaTeX command detected"):
            LaTeXService.compile_resume("sess1")
