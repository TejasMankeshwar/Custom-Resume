from typing import Dict, Any, Optional, List
import uuid
from datetime import datetime, timedelta
import threading
import time
from backend.services.file_service import file_service

class Session:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.now()
        self.last_accessed = self.created_at
        self.data: Dict[str, Any] = {}
        self.jd_analysis: Optional[Dict[str, Any]] = None
        self.match_analysis: Optional[Dict[str, Any]] = None
        self.validated_changes: List[Dict[str, Any]] = []
        self.rejection_warnings: List[str] = []

class SessionService:
    def __init__(self, expiry_minutes: int = 60, cleanup_interval_seconds: int = 300):
        self._sessions: Dict[str, Session] = {}
        self.expiry_minutes = expiry_minutes
        self._lock = threading.Lock()
        
        self.cleanup_interval_seconds = cleanup_interval_seconds
        self._stop_event = threading.Event()
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()

    def _cleanup_loop(self):
        while not self._stop_event.is_set():
            time.sleep(self.cleanup_interval_seconds)
            self._purge_expired_sessions()
            
    def _purge_expired_sessions(self):
        with self._lock:
            now = datetime.now()
            expired_ids = [
                sid for sid, session in self._sessions.items()
                if now - session.last_accessed > timedelta(minutes=self.expiry_minutes)
            ]
            for sid in expired_ids:
                del self._sessions[sid]
                # Try to clean up directory (ignoring errors in background thread)
                try:
                    file_service.delete_session_dir(sid)
                except Exception:
                    pass

    def create_session(self) -> str:
        with self._lock:
            session_id = str(uuid.uuid4())
            self._sessions[session_id] = Session(session_id)
            return session_id

    def get_session(self, session_id: str) -> Optional[Session]:
        with self._lock:
            session = self._sessions.get(session_id)
            if session:
                if datetime.now() - session.last_accessed > timedelta(minutes=self.expiry_minutes):
                    del self._sessions[session_id]
                    try:
                        file_service.delete_session_dir(session_id)
                    except Exception:
                        pass
                    return None
                session.last_accessed = datetime.now()
                return session
            return None

    def delete_session(self, session_id: str) -> bool:
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                try:
                    file_service.delete_session_dir(session_id)
                except Exception:
                    pass
                return True
            return False

session_manager = SessionService()
