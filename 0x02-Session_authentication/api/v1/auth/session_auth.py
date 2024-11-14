#!/usr/bin/env python3
"""
 class SessionAuth that inherits from Auth.
 For the moment this class will be empty.
 It’s the first step for creating a new authentication mechanism:
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
        class SessionAuth that inherits from Auth.
        For the moment this class will be empty.
        It’s the first step for creating a new authentication mechanism:
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id:
        Return None if user_id is None
        Return None if user_id is not a string
        Otherwise:
            Generate a Session ID using uuid module and uuid4() like id in Base
            Use this Session ID as key of the dictionary
            user_id_by_session_id - the value for this key must be user_id
        Return the Session ID
        The same user_id can have multiple Session ID -
        indeed, the user_id is the value in the dictionary
        user_id_by_session_id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns:
            a User ID based on a Session ID:
            None if session_id is None
            None if session_id is not a string
            the value (the User ID) for the key
            session_id in the dictionary user_id_by_session_id.
            You must use .get() built-in for
            accessing in a dictionary a value based on key
        """
        if session_id is None or not isinstance(session_id,
                                                str):
            return None
        return self.user_id_by_session_id.get(session_id)
