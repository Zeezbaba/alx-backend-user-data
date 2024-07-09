#!/usr/bin/env python3
"""class to manage the API authentication
"""

from flask import request
from typing import List, TypeVar


class Auth():
    """Manages API Authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """determine if a path require auth.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif excluded_path.endswith('/'):
                if path == excluded_path:
                    return False
            else:
                if path == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """retrieves auth. header from request
        """
        if request is None:
            return None
        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves current user
        """
        return None
