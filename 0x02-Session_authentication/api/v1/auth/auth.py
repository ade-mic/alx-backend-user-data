#!/usr/bin/env python3
"""
The module contains api/v1/auth/auth.py
"""
from flask import request
from typing import List, TypeVar
import fnmatch
from os import getenv


class Auth:
    """
    a class for API authentication
    public method:
        def require_auth(
            self, path: str,
            excluded_paths: List[str]) -> bool:
            that returns False - path and excluded_paths will be used later
        def authorization_header(self, request=None) -> str:
            that returns None - request will be the Flask request object
        def current_user(self, request=None) -> TypeVar('User'):
            that returns None - request will be the Flask request object
    """
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """
        Args:
            path(str):
            excluded_paths(List[str]):
        Returns: False - path and excluded_paths will be used late
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_path += '/'
            if fnmatch.fnmatch(path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns None - request will be the Flask request object
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None - request will be the Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        Return:
            None if request is None
            The value of the cookie named _my_session_id
            from request - the name of the cookie must be
            defined by the environment variable SESSION_NAME
            You must use .get() built-in for accessing the
            cookie in the request cookies dictionary
            You must use the environment variable SESSION_NAME
            to define the name of the cookie used for the Session ID
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
