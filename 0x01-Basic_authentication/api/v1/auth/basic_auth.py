#!/usr/bin/env python3
"""Module for basic authentication
"""

from api.v1.auth.auth import Auth
import base64


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
