#!/usr/bin/env python3
"""
Module of UserSession
"""
from models.base import Base
import uuid


class UserSession(Base):
    """
    inherits from Base
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialise this
        Args:
            user_id: string
            session_id: string
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
