#!/usr/bin/env python3
"""stores session id in the database
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from flask import request
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication with database storage
    """
    def create_session(self, user_id=None):
        """creates and stores new instance of
        UserSession and returns the Session ID
        """
        session_id = super().create_session(user_id)

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting UserSession
        in the database based on session_id
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """destroys the UserSession based on the
        Session ID from the request cookie
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        user_session = sessions[0]
        user_session.remove()
        return True
