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
from typing import Union


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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        It takes a single session_id string argument
        and returns the corresponding User or None.
        Args:
            session_id(str)
        Returns:
            User or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        updates the corresponding user’s session ID to None
        Args:
            user_id(int)
        Return:
            None
        """
        try:
            self._db.update_user(user_id=user_id, session_id=None)
            return None
        except NoResultFound:
            raise ValueError('No user found with the id')

    def get_reset_password_token(self, email: str):
        """
        generate a UUID and update the user’s reset_token
        Args:
            email(str)
        Return:
            token(str): a UUID and update the user’s reset_token
        Exceptions:
            ValueError: If the user does not exist
        """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError(f'user with {email} not found')

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Use the reset_token to find the corresponding user.
        Args:
            reset_token (str): find the corresponding user
            password (str)
        Returns:
             None
        Raises:
            ValueError: if reset_token does not correspond to any user
        hash the password and update the user’s hashed_password field
        with the new hashed password and the reset_token field to None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hash_password = _hash_password(password)
            self._db.update_user(user.id, hash_password=hash_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError('user does not exist')


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
    return str(uuid4())
