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

    def _generate_uuid(self) -> str:
        """return a string representation of a new UUID
        """
        return str(uuid.uuid4())
