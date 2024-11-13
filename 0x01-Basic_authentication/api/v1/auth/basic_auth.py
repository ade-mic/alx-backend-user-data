#!/usr/bin/env python3
"""
class BasicAuth that inherits from Auth.
For the moment this class will be empty.
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    class BasicAuth that inherits from Auth.
    For the moment this class will be empty.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """
         returns the Base64 part of the Authorization
         header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Returns the decoded
        value of a Base64 string base64_authorization_header
        Args:
            base64_authorization_header (str)
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(
                base64_authorization_header
            )
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except(base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded
        Args:
            decoded_base64_authorization_header: str
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password.
            Args:
                    user_email: str,
                    user_pwd: str
        """
        if user_email is None and user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users or len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        BasicAuth that overloads Auth
        and retrieves the User instance for a request
        """
        authorization_header = self.authorization_header(request=request)
        extract_base64 = self.extract_base64_authorization_header(
            authorization_header)
        decode_base64 = self.decode_base64_authorization_header(extract_base64)
        credential = self.extract_user_credentials(decode_base64)
        user = self.user_object_from_credentials(user_email=credential[0],
                                                 user_pwd=credential[1])
        return user
