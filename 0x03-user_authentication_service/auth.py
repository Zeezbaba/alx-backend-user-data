#!/usr/bin/env python3
"""password hashing using bycrpt
"""

import bcrypt
import uuid
from db import DB
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hashing
    """
    salt = bcrypt.gensalt()
    pass_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return pass_hash


def _generate_uuid() -> str:
    """return a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """user registration
        """
        try:
            # check if user already exist
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            password_hash = _hash_password(password)
            new_user = self._db.add_user(email, password_hash.decode('utf-8'))
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """validate user login
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password.encode('utf-8'))
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """find the user corresponding to the email,
        generate a new UUID and store it in the database
        as the user session_id, then return the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """gets user from session id
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user’s session ID to None
        """
        try:
            user = self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass
