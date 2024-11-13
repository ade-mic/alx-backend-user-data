#!/usr/bin/env python3
"""
The module contains api/v1/auth/auth.py
"""
from flask import request
from typing import List, TypeVar
import fnmatch


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

        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_path += '/'
                if fnmatch.fnmatch(path, excluded_path):
                    return False
        return False

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
