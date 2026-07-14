import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import threading

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
    def __init__(self, expiry_minutes: int = 60):
        self._sessions: Dict[str, Session] = {}
        self.expiry_minutes = expiry_minutes
        self._lock = threading.Lock()

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
                    return None
                session.last_accessed = datetime.now()
                return session
            return None

    def delete_session(self, session_id: str) -> bool:
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
                return True
            return False

session_manager = SessionService()
