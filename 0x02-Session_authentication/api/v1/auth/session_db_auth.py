# api/v1/auth/session_db_auth.py
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from typing import Optional


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class that stores sessions in a database/file
    instead of memory for persistence across restarts.
    """
    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """
        Create and store a new session in the database,
        returning the Session ID.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create a new UserSession instance
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Save it to the database (or file storage)

        return session_id

    def user_id_for_session_id(self, session_id: Optional[str] =
                               None) -> Optional[str]:
        """
        Retrieve the User ID associated with a session ID from the database.
        """
        if session_id is None:
            return None

        # Look for a UserSession in the database by session_id
        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return None

        user_session = user_sessions[0]

        # Check session expiration
        if self.session_duration <= 0:
            return user_session.user_id
        created_at = user_session.created_at
        if created_at + timedelta(seconds=self.session_duration
                                  ) < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroy the session by removing it from the database using session ID.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Search for the session in the database and delete it
        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()  # Remove from database

        return True
