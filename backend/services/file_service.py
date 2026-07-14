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

file_service = FileService()
