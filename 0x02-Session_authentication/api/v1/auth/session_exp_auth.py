#!/usr/bin/env python3
"""
Module of SessionExpAuth
"""
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth that inherits from SessionAuth with session
      expiration.
    """

    def __init__(self):
        """
        Initialize SessionExpAuth with session duration
          from environment variable.
        """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session ID for a user and stores the user and timestamp
        in a session dictionary if successful.

        Args:
            user_id (str): The user ID to create a session for.

        Returns:
            str: The created session ID, or None if creation failed.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store session dictionary with user_id and created_at
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a session ID if the session
        is still valid.

        Args:
            session_id (str): The session ID to retrieve the user ID for.

        Returns:
            str: The user ID associated with the session ID, or None if the
                 session has expired or is invalid.
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        # If session_duration is 0 or less, session never expires
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        # Check for creation time and if the session has expired
        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        # Validate expiration
        if created_at + timedelta(seconds=self.session_duration)\
                < datetime.now():
            return None  # Session has expired

        return session_dict.get('user_id')
