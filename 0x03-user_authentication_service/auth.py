#!/usr/bin/env python3
"""
define a _hash_password method that takes in a password
string arguments and returns bytes
Args:
    password(str)
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Auth.register_user should take mandatory
            Args:
                email(str)
                password(str)
            Returns
                User object.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email=email,
                                         hashed_password=hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        expect
        Args:
            email(str)
            password(str)
            required arguments and
        Return
             boolean.
        """
        try:
            user = self._db.find_user_by(email=email)
            is_correct = bcrypt.checkpw(password.encode('utf-8'),
                                        user.hashed_password)
            return is_correct
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        The method should find the user corresponding to the email,
        generate a new UUID and store it in the database as the
        user’s session_id
        Args:
            email(str)
        Returns:
            session_id: returns session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = str(uuid4())
            self._db.update_user(user_id=user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None


def _hash_password(password: str) -> bytes:
    """
    define a _hash_password method that takes in a password
    string arguments and returns bytes
    Args:
        password(str)
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return uuid4()
