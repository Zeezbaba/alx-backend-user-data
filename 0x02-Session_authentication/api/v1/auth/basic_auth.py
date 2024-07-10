#!/usr/bin/env python3
"""Module for basic authentication
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) \
            -> str:
        """ returns the decoded value of a Base64
        string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_header = base64.b64decode(base64_authorization_header
                                              .encode('utf-8'))
            return decoded_header.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) \
            -> (str, str):
        """returns the user email and password
        from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based
        on his email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        user = User.search({"email": user_email})
        if not user or user == []:
            return None

        user = user[0]
        # Validate the password
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves
        the User instance for a request
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth_header = \
            self.extract_base64_authorization_header(auth_header)
        if base64_auth_header is None:
            return None

        decoded_auth_header = \
            self.decode_base64_authorization_header(base64_auth_header)
        if decoded_auth_header is None:
            return None

        user_email, user_pwd = \
            self.extract_user_credentials(decoded_auth_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
