import hashlib
import os
from pathlib import Path

# Use the actual master resume paths
MASTER_RESUME_PATH = Path("Resume/main.tex").resolve()
GENERATED_DIR = Path("generated").resolve()

class MasterResumeError(Exception):
    pass

class FileSecurityError(Exception):
    pass

class FileService:
    @staticmethod
    def get_master_resume_path() -> Path:
        return MASTER_RESUME_PATH

    @staticmethod
    def read_master_resume() -> str:
        if not MASTER_RESUME_PATH.exists():
            raise MasterResumeError("The master resume could not be loaded.")
        with open(MASTER_RESUME_PATH, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def compute_master_resume_hash() -> str:
        if not MASTER_RESUME_PATH.exists():
            raise MasterResumeError("The master resume could not be loaded.")
        sha256_hash = hashlib.sha256()
        with open(MASTER_RESUME_PATH, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @staticmethod
    def get_safe_session_dir(session_id: str) -> Path:
        """Resolve session dir and prevent path traversal."""
        session_dir = (GENERATED_DIR / session_id).resolve()
        
        # Verify it is contained inside GENERATED_DIR
        try:
            session_dir.relative_to(GENERATED_DIR)
        except ValueError:
            raise FileSecurityError("Invalid session ID resulting in path traversal attempt.")
            
        return session_dir

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filenames to only allow safe characters."""
        import re
        # Allow alphanumeric, dashes, and underscores
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)
        return safe_name

    @staticmethod
    def write_generated_resume(session_id: str, content: str) -> str:
        session_dir = FileService.get_safe_session_dir(session_id)
        session_dir.mkdir(parents=True, exist_ok=True)
        out_path = session_dir / "resume.tex"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        return str(out_path)

    @staticmethod
    def read_generated_resume(session_id: str) -> str:
        session_dir = FileService.get_safe_session_dir(session_id)
        out_path = session_dir / "resume.tex"
        if not out_path.exists():
            raise MasterResumeError("Generated resume not found.")
        with open(out_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def delete_session_dir(session_id: str) -> bool:
        import shutil
        try:
            session_dir = FileService.get_safe_session_dir(session_id)
            if session_dir.exists() and session_dir.is_dir():
                shutil.rmtree(session_dir)
                return True
        except Exception:
            pass
        return False

file_service = FileService()
