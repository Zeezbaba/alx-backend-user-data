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
        return False

    def authorization_header(self, request=None) -> str:
        """retrieves auth. header from request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves current user
        """
        return None
