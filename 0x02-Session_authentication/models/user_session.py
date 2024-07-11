#!/usr/bin/env python3
"""authentication system, based on Session
ID stored in database
"""

from models.base import Base


class UserSession(Base):
    """store session IDs in the database
    """
    def __init__(self, *args: list, **kwargs: dict):
        """initialization
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
