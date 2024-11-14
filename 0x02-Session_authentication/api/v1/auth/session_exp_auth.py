#!/usr/bin/env python3
"""
Module of SessionExpAuth
"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    def __init__(self):
        """
        Initialize session duration from the environment variable SESSION_DURATION.
        If not set or invalid, default to 0 (no expiration).
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session ID and store it in the dictionary with the current timestamp.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create session dictionary with user_id and created_at timestamp
        session_info = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        # Store session info
        self.user_id_by_session_id[session_id] = session_info
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve user_id if the session is still valid.
        """
        if session_id is None:
            return None

        session_info = self.user_id_by_session_id.get(session_id)
        if session_info is None:
            return None

        # Check if session duration is 0 (no expiration)
        if self.session_duration <= 0:
            return session_info.get("user_id")

        # Check for created_at and expiration
        created_at = session_info.get("created_at")
        if created_at is None:
            return None

        # Validate if the session has expired
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None  # Session has expired

        # Session is valid
        return session_info.get("user_id")
